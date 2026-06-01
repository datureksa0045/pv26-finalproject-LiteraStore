import sqlite3
import os

# --- KOREKSI PATH ABSOLUT AGAR TIDAK CRASH DI WINDOWS ---
# Mendapatkan direktori absolut dari file database_manager.py ini berada
CURRENT_DIR = os.path.dirname(os.path.abspath(r"D:\Tugas Kuliah\Semester 6\Pemvis\LiteraStore\database")) # hasil: models/

# Menentukan folder 'database' sejajar dengan folder 'models' (di dalam direktori utama LiteraStore)
BASE_DIR = os.path.dirname(CURRENT_DIR) # hasil: LiteraStore/
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "database.db")

def init_db():
    # Membuat folder 'database' secara aman jika belum ada
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabel Buku
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS buku (
        id_buku INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        penulis TEXT NOT NULL,
        kategori TEXT NOT NULL,
        harga REAL NOT NULL,
        stok INTEGER NOT NULL
    )
    ''')
    
    # 2. Tabel Transaksi
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transaksi (
        id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
        id_buku INTEGER,
        jumlah_jual INTEGER NOT NULL,
        total_harga REAL NOT NULL,
        tanggal_transaksi TEXT NOT NULL,
        FOREIGN KEY (id_buku) REFERENCES buku(id_buku) ON DELETE CASCADE
    )
    ''')
    
    # Seeding data dummy jika kosong
    cursor.execute("SELECT COUNT(*) FROM buku")
    if cursor.fetchone()[0] == 0:
        buku_dummy = [
            ("Laskar Pelangi", "Andrea Hirata", "Fiksi", 95000, 15),
            ("Bumi", "Tere Liye", "Fiksi", 105000, 20),
            ("Clean Code", "Robert C. Martin", "Teknologi", 250000, 5),
            ("Sapiens", "Yuval Noah Harari", "Non-Fiksi", 150000, 8),
            ("Cosmos", "Carl Sagan", "Sains", 135000, 12)
        ]
        cursor.executemany("INSERT INTO buku (judul, penulis, kategori, harga, stok) VALUES (?, ?, ?, ?, ?)", buku_dummy)
        
        cursor.execute("INSERT INTO transaksi (id_buku, jumlah_jual, total_harga, tanggal_transaksi) VALUES (1, 2, 190000, '2026-06-01')")
        cursor.execute("INSERT INTO transaksi (id_buku, jumlah_jual, total_harga, tanggal_transaksi) VALUES (3, 1, 250000, '2026-06-01')")
        
    conn.commit()
    conn.close()

def get_all_buku(search="", kategori="Semua Kategori", sort_by="ID (Asc)"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM buku WHERE (judul LIKE ? OR penulis LIKE ?)"
    params = [f"%{search}%", f"%{search}%"]
    
    if kategori != "Semua Kategori":
        query += " AND kategori = ?"
        params.append(kategori)
        
    order_map = {
        "ID (Asc)": "id_buku ASC",
        "ID (Desc)": "id_buku DESC",
        "Judul (A-Z)": "judul ASC",
        "Harga (Termurah)": "harga ASC",
        "Stok (Tersisa)": "stok ASC"
    }
    query += f" ORDER BY {order_map.get(sort_by, 'id_buku ASC')}"
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

def insert_buku(judul, penulis, kategori, harga, stok):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO buku (judul, penulis, kategori, harga, stok) VALUES (?, ?, ?, ?, ?)", 
                   (judul, penulis, kategori, harga, stok))
    conn.commit()
    conn.close()

def update_buku(id_buku, judul, penulis, kategori, harga, stok):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE buku SET judul=?, penulis=?, kategori=?, harga=?, stok=? WHERE id_buku=?", 
                   (judul, penulis, kategori, harga, stok, id_buku))
    conn.commit()
    conn.close()

def delete_buku(id_buku):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM buku WHERE id_buku=?", (id_buku,))
    conn.commit()
    conn.close()

def get_all_transaksi():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.id_transaksi, b.judul, t.jumlah_jual, t.total_harga, t.tanggal_transaksi 
        FROM transaksi t
        JOIN buku b ON t.id_buku = b.id_buku
        ORDER BY t.id_transaksi DESC
    ''')
    data = cursor.fetchall()
    conn.close()
    return data

def insert_transaksi(id_buku, jumlah_jual, total_harga, tanggal):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE buku SET stok = stok - ? WHERE id_buku = ?", (jumlah_jual, id_buku))
    cursor.execute("INSERT INTO transaksi (id_buku, jumlah_jual, total_harga, tanggal_transaksi) VALUES (?, ?, ?, ?)", 
                   (id_buku, jumlah_jual, total_harga, tanggal))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM buku")
    total_buku = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(stok) FROM buku")
    total_stok = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(total_harga) FROM transaksi")
    total_pendapatan = cursor.fetchone()[0] or 0.0
    conn.close()
    return total_buku, total_stok, total_pendapatan