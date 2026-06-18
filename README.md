# LiteraStore

LiteraStore adalah aplikasi desktop manajemen toko buku berbasis PySide6 dan SQLite. Aplikasi ini menyediakan fitur untuk penjual dalam mengelola katalog buku, memproses transaksi kasir, melihat ringkasan penjualan, serta mengekspor laporan. Aplikasi juga menyediakan mode pembeli untuk melihat etalase, mengelola keranjang, checkout, dan melihat riwayat transaksi.

## Anggota Kelompok

1. Datu Reksa Hamza Putra - F1D02310045
2. Nabila Zahirani - F1D02310019
3. Rosida Asri Ardiani - F1D02410142

## Fitur Utama

- Login berbasis role Penjual dan Pembeli.
- Dashboard penjual berisi total buku, total stok, pendapatan, jumlah transaksi, buku terlaris, dan stok menipis.
- Manajemen buku dengan tambah, tampil, edit, hapus, search, filter kategori, dan sorting.
- Transaksi kasir menggunakan dialog input, validasi jumlah, validasi stok, dan pencatatan otomatis ke database.
- Export laporan penjualan ke CSV dan PDF.
- Etalase pembeli dengan pencarian buku, detail sinopsis, keranjang belanja, checkout, dan riwayat transaksi.
- Penyimpanan data menggunakan SQLite.
- Styling aplikasi menggunakan file QSS dan style PySide6.

## Struktur Proyek

```text
.
├── main.py
├── requirements.txt
├── run.ps1
├── assets/
│   ├── books_blur.svg
│   └── styles.qss
├── database/
│   └── database.db
├── models/
│   └── database_manager.py
├── utils/
│   └── exporters.py
└── views/
    ├── buku_view.py
    ├── dashboard_pembeli_view.py
    ├── dashboard_view.py
    ├── login_view.py
    └── transaksi_view.py
```

## Instalasi

Pastikan Python sudah terpasang, lalu jalankan:

```powershell
cd "c:/Final Project/pv26-finalproject-LiteraStore"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Jika memakai virtual environment yang sudah tersedia di proyek, cukup jalankan instalasi dependensi:

```powershell
.\.venv\Scripts\pip.exe install -r requirements.txt
```

## Menjalankan Aplikasi

Menggunakan script PowerShell:

```powershell
.\run.ps1
```

Atau manual:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Akun Demo

| Role | Username | Password |
| --- | --- | --- |
| Penjual | penjual | 12345 |
| Pembeli | pembeli | 12345 |
| Pembeli | nabila | 12345 |

## Pembagian Tugas

| Anggota | Kontribusi |
| --- | --- |
| Datu Reksa Hamza Putra | Struktur aplikasi, database, dashboard, dan integrasi halaman utama. |
| Nabila Zahirani | Tampilan pembeli, etalase buku, keranjang, checkout, dan riwayat transaksi. |
| Rosida Asri Ardiani | Manajemen buku, transaksi kasir, validasi input, export laporan, dan styling. |

## Catatan

- Database akan dibuat dan diisi data awal otomatis saat aplikasi pertama kali dijalankan.
- Export PDF membutuhkan package `reportlab` yang sudah tercantum di `requirements.txt`.
- Jika PowerShell menolak menjalankan script, gunakan perintah manual dengan interpreter dari `.venv`.
