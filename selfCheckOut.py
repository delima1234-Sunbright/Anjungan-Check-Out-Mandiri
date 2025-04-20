from flask import Flask, render_template, Response, jsonify, redirect, url_for, session, request, copy_current_request_context
import cv2
from pyzbar.pyzbar import decode
import threading
import time
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import midtransclient
import uuid

app = Flask(__name__)
app.secret_key = 'Delimabrpurba7225'

# Midtrans Configuration (Sandbox)
MIDTRANS_CLIENT_KEY = 'SB-Mid-client-DgT73RW4UTD9dsy7'  # Replace with your Midtrans Sandbox Client Key
MIDTRANS_SERVER_KEY = 'SB-Mid-server-GEWrPzhUN6u915Pthmk5n12d'  # Replace with your Midtrans Sandbox Server Key

# Initialize Midtrans Snap API Client
snap = midtransclient.Snap(
    is_production=False,  # Sandbox mode
    server_key='SB-Mid-server-GEWrPzhUN6u915Pthmk5n12d',
    client_key='SB-Mid-client-DgT73RW4UTD9dsy7'
)

# File paths for Excel files
PRODUCTS_FILE = 'Data/Database Product.2csv.csv'
SALES_FILE = 'Data/sales.xlsx'

# Initialize sales Excel file if it doesn't exist
def init_sales_file():
    if not os.path.exists('Data'):
        os.makedirs('Data')
        
    if not os.path.exists(SALES_FILE):
        sales_df = pd.DataFrame(columns=[
            'transactionID', 
            'customerID', 
            'product_list', 
            'total_price', 
            'transaction_date'
        ])
        sales_df.to_excel(SALES_FILE, index=False)

# Load product database from CSV
def load_products():
    try:
        df = pd.read_csv(PRODUCTS_FILE)
        df.columns = df.columns.str.strip()
        
        # If stock column doesn't exist, add it with default value 100
        if 'stock' not in df.columns:
            df['stock'] = 100
            df.to_csv(PRODUCTS_FILE, index=False)
            
        return df
    except Exception as e:
        print(f"Error loading products file: {e}")
        # Create an empty dataframe with required columns if file doesn't exist
        df = pd.DataFrame(columns=['KODE_BARCODE', 'NAMA', 'KATEGORI', 'HARGA', 'stock'])
        df.to_csv(PRODUCTS_FILE, index=False)
        return df

# Global variables
scanned_products = {}
temp_transaction_items = {}  # Thread-safe storage for transaction items
camera = None
camera_active = False
camera_lock = threading.Lock()
latest_product = None
last_barcode = None
last_detected_time = 0
delay_time = 3

def cari_produk(barcode):
    products_df = load_products()
    try:
        barcode = float(barcode)
        product = products_df[products_df['KODE_BARCODE'] == barcode]
        
        if not product.empty and product['stock'].iloc[0] > 0:  # Check stock
            name = product['NAMA'].iloc[0]
            category = product['KATEGORI'].iloc[0]
            price_str = product['HARGA'].iloc[0]
            stock = product['stock'].iloc[0]
            
            price = int(price_str.replace('Rp', '').replace('.', '').strip())
            return {'name': name, 'category': category, 'price': price, 'stock': stock}
    except ValueError:
        pass
    return None

