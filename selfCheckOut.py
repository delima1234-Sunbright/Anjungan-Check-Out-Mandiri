from flask import Flask, render_template, Response, jsonify, redirect, url_for, session, request
import cv2
from pyzbar.pyzbar import decode
import threading
import time
import pandas as pd
from datetime import datetime
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'Delimabrpurba7225'

# Inisialisasi database SQLite
def init_db():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sales (
                    transactionID TEXT PRIMARY KEY,
                    customerID TEXT,
                    product_list TEXT,
                    total_price INTEGER,
                    transaction_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    KODE_BARCODE INTEGER PRIMARY KEY,
                    NAMA TEXT,
                    KATEGORI TEXT,
                    HARGA TEXT,
                    stock INTEGER)''')
    conn.commit()
    conn.close()

# Load product database dari CSV dan masukkan ke SQLite jika belum ada
file_path = 'Data\Database Product.2csv.csv'
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

def populate_products_db():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    for _, row in df.iterrows():
        c.execute('''INSERT OR IGNORE INTO products (KODE_BARCODE, NAMA, KATEGORI, HARGA, stock)
                     VALUES (?, ?, ?, ?, ?)''',
                  (row['KODE_BARCODE'], row['NAMA'], row['KATEGORI'], row['HARGA'], 100))  # Stok awal 100
    conn.commit()
    conn.close()

# Global variables
scanned_products = {}
camera = None
camera_active = False
camera_lock = threading.Lock()
latest_product = None
last_barcode = None
last_detected_time = 0
delay_time = 3

def cari_produk(barcode):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    try:
        barcode = float(barcode)
        c.execute("SELECT NAMA, KATEGORI, HARGA, stock FROM products WHERE KODE_BARCODE = ?", (barcode,))
        result = c.fetchone()
        if result and result[3] > 0:  # Cek stok
            name, category, price_str, stock = result
            price = int(price_str.replace('Rp', '').replace('.', '').strip())
            return {'name': name, 'category': category, 'price': price, 'stock': stock}
    except ValueError:
        pass
    finally:
        conn.close()
    return None

def scan_barcode():
    global scanned_products, camera, camera_active, last_detected_time, latest_product, last_barcode
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
                    session['transaction']['items'][produk['name']] = {
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
    transaction = session.get('transaction', {
        'transaction_id': '', 'customer_id': '', 'transaction_date': '', 'items': {}
    })
    total_amount = sum(item['total_price'] for item in scanned_products.values()) if scanned_products else 0
    return render_template('cart.html', transaction=transaction, products=scanned_products, total_amount=total_amount)

@app.route('/payment')
def payment():
    transaction = session.get('transaction', None)
    if not transaction or 'products' not in transaction:  # Change to 'products'
        return redirect(url_for('cart'))
        
    # Calculate total amount
    total_amount = sum(item['total_price'] for item in transaction['products'])
    
    return render_template('payment.html', 
                         transaction=transaction,
                         total_amount=total_amount)

@app.route('/receipt', methods=['GET', 'POST'])
def receipt():
    if 'transaction' not in session or not scanned_products:
        return redirect(url_for('cart'))
    
    transaction = session['transaction']  # Get the transaction from session
    receipt_id = generate_receipt_id()
    total = sum(item['total_price'] for item in transaction['products'])
    
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            send_receipt(email, receipt_id, transaction, total)
    
    # Pass transaction to the template
    return render_template('receipt.html', 
                          receipt_id=receipt_id, 
                          cart=transaction['products'], 
                          total=total, 
                          date=transaction['transaction_date'],
                          transaction=transaction)  # Add this line

@app.route('/thankyou')
def thankyou():
    global scanned_products
    if 'transaction' in session:
        save_to_sales_db(session['transaction']['transaction_id'], session['transaction']['customer_id'],
                         session['transaction']['products'], sum(item['total_price'] for item in session['transaction']['products']))
        update_stock(scanned_products)
        session.pop('transaction')
        scanned_products = {}
    return render_template('thankyou.html')

@app.route('/start_scan')
def start_scan():
    global camera_active
    if not camera_active:
        camera_active = True
        if 'transaction' not in session:
            transaction_id, customer_id, transaction_date = generate_transaction_details()
            session['transaction'] = {
                'transaction_id': transaction_id,
                'customer_id': customer_id,
                'transaction_date': transaction_date,
                'items': {}
            }
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
    global scanned_products
    with camera_lock:
        if name in scanned_products:
            del scanned_products[name]
            if name in session['transaction']['items']:
                del session['transaction']['items'][name]
            return jsonify({"status": "item_removed"})
        return jsonify({"status": "item_not_found"}), 404

@app.route('/checkout')
def checkout():
    global scanned_products

    if not scanned_products:
        return redirect(url_for('cart'))
    
    transaction_id, customer_id, transaction_date = generate_transaction_details()
    
    # Create a new dictionary for the session using 'products' instead of 'items'
    session['transaction'] = {
        'transaction_id': transaction_id,
        'customer_id': customer_id,
        'transaction_date': transaction_date,
        'products': []  # Use 'products' instead of 'items'
    }
    
    # Add items to the list
    for name, item in scanned_products.items():
        session['transaction']['products'].append({
            'name': name,
            'price': item['price'],
            'quantity': item['quantity'],
            'total_price': item['price'] * item['quantity'],
            'category': item['category'],
            'item_id': hash(name) % 10000000  # Simple hash for ID
        })

    return redirect(url_for('payment'))

def generate_transaction_details():
    today_date = datetime.now().strftime('%Y%m%d')
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sales WHERE transactionID LIKE ?", (f"{today_date}%",))
    transaction_count = c.fetchone()[0] + 1
    customer_count = transaction_count
    transaction_id = f"{today_date}-{transaction_count:04d}"
    customer_id = f"CUST-{today_date}-{customer_count:03d}"
    transaction_date = datetime.now().strftime('%Y-%m-%d')
    conn.close()
    return transaction_id, customer_id, transaction_date

def generate_receipt_id():
    today = datetime.now().strftime("%Y%m%d")
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sales WHERE transactionID LIKE ?", (f"{today}%",))
    counter = c.fetchone()[0] + 1
    conn.close()
    return f"RCT-{today}-{counter:04d}"

def save_to_sales_db(transaction_id, customer_id, products, total):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute('''INSERT INTO sales (transactionID, customerID, product_list, total_price, transaction_date)
                 VALUES (?, ?, ?, ?, ?)''',
              (transaction_id, customer_id, str(products), total, datetime.now().strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()

def update_stock(products):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    for product_name, details in products.items():
        c.execute('''UPDATE products SET stock = stock - ? WHERE NAMA = ?''',
                  (details['quantity'], product_name))
    conn.commit()
    conn.close()

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


if __name__ == "__main__":
    init_db()
    populate_products_db()
    try:
        app.run(debug=True, threaded=True)
    finally:
        if camera and camera.isOpened():
            camera.release()