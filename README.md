# Flask Self-Checkout System with Barcode Scanner & Midtrans

Proyek ini adalah aplikasi web berbasis Flask yang mensimulasikan sistem kasir mandiri (self-checkout). Aplikasi ini memungkinkan pengguna untuk memindai barcode produk menggunakan webcam, menambahkan item ke keranjang belanja virtual, dan melanjutkan ke proses pembayaran (simulasi) menggunakan Midtrans (mode Sandbox). Aplikasi juga mencatat penjualan dan mengelola stok produk sederhana.

## Fitur Utama

*   **Pemindaian Barcode**: Menggunakan webcam untuk memindai barcode produk secara real-time (menggunakan OpenCV dan Pyzbar).
*   **Manajemen Produk**: Memuat data produk (nama, kategori, harga, stok) dari file CSV.
*   **Manajemen Stok**: Stok produk akan berkurang setelah transaksi berhasil. Jika stok produk habis, produk tidak dapat ditambahkan.
*   **Keranjang Belanja**: Menampilkan produk yang dipindai, kuantitas, dan total harga. Pengguna dapat menghapus item dari keranjang.
*   **Integrasi Pembayaran Midtrans**: Terintegrasi dengan Midtrans Snap API (mode Sandbox) untuk simulasi proses pembayaran.
*   **Pencatatan Penjualan**: Menyimpan detail setiap transaksi ke dalam file Excel (`sales.xlsx`).
*   **Struk Elektronik**: Membuat struk setelah pembayaran dan memberikan opsi untuk mengirimkannya melalui email.
*   **Antarmuka Web**: Dibuat menggunakan Flask dan template HTML.

## Teknologi yang Digunakan

*   **Backend**: Python, Flask
*   **Pemrosesan Gambar**: OpenCV (`cv2`), Pyzbar
*   **Manipulasi Data**: Pandas
*   **Pembayaran**: Midtrans Python Client (`midtransclient`)
*   **Email**: `smtplib`, `email.mime`
*   **Frontend**: HTML (menggunakan template Jinja2 Flask)

## Prasyarat

*   Python 3.7+
*   pip (Python package installer)
*   Webcam yang berfungsi
*   Akun Midtrans Sandbox (untuk mendapatkan Client Key dan Server Key)
*   Akun Gmail (dengan "App Password" diaktifkan jika menggunakan Gmail untuk mengirim email struk)

## Instalasi & Setup

1.  **Clone repository**
    ```bash
    # git clone https://github.com/delima1234-Sunbright/Anjungan-Check-Out-Mandiri
    # cd [NAMA_DIREKTORI_PROYEK]
    ```

2.  **Buat dan aktifkan virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

4.  **Konfigurasi Kunci Midtrans:**
    Buka file `app.py` dan ganti placeholder kunci Midtrans dengan kunci Sandbox:
    ```python
    MIDTRANS_CLIENT_KEY = 'SB-Mid-client-ANDA'  # Ganti dengan Client Key Sandbox 
    MIDTRANS_SERVER_KEY = 'SB-Mid-server-ANDA'  # Ganti dengan Server Key Sandbox 

    # Dan juga di inisialisasi Snap:
    snap = midtransclient.Snap(
        is_production=False,
        server_key='SB-Mid-server-ANDA', 
        client_key='SB-Mid-client-ANDA'  
    )
    ```

## Menjalankan Aplikasi

1.  Pastikan virtual environment Anda aktif.
2.  Jalankan aplikasi Flask:
    ```bash
    python Selfcheckout.py
    ```
3.  Buka browser Anda dan akses `http://127.0.0.1:5000/`.

## Alur Kerja Aplikasi

1.  **Halaman Selamat Datang**: Pengguna akan disambut di halaman utama.
2.  **Mulai Pindai**: Pengguna mengklik tombol untuk memulai pemindaian. Kamera akan aktif.
3.  **Pemindaian Produk**: Arahkan barcode produk ke webcam. Jika produk dikenali dan stok tersedia, produk akan ditambahkan ke keranjang.
4.  **Keranjang Belanja (`/cart`)**: Menampilkan daftar produk yang dipindai, kuantitas, dan harga. Pengguna dapat menghapus item atau melanjutkan ke pembayaran.
5.  **Halaman Pembayaran (`/payment`)**: Menampilkan ringkasan pesanan dan tombol untuk melanjutkan ke pembayaran Midtrans.
6.  **Proses Pembayaran Midtrans**: Pengguna akan diarahkan ke antarmuka Midtrans Snap untuk menyelesaikan pembayaran (simulasi di Sandbox).
7.  **Halaman Terima Kasih (`/thankyou`)**: Setelah pembayaran (disimulasikan berhasil atau kembali dari Midtrans), pengguna akan diarahkan ke halaman terima kasih. Pada tahap ini, data penjualan disimpan dan stok diperbarui.
8.  **Struk (`/receipt`)**: Pengguna dapat melihat struk transaksi dan memasukkan email untuk menerima struk elektronik.

## Struktur File (Penting)

```
.
├── app.py                  # File utama aplikasi Flask
├── Data/
│   ├── Database Product.2csv.csv  # Database produk (harus buat barcode manual)
│   └── sales.xlsx            # Catatan penjualan 
├── templates/              # Direktori untuk file HTML
│   ├── welcome.html
│   ├── cart.html
│   ├── payment.html
│   ├── receipt.html
│   └── thankyou.html
└── README.md               # File ini
```