def scan_barcode():
    global scanned_products, camera, camera_active, last_detected_time, latest_product, last_barcode, temp_transaction_items
    with camera_lock:
        if camera is None or not camera.isOpened():
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                print("Error: Cannot open camera.")
                camera_active = False
                return
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while camera_active:
        ret, frame = camera.read()
        if not ret:
            continue
        barcodes = decode(frame)
        current_time = time.time()

        for code in barcodes:
            barcode_data = code.data.decode('utf-8')
            if barcode_data == last_barcode and (current_time - last_detected_time < delay_time):
                continue

            produk = cari_produk(barcode_data)
            if produk:
                with camera_lock:
                    latest_product = produk
                    if produk['name'] in scanned_products:
                        if scanned_products[produk['name']]['quantity'] < produk['stock']:
                            scanned_products[produk['name']]['quantity'] += 1
                    else:
                        scanned_products[produk['name']] = {
                            'price': produk['price'],
                            'quantity': 1,
                            'category': produk['category']
                        }
                    scanned_products[produk['name']]['total_price'] = (
                        scanned_products[produk['name']]['price'] * scanned_products[produk['name']]['quantity']
                    )
                    
                    # Store in thread-safe dict instead of directly in session
                    temp_transaction_items[produk['name']] = {
                        'item_id': str(hash(produk['name']) % 100000),
                        'price': produk['price'],
                        'quantity': scanned_products[produk['name']]['quantity'],
                        'total_price': scanned_products[produk['name']]['total_price']
                    }
                    
                last_barcode = barcode_data
                last_detected_time = current_time
        time.sleep(0.1)

def gen_frames():
    global camera, camera_active, latest_product
    with camera_lock:
        if camera is None or not camera.isOpened():
            return
    while camera_active:
        ret, frame = camera.read()
        if not ret:
            break
        if latest_product:
            text = f"Name: {latest_product['name']} | Price: Rp{latest_product['price']:,}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_hash_code(text):
    import hashlib
    return abs(int(hashlib.md5(text.encode()).hexdigest(), 16) % (10 ** 10))

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/cart')
def cart():
    # Update the session with any items from the temp_transaction_items
    global temp_transaction_items
    if 'transaction' in session and temp_transaction_items:
        session['transaction']['items'].update(temp_transaction_items)
        temp_transaction_items = {}  # Clear the temp items
        session.modified = True
    
    transaction = session.get('transaction', {
        'transaction_id': '', 'customer_id': '', 'transaction_date': '', 'items': {}
    })
    total_amount = sum(item['total_price'] for item in scanned_products.values()) if scanned_products else 0
    return render_template('cart.html', transaction=transaction, products=scanned_products, total_amount=total_amount)

@app.route('/payment')
def payment():
    transaction = session.get('transaction', None)
    if not transaction or not transaction.get('products'):
        return redirect(url_for('cart'))
    
    # Calculate total amount
    total_amount = sum(item['total_price'] for item in transaction['products'])
    
    return render_template('payment.html', 
                         transaction=transaction,
                         total_amount=total_amount,
                         midtrans_client_key=MIDTRANS_CLIENT_KEY)

@app.route('/initiate_payment', methods=['POST'])
def initiate_payment():
    transaction = session.get('transaction', None)
    if not transaction or not transaction.get('products'):
        return jsonify({'error': 'No transaction data'}), 400

    total_amount = sum(item['total_price'] for item in transaction['products'])
    
    # Prepare item details for Midtrans
    item_details = [
        {
            'id': item['item_id'],
            'price': item['price'],
            'quantity': item['quantity'],
            'name': name
        }
        for name, item in session['transaction']['items'].items()
    ]

    # Create transaction details
    transaction_details = {
        'order_id': f"ORDER-{transaction['transaction_id']}-{uuid.uuid4().hex[:8]}",
        'gross_amount': total_amount
    }

    # Customer details
    customer_details = {
        'first_name': transaction['customer_id'],
        'email': f"customer-{transaction['customer_id']}@example.com"  # Placeholder email
    }

    # Create Snap transaction
    try:
        snap_response = snap.create_transaction({
            'transaction_details': transaction_details,
            'item_details': item_details,
            'customer_details': customer_details,
            'enabled_payments': ['credit_card', 'gopay', 'shopeepay', 'bank_transfer']
        })
        snap_token = snap_response['token']
        return jsonify({'snap_token': snap_token})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/receipt', methods=['GET', 'POST'])
def receipt():
    if 'transaction' not in session or not scanned_products:
        return redirect(url_for('cart'))
    
    transaction = session['transaction']
    receipt_id = generate_receipt_id()
    total = sum(item['total_price'] for item in transaction['products'])
    
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            send_receipt(email, receipt_id, transaction, total)
    
    return render_template('receipt.html', 
                          receipt_id=receipt_id, 
                          cart=transaction['products'], 
                          total=total, 
                          date=transaction['transaction_date'],
                          transaction=transaction)

