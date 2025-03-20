from flask import Flask, render_template, Response, jsonify
import cv2
from pyzbar.pyzbar import decode
import threading
import time
import pandas as pd

app = Flask(__name__)

# Load product database
file_path = 'Database Product.2csv.csv'
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# Global variables
scanned_products = {}
camera = None
camera_active = False
camera_lock = threading.Lock()
latest_product = None  # To store the latest scanned product info
last_barcode = None    # To track the last scanned barcode
last_detected_time = 0

# Delay for duplicate scans
delay_time = 3

def cari_produk(barcode):
    try:
        barcode = float(barcode)
        hasil = df[df['KODE_BARCODE'] == barcode]
        if not hasil.empty:
            produk = hasil.iloc[0]
            return {
                'name': produk['NAMA'],
                'category': produk['KATEGORI'],
                'price': int(produk['HARGA'].replace('Rp', '').replace('.', '').strip())
            }
    except ValueError:
        pass
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

    print("Starting barcode scanning...")
    while camera_active:
        ret, frame = camera.read()
        if not ret:
            print("Failed to read frame from camera.")
            continue

        barcodes = decode(frame)
        current_time = time.time()

        for code in barcodes:
            barcode_data = code.data.decode('utf-8')

            # Check if this is a new barcode or enough time has passed since the last scan
            if barcode_data == last_barcode and (current_time - last_detected_time < delay_time):
                continue  # Skip if it's the same barcode within the delay period

            produk = cari_produk(barcode_data)
            if produk:
                with camera_lock:
                    latest_product = produk  # Store the latest scanned product
                    if produk['name'] in scanned_products:
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

                    print(f"Scanned: {produk['name']} - {produk['category']} - Rp{produk['price']:,} "
                          f"(Qty: {scanned_products[produk['name']]['quantity']}, Total: Rp{scanned_products[produk['name']]['total_price']:,})")

                # Update the last scanned barcode and time
                last_barcode = barcode_data
                last_detected_time = current_time

        time.sleep(0.1)  # Small delay to prevent overwhelming the loop

def gen_frames():
    global camera, camera_active, latest_product

    with camera_lock:
        if camera is None or not camera.isOpened():
            print("Camera is not initialized.")
            return

    while camera_active:
        ret, frame = camera.read()
        if not ret:
            print("Failed to generate frame.")
            break

        # Overlay product info on the frame if a product was recently scanned
        if latest_product:
            text = f"Name: {latest_product['name']} | Category: {latest_product['category']} | Price: Rp{latest_product['price']:,}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Failed to encode frame.")
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/receipt')
def receipt():
    return render_template('receipt.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/start_scan')
def start_scan():
    global camera_active, camera
    if not camera_active:
        camera_active = True
        print("Starting scanning thread...")
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
            print("Camera released.")
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    try:
        app.run(debug=True, threaded=True)
    finally:
        if camera and camera.isOpened():
            camera.release()
            print("Camera released on exit.")