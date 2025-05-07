from flask import Flask, render_template, Response, jsonify, redirect, url_for, session, request
import cv2
from pyzbar.pyzbar import decode
import threading
import time
import pandas as pd
from datetime import datetime
import sqlite3
import midtransclient
import uuid
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'Delimabrpurba7225'

# Midtrans Configuration (Sandbox)
MIDTRANS_CLIENT_KEY = 'SB-Mid-client-DgT73RW4UTD9dsy7'
MIDTRANS_SERVER_KEY = 'SB-Mid-server-GEWrPzhUN6u915Pthmk5n12d'

# Initialize Midtrans Snap API Client
snap = midtransclient.Snap(
    is_production=False,
    server_key=MIDTRANS_SERVER_KEY,
    client_key=MIDTRANS_CLIENT_KEY
)

# CSV File path for products
PRODUCTS_CSV_PATH = 'Data/Database Product.2csv.csv'

# Load product database from CSV
try:
    df = pd.read_csv(PRODUCTS_CSV_PATH)
    df.columns = df.columns.str.strip()
except Exception as e:
    logging.error(f"Error loading product database: {e}")
    df = pd.DataFrame(columns=['KODE_BARCODE', 'NAMA', 'KATEGORI', 'HARGA'])

# Initialize SQLite database
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

# Populate products table from CSV
def populate_products_db():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    for _, row in df.iterrows():
        c.execute('''INSERT OR IGNORE INTO products (KODE_BARCODE, NAMA, KATEGORI, HARGA, stock)
                    VALUES (?, ?, ?, ?, ?)''',
                (row['KODE_BARCODE'], row['NAMA'], row['KATEGORI'], row['HARGA'], 100))
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
        if result and result[3] > 0:
            name, category, price_str, stock = result
            price = int(price_str.replace('Rp', '').replace('.', '').strip())
            logging.info(f"Product found: {name} for barcode: {barcode}")
            return {'name': name, 'category': category, 'price': price, 'stock': stock}
        else:
            logging.info(f"No product found or stock is 0 for barcode: {barcode}")
    except ValueError:
        logging.error(f"Invalid barcode format: {barcode}")
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
    if not transaction or not transaction.get('products'):
        return redirect(url_for('cart'))
    
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
    
    item_details = [
        {
            'id': item['item_id'],
            'price': item['price'],
            'quantity': item['quantity'],
            'name': name
        }
        for name, item in session['transaction']['items'].items()
    ]

    transaction_details = {
        'order_id': f"ORDER-{transaction['transaction_id']}-{uuid.uuid4().hex[:8]}",
        'gross_amount': total_amount
    }

    customer_details = {
        'first_name': transaction['customer_id'],
        'email': f"customer-{transaction['customer_id']}@example.com"
    }

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
        logging.error(f"Payment initiation error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/receipt', methods=['GET'])
def receipt():
    if 'transaction' not in session or not scanned_products:
        return redirect(url_for('cart'))
    
    transaction = session['transaction']
    receipt_id = generate_receipt_id()
    total = sum(item['total_price'] for item in transaction['products'])
    
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
        total_price = sum(item['total_price'] for item in session['transaction']['products'])
        save_to_sales_db(session['transaction']['transaction_id'], 
                        session['transaction']['customer_id'],
                        session['transaction']['products'], 
                        total_price)
        
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
                'items': {},
                'products': []
            }
        threading.Thread(target=scan_barcode, daemon=True).start()
        logging.info("Scanning started.")
        return jsonify({"status": "scanning"})
    logging.info("Scan already active.")
    return jsonify({"status": "already_scanning"})

@app.route('/video_feed')
def video_feed():
    if not camera_active:
        logging.error("Camera not active for video feed.")
        return jsonify({"error": "Camera not active"}), 400
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cart_data')
def cart_data():
    with camera_lock:
        # Update session with scanned products
        if 'transaction' in session:
            for name, item in scanned_products.items():
                session['transaction']['items'][name] = {
                    'item_id': str(hash(name) % 100000),
                    'price': item['price'],
                    'quantity': item['quantity'],
                    'total_price': item['total_price']
                }
            session.modified = True  # Mark session as modified
        return jsonify(scanned_products)

@app.route('/stop_scan')
def stop_scan():
    global camera, camera_active
    with camera_lock:
        camera_active = False
        if camera and camera.isOpened():
            camera.release()
            camera = None
            logging.info("Camera stopped and released.")
    return jsonify({"status": "stopped"})

@app.route('/remove_item/<name>', methods=['POST'])
def remove_item(name):
    global scanned_products
    with camera_lock:
        if name in scanned_products:
            del scanned_products[name]
            if name in session['transaction']['items']:
                del session['transaction']['items'][name]
            session['transaction']['products'] = [
                item for item in session['transaction']['products']
                if item['name'] != name
            ]
            session.modified = True
            logging.info(f"Removed item: {name}")
            return jsonify({"status": "item_removed"})
        logging.warning(f"Item not found: {name}")
        return jsonify({"status": "item_not_found"}), 404

@app.route('/checkout')
def checkout():
    global scanned_products
    if not scanned_products:
        logging.info("No products in cart, redirecting to cart.")
        return redirect(url_for('cart'))
    
    transaction_id, customer_id, transaction_date = generate_transaction_details()
    
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
    session.modified = True
    logging.info("Checkout initiated.")
    
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
    logging.info(f"Generated transaction details: {transaction_id}, {customer_id}")
    return transaction_id, customer_id, transaction_date

def generate_receipt_id():
    today = datetime.now().strftime("%Y%m%d")
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sales WHERE transactionID LIKE ?", (f"{today}%",))
    counter = c.fetchone()[0] + 1
    conn.close()
    logging.info(f"Generated receipt ID: RCT-{today}-{counter:04d}")
    return f"RCT-{today}-{counter:04d}"

def save_to_sales_db(transaction_id, customer_id, products, total):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute('''INSERT INTO sales (transactionID, customerID, product_list, total_price, transaction_date)
                 VALUES (?, ?, ?, ?, ?)''',
              (transaction_id, customer_id, str(products), total, datetime.now().strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()
    logging.info(f"Saved transaction {transaction_id} to database.")

def update_stock(products):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    for product_name, details in products.items():
        c.execute('''UPDATE products SET stock = stock - ? WHERE NAMA = ?''',
                  (details['quantity'], product_name))
    conn.commit()
    conn.close()
    logging.info("Updated stock in database.")

if __name__ == "__main__":
    init_db()
    populate_products_db()
    try:
        app.run(debug=True, threaded=True)
    finally:
        if camera and camera.isOpened():
            camera.release()
            logging.info("Camera released on shutdown.")