@app.route('/thankyou')
def thankyou():
    global scanned_products
    if 'transaction' in session:
        save_to_sales_excel(session['transaction']['transaction_id'], session['transaction']['customer_id'],
                         session['transaction']['products'], sum(item['total_price'] for item in session['transaction']['products']))
        update_stock_excel(scanned_products)
        session.pop('transaction')
        scanned_products = {}
    return render_template('thankyou.html')

@app.route('/start_scan')
def start_scan():
    global camera_active, temp_transaction_items
    if not camera_active:
        camera_active = True
        if 'transaction' not in session:
            transaction_id, customer_id, transaction_date = generate_transaction_details()
            session['transaction'] = {
                'transaction_id': transaction_id,
                'customer_id': customer_id,
                'transaction_date': transaction_date,
                'items': {},
                'products': []  # Initialize products as a list
            }
        
        # Clear the temporary transaction items dict
        temp_transaction_items = {}
        
        threading.Thread(target=scan_barcode, daemon=True).start()
        return jsonify({"status": "scanning"})
    return jsonify({"status": "already_scanning"})

@app.route('/video_feed')
def video_feed():
    if not camera_active:
        return jsonify({"error": "Camera not active"}), 400
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cart_data')
def cart_data():
    # Update session with any new scanned items
    global temp_transaction_items
    if 'transaction' in session and temp_transaction_items:
        session['transaction']['items'].update(temp_transaction_items)
        temp_transaction_items = {}
        session.modified = True
    
    with camera_lock:
        return jsonify(scanned_products)

@app.route('/stop_scan')
def stop_scan():
    global camera, camera_active
    with camera_lock:
        camera_active = False
        if camera and camera.isOpened():
            camera.release()
            camera = None
    return jsonify({"status": "stopped"})

@app.route('/remove_item/<name>', methods=['POST'])
def remove_item(name):
    global scanned_products, temp_transaction_items
    with camera_lock:
        if name in scanned_products:
            del scanned_products[name]
            if name in temp_transaction_items:
                del temp_transaction_items[name]
            if 'transaction' in session and name in session['transaction']['items']:
                del session['transaction']['items'][name]
                session.modified = True
            
            # Update products list if it exists
            if 'transaction' in session and 'products' in session['transaction']:
                session['transaction']['products'] = [
                    item for item in session['transaction']['products']
                    if item['name'] != name
                ]
                session.modified = True
                
            return jsonify({"status": "item_removed"})
        return jsonify({"status": "item_not_found"}), 404

@app.route('/update_cart')
def update_cart():
    """Endpoint to sync temporary items with session"""
    global temp_transaction_items
    if 'transaction' in session and temp_transaction_items:
        session['transaction']['items'].update(temp_transaction_items)
        temp_transaction_items = {}
        session.modified = True
    return jsonify({"status": "cart_updated"})

@app.route('/checkout')
def checkout():
    global scanned_products, temp_transaction_items
    
    # Make sure to sync any pending items
    if 'transaction' in session and temp_transaction_items:
        session['transaction']['items'].update(temp_transaction_items)
        temp_transaction_items = {}
        session.modified = True
    
    if not scanned_products:
        return redirect(url_for('cart'))
    
    transaction_id, customer_id, transaction_date = generate_transaction_details()
    
    # Create products list for session
    products = []
    for name, item in scanned_products.items():
        products.append({
            'item_id': str(hash(name) % 100000),
            'name': name,
            'price': item['price'],
            'quantity': item['quantity'],
            'total_price': item['total_price']
        })
    
    session['transaction'] = {
        'transaction_id': transaction_id,
        'customer_id': customer_id,
        'transaction_date': transaction_date,
        'items': session.get('transaction', {}).get('items', {}),
        'products': products
    }
    
    return redirect(url_for('payment'))

def generate_transaction_details():
    today_date = datetime.now().strftime('%Y%m%d')
    
    try:
        sales_df = pd.read_excel(SALES_FILE)
        transaction_count = len(sales_df[sales_df['transactionID'].str.contains(today_date, na=False)]) + 1
    except (FileNotFoundError, pd.errors.EmptyDataError):
        transaction_count = 1
    
    customer_count = transaction_count
    transaction_id = f"{today_date}-{transaction_count:04d}"
    customer_id = f"CUST-{today_date}-{customer_count:03d}"
    transaction_date = datetime.now().strftime('%Y-%m-%d')
    
    return transaction_id, customer_id, transaction_date

def generate_receipt_id():
    today = datetime.now().strftime("%Y%m%d")
    
    try:
        sales_df = pd.read_excel(SALES_FILE)
        counter = len(sales_df[sales_df['transactionID'].str.contains(today, na=False)]) + 1
    except (FileNotFoundError, pd.errors.EmptyDataError):
        counter = 1
    
    return f"RCT-{today}-{counter:04d}"

def save_to_sales_excel(transaction_id, customer_id, products, total):
    # Initialize sales file if it doesn't exist
    init_sales_file()
    
    try:
        sales_df = pd.read_excel(SALES_FILE)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        sales_df = pd.DataFrame(columns=['transactionID', 'customerID', 'product_list', 'total_price', 'transaction_date'])
    
    # Add new transaction
    new_row = {
        'transactionID': transaction_id,
        'customerID': customer_id,
        'product_list': str(products),
        'total_price': total,
        'transaction_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    sales_df = pd.concat([sales_df, pd.DataFrame([new_row])], ignore_index=True)
    sales_df.to_excel(SALES_FILE, index=False)

def update_stock_excel(products):
    products_df = load_products()
    
    for product_name, details in products.items():
        # Find the product in the DataFrame
        mask = products_df['NAMA'] == product_name
        if mask.any():
            # Update stock
            products_df.loc[mask, 'stock'] = products_df.loc[mask, 'stock'] - details['quantity']
    
    # Save the updated DataFrame
    products_df.to_csv(PRODUCTS_FILE, index=False)

def send_receipt(email, receipt_id, transaction, total):
    sender_email = "your_email@gmail.com"  # Ganti dengan email Anda
    password = "your_app_password"         # Gunakan app password, bukan password biasa

    msg = MIMEMultipart("alternative")
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Your E-Receipt (Anjungan Check Out Mandiri)"

    body = f"Receipt ID: {receipt_id}\nTransaction ID: {transaction['transaction_id']}\nCustomer ID: {transaction['customer_id']}\nDate: {transaction['transaction_date']}\n\nItems:\n"
    for item in transaction['products']:
        body += f"- {item['name']}: {item['quantity']} x Rp{item['price']:,} = Rp{item['total_price']:,}\n"
    body += f"\nTotal: Rp{total:,}"

    html_body = f"""
    <html>
    <body>
        <h2>Your E-Receipt</h2>
        <p><strong>Receipt ID:</strong> {receipt_id}</p>
        <p><strong>Transaction ID:</strong> {transaction['transaction_id']}</p>
        <p><strong>Customer ID:</strong> {transaction['customer_id']}</p>
        <p><strong>Date:</strong> {transaction['transaction_date']}</p>
        <h3>Items:</h3>
        <ul>
    """
    for item in transaction['products']:
        html_body += f"<li>{item['name']}: {item['quantity']} x Rp{item['price']:,} = Rp{item['total_price']:,}</li>"
    html_body += f"""
        </ul>
        <h3>Total: Rp{total:,}</h3>
        <p>Thank you for shopping with us!</p>
    </body>
    </html>
    """

    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)

# Add a periodic background task to sync session data
@app.before_request
def before_request():
    global temp_transaction_items
    if 'transaction' in session and temp_transaction_items:
        session['transaction']['items'].update(temp_transaction_items)
        temp_transaction_items = {}
        session.modified = True

if __name__ == "__main__":
    init_sales_file()
    try:
        app.run(debug=True, threaded=True)
    finally:
        if camera and camera.isOpened():
            camera.release()