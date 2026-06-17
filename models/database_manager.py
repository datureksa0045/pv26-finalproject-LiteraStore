import sqlite3
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "database.db")


def _ensure_buku_columns(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(buku)")
    columns = {row[1] for row in cursor.fetchall()}
    if "cover_url" not in columns:
        cursor.execute("ALTER TABLE buku ADD COLUMN cover_url TEXT DEFAULT ''")
    if "sinopsis" not in columns:
        cursor.execute("ALTER TABLE buku ADD COLUMN sinopsis TEXT DEFAULT ''")
    conn.commit()


def _seed_buku_samples():
    return [
        ("Laskar Pelangi", "Andrea Hirata", "Fiksi", 95000, 15, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Kisah perjuangan anak-anak Belitung yang penuh semangat, persahabatan, dan harapan."),
        ("Bumi", "Tere Liye", "Fiksi", 105000, 20, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Petualangan di dunia paralel yang menyentuh tema keluarga, mimpi, dan keberanian."),
        ("Clean Code", "Robert C. Martin", "Teknologi", 250000, 5, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Panduan praktis menulis kode yang bersih, rapi, dan mudah dipelihara."),
        ("Sapiens", "Yuval Noah Harari", "Non-Fiksi", 150000, 8, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Perjalanan manusia dari masa purba hingga modern dalam perspektif sains dan sejarah."),
        ("Cosmos", "Carl Sagan", "Sains", 135000, 12, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Eksplorasi alam semesta yang memadukan ilmu pengetahuan, filosofi, dan keajaiban kosmos."),
        ("Atomic Habits", "James Clear", "Pengembangan Diri", 125000, 18, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Cara membangun kebiasaan baik dengan langkah kecil yang konsisten."),
        ("The Psychology of Money", "Morgan Housel", "Bisnis", 140000, 10, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Pelajaran finansial yang sederhana namun sangat berpengaruh pada keputusan hidup."),
        ("Rich Dad Poor Dad", "Robert Kiyosaki", "Bisnis", 160000, 13, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Kisah dan prinsip dasar tentang bagaimana membangun kekayaan secara cerdas."),
        ("1984", "George Orwell", "Fiksi", 90000, 22, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Dunia distopia yang penuh pengawasan, kontrol, dan ketakutan."),
        ("The Hobbit", "J.R.R. Tolkien", "Fantasi", 110000, 16, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Petualangan epik seorang hobbit yang menemukan keberanian di tengah dunia ajaib."),
        ("Dilan 1990", "Pidi Baiq", "Roman", 85000, 24, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Kisah cinta remaja yang hangat, lugu, dan penuh kenangan."),
        ("Bintang", "Tere Liye", "Fiksi", 98000, 11, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Kisah penuh imajinasi tentang harapan, perjuangan, dan masa depan."),
        ("Educated", "Tara Westover", "Biografi", 165000, 7, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Perjalanan hidup yang menggugah tentang belajar, bertahan, dan menemukan identitas."),
        ("Deep Work", "Cal Newport", "Produktivitas", 130000, 9, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Prinsip fokus dan disiplin untuk menghasilkan karya yang bermutu."),
        ("Manajemen Waktu", "M. Hadi", "Bisnis", 115000, 14, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Panduan sederhana untuk mengatur waktu, prioritas, dan produktivitas."),
        ("A Brief History of Time", "Stephen Hawking", "Sains", 175000, 6, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Penjelasan tentang alam semesta dengan bahasa yang mudah dipahami."),
        ("The Alchemist", "Paulo Coelho", "Filosofi", 120000, 17, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Perjalanan seorang gembala yang menemukan arti hidup dan mimpi."),
        ("Marmut Merah Jambu", "Raditya Dika", "Humor", 80000, 25, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Kisah lucu dan dekat dengan kehidupan sehari-hari yang penuh candaan."),
        ("Pulang", "Tere Liye", "Fiksi", 102000, 19, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Cerita tentang perjalanan pulang, keluarga, dan arti rumah yang sesungguhnya."),
        ("The Art of War", "Sun Tzu", "Strategi", 98000, 12, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Panduan klasik tentang strategi, keputusan, dan kepemimpinan."),
        ("Hujan", "Tere Liye", "Fiksi", 108000, 20, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Kisah penuh ketegangan, misteri, dan harapan di tengah badai."),
        ("The Silent Patient", "Alex Michaelides", "Thriller", 145000, 8, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Misteri psikologis tentang seorang pasien yang bungkam dan kasus yang mengerikan."),
        ("Filosofi Teras", "Henry Manampiring", "Filosofi", 110000, 11, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Pengantar tentang keseimbangan batin, kesadaran, dan hidup yang damai."),
        ("A Mind for Numbers", "Barbara Oakley", "Belajar", 138000, 10, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Teknik belajar yang efektif untuk otak yang ingin berkembang."),
        ("The Power of Habit", "Charles Duhigg", "Pengembangan Diri", 127000, 15, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Mengenal pola kebiasaan yang memengaruhi hidup, kerja, dan tujuan."),
        ("Nanti Kita Cerita Tentang Hari Ini", "Marchella FP", "Roman", 99000, 21, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Cerita persahabatan, tumbuh dewasa, dan momen penting yang tak terlupakan."),
        ("Sang Pemimpi", "Andrea Hirata", "Fiksi", 104000, 18, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Kisah impian dan semangat meraih masa depan dengan penuh harapan."),
        ("How to Win Friends", "Dale Carnegie", "Komunikasi", 95000, 22, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Panduan membangun hubungan baik dan menyenangkan dalam kehidupan sehari-hari."),
        ("Ikigai", "Hector Garcia", "Kesehatan", 132000, 9, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Menemukan alasan untuk bangun pagi dan hidup dengan penuh makna."),
        ("The Hobbit 2", "J.R.R. Tolkien", "Fantasi", 112000, 14, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Petualangan penuh teka-teki, keberanian, dan makna persahabatan."),
        ("Bukan Pixel", "Aisyah", "Novel", 87000, 19, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Cerita tentang dunia modern, harapan, dan pertemanan yang tulus."),
        ("One Piece Vol. 1", "Eiichiro Oda", "Komik", 65000, 25, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Awal petualangan bajak laut yang penuh humor, semangat, dan ambisi."),
        ("Naruto Vol. 1", "Masashi Kishimoto", "Komik", 68000, 26, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Cerita tentang ninja muda yang ingin dikenal dan membuktikan diri."),
        ("Doraemon", "Fujiko F. Fujio", "Komik", 59000, 30, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Petualangan seru bersama robot kucing yang penuh kecerdasan."),
        ("Perahu Kertas", "Dewi Lestari", "Roman", 92000, 18, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Cerita cinta yang hangat, liris, dan penuh pertumbuhan diri."),
        ("Tentang Kamu", "Tere Liye", "Roman", 89000, 20, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Kisah yang menyentuh tentang perasaan, harapan, dan pilihan hati."),
        ("Laut Bercerita", "Leila S. Chudori", "Fiksi", 118000, 10, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Novel sejarah yang kuat, menggugah, dan sarat nilai kemanusiaan."),
        ("Habis Gelap Terbitlah Terang", "R.A. Kartini", "Biografi", 76000, 23, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Jejak perjuangan perempuan Indonesia dalam menuntut pendidikan dan kesetaraan."),
        ("Bumi Manusia", "Pramoedya Ananta Toer", "Sejarah", 135000, 8, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Kisah sejarah yang menegangkan dan penuh perlawanan terhadap ketidakadilan."),
        ("Seni Berpikir Positif", "Dr. Norman Vincent Peale", "Pengembangan Diri", 101000, 13, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Mengajak pembaca melihat sisi baik dalam setiap situasi hidup."),
        ("Never Split the Difference", "Chris Voss", "Bisnis", 155000, 7, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Strategi negosiasi yang tajam, praktis, dan sangat aplikatif."),
        ("Mindset", "Carol S. Dweck", "Psikologi", 129000, 12, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Mengubah cara pandang tentang kemampuan, belajar, dan pertumbuhan."),
        ("The Design of Everyday Things", "Don Norman", "Teknologi", 170000, 6, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Mengenal desain yang baik, fungsional, dan menyenangkan untuk digunakan."),
        ("Start With Why", "Simon Sinek", "Bisnis", 124000, 14, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Menghubungkan tujuan dan motivasi yang membuat orang bertindak."),
        ("Thinking, Fast and Slow", "Daniel Kahneman", "Psikologi", 168000, 5, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Menyelami cara otak bekerja dalam mengambil keputusan sehari-hari."),
        ("The Lean Startup", "Eric Ries", "Bisnis", 148000, 9, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Pendekatan praktis membangun bisnis dengan eksperimen dan inovasi."),
        ("Zero to One", "Peter Thiel", "Bisnis", 152000, 8, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Membangun startup yang benar-benar baru dan berpotensi besar."),
        ("The Subtle Art", "Mark Manson", "Pengembangan Diri", 118000, 10, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Panduan jujur tentang hidup, tanggung jawab, dan mencari makna."),
        ("Seni Hidup Minimalis", "Francesco", "Kesehatan", 108000, 13, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Cara hidup lebih ringan, tenang, dan fokus pada hal yang benar-benar penting."),
        ("Buku Teks Algoritma", "Tim Penulis", "Teknologi", 90000, 18, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Pengantar algoritma dan pemrograman untuk pembelajar pemula."),
        ("Misteri Gunung", "Rian Arifin", "Thriller", 98000, 11, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Perjalanan penuh teka-teki di alam yang gelap dan menegangkan."),
        ("Kisah di Ujung Senja", "Maya Sari", "Roman", 91000, 16, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Cerita tentang penyesalan, harapan, dan cinta yang tak selesai."),
        ("Kumpulan Puisi Rindu", "Dina Putri", "Puisi", 77000, 24, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80", "Puisi yang lembut, puitis, dan penuh perasaan tentang cinta dan rindu."),
        ("Lima Menit", "Ari Kurniawan", "Inspirasi", 86000, 17, "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80", "Kisah sederhana tentang perubahan kecil yang mengubah hidup."),
        ("Kisah Kota", "Rizki Ananda", "Fiksi", 94000, 15, "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?auto=format&fit=crop&w=600&q=80", "Perjalanan kota yang penuh warna, suara, dan harapan masa depan."),
        ("Kupu-Kupu Malam", "Ayu Pratiwi", "Fiksi", 103000, 12, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80", "Novel yang membawa pembaca ke dunia imajinasi dan misteri yang menawan.")
    ]


def init_db():
    
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
        id_user INTEGER,
        id_buku INTEGER,
        jumlah_jual INTEGER NOT NULL,
        total_harga REAL NOT NULL,
        tanggal_transaksi TEXT NOT NULL,
        FOREIGN KEY (id_buku) REFERENCES buku(id_buku) ON DELETE CASCADE
    )
    ''')

    # migrate transaksi: tambahkan kolom id_user kalau database lama belum punya
    cursor.execute("PRAGMA table_info(transaksi)")
    cols = {row[1] for row in cursor.fetchall()}
    if "id_user" not in cols:
        cursor.execute("ALTER TABLE transaksi ADD COLUMN id_user INTEGER")
        conn.commit()
    # 3. Tabel User untuk login
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('Penjual', 'Pembeli'))
    )
    ''')
    
    _ensure_buku_columns(conn)
    _ensure_keranjang_table(conn)


    # Seeding data buku agar tersedia minimal 50 judul di etalase pembeli
    cursor.execute("SELECT COUNT(*) FROM buku")
    existing_count = cursor.fetchone()[0]
    buku_dummy = _seed_buku_samples()
    if existing_count == 0:
        cursor.executemany("INSERT INTO buku (judul, penulis, kategori, harga, stok, cover_url, sinopsis) VALUES (?, ?, ?, ?, ?, ?, ?)", buku_dummy[:50])
    elif existing_count < 50:
        for item in buku_dummy[existing_count:50]:
            cursor.execute("INSERT INTO buku (judul, penulis, kategori, harga, stok, cover_url, sinopsis) VALUES (?, ?, ?, ?, ?, ?, ?)", item)
    else:
        # Pastikan semua data tetap punya cover/sinopsis yang cukup
        for item in buku_dummy[:50]:
            cursor.execute("UPDATE buku SET cover_url=?, sinopsis=? WHERE judul=? AND penulis=?", (item[5], item[6], item[0], item[1]))

    cursor.execute("SELECT COUNT(*) FROM transaksi")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO transaksi (id_buku, jumlah_jual, total_harga, tanggal_transaksi) VALUES (1, 2, 190000, '2026-06-01')")
        cursor.execute("INSERT INTO transaksi (id_buku, jumlah_jual, total_harga, tanggal_transaksi) VALUES (3, 1, 250000, '2026-06-01')")
        
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("penjual", "12345", "Penjual"))
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("pembeli", "12345", "Pembeli"))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", ("nabila", "12345", "Pembeli"))

    conn.commit()
    conn.close()


def validate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id_user, username, password, role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


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

def get_total_transaksi():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM transaksi
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def get_low_stock_books():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT judul, stok
        FROM buku
        WHERE stok <= 5
        ORDER BY stok ASC
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def get_best_selling_books():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.judul,
               SUM(t.jumlah_jual)
        FROM transaksi t
        JOIN buku b
        ON b.id_buku=t.id_buku
        GROUP BY t.id_buku
        ORDER BY SUM(t.jumlah_jual) DESC
        LIMIT 5
    """)

    data = cursor.fetchall()

    conn.close()

    return data
def get_total_transaksi():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM transaksi")
    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_best_selling_book():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT buku.judul,
               SUM(transaksi.jumlah_jual) as total
        FROM transaksi
        JOIN buku ON transaksi.id_buku = buku.id_buku
        GROUP BY buku.judul
        ORDER BY total DESC
        LIMIT 1
    """)

    data = cursor.fetchone()

    conn.close()

    if data:
        return data[0]

    return "Belum Ada"


def get_low_stock_book():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT judul
        FROM buku
        ORDER BY stok ASC
        LIMIT 1
    """)

    data = cursor.fetchone()

    conn.close()

    if data:
        return data[0]

    return "-"


# =====================
# Keranjang Pembeli
# =====================

def _ensure_keranjang_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keranjang (
            id_user INTEGER NOT NULL,
            id_buku INTEGER NOT NULL,
            jumlah INTEGER NOT NULL,
            PRIMARY KEY (id_user, id_buku),
            FOREIGN KEY (id_buku) REFERENCES buku(id_buku) ON DELETE CASCADE
        )
    ''')
    conn.commit()


def cart_add_or_update(user_id, id_buku, qty_delta=1):
    """Tambah qty ke item keranjang. Qty tidak boleh melebihi stok."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT stok FROM buku WHERE id_buku=?", (id_buku,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise ValueError("Buku tidak ditemukan")

    stok = int(row[0])
    if stok <= 0:
        conn.close()
        raise ValueError("Stok buku habis")

    cursor.execute("SELECT jumlah FROM keranjang WHERE id_user=? AND id_buku=?", (user_id, id_buku))
    existing = cursor.fetchone()
    current_qty = int(existing[0]) if existing else 0

    new_qty = current_qty + int(qty_delta)
    if new_qty < 1:
        # anggap hapus
        cursor.execute("DELETE FROM keranjang WHERE id_user=? AND id_buku=?", (user_id, id_buku))
        conn.commit()
        conn.close()
        return

    if new_qty > stok:
        new_qty = stok

    cursor.execute(
        """
        INSERT INTO keranjang (id_user, id_buku, jumlah)
        VALUES (?, ?, ?)
        ON CONFLICT(id_user, id_buku) DO UPDATE SET jumlah=excluded.jumlah
        """,
        (user_id, id_buku, new_qty),
    )
    conn.commit()
    conn.close()


def cart_set_qty(user_id, id_buku, qty):
    """Set qty absolut. Jika qty<=0 maka item dihapus."""
    qty = int(qty)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if qty <= 0:
        cursor.execute("DELETE FROM keranjang WHERE id_user=? AND id_buku=?", (user_id, id_buku))
        conn.commit()
        conn.close()
        return

    cursor.execute("SELECT stok FROM buku WHERE id_buku=?", (id_buku,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise ValueError("Buku tidak ditemukan")

    stok = int(row[0])
    if stok <= 0:
        conn.close()
        raise ValueError("Stok buku habis")

    if qty > stok:
        qty = stok

    cursor.execute(
        """
        INSERT INTO keranjang (id_user, id_buku, jumlah)
        VALUES (?, ?, ?)
        ON CONFLICT(id_user, id_buku) DO UPDATE SET jumlah=excluded.jumlah
        """,
        (user_id, id_buku, qty),
    )
    conn.commit()
    conn.close()


def cart_get_items(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT k.id_buku,
               b.judul,
               b.harga,
               b.stok,
               k.jumlah,
               (b.harga * k.jumlah) AS subtotal
        FROM keranjang k
        JOIN buku b ON b.id_buku = k.id_buku
        WHERE k.id_user=?
        ORDER BY b.id_buku ASC
    ''', (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data


def cart_clear(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM keranjang WHERE id_user=?", (user_id,))
    conn.commit()
    conn.close()


def get_total_transaksi_user(user_id):
    if not user_id:
        return 0

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transaksi WHERE id_user=?", (user_id,))
    total = cursor.fetchone()[0]
    conn.close()
    return total


def get_transaksi_user_items(user_id):
    if not user_id:
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.id_transaksi,
               b.judul,
               t.jumlah_jual,
               t.total_harga,
               t.tanggal_transaksi
        FROM transaksi t
        JOIN buku b ON b.id_buku = t.id_buku
        WHERE t.id_user=?
        ORDER BY t.id_transaksi DESC
    ''', (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data


def checkout_cart(user_id, tanggal=None):
    """Checkout semua item keranjang: validasi stok, kurangi stok, simpan transaksi, lalu clear."""
    from datetime import date

    if tanggal is None:
        tanggal = str(date.today())

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id_buku, jumlah FROM keranjang WHERE id_user=?", (user_id,))
    items = cursor.fetchall()
    if not items:
        conn.close()
        raise ValueError("Keranjang kosong")

    # Validasi stok dulu
    for id_buku, qty in items:
        cursor.execute("SELECT stok, harga FROM buku WHERE id_buku=?", (id_buku,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise ValueError("Buku tidak ditemukan")
        stok, harga = int(row[0]), float(row[1])
        if qty > stok:
            conn.close()
            raise ValueError(f"Stok kurang untuk buku ID {id_buku}")

    total_spent = 0.0
    # proses
    for id_buku, qty in items:
        cursor.execute("SELECT harga FROM buku WHERE id_buku=?", (id_buku,))
        harga = float(cursor.fetchone()[0])
        total = harga * int(qty)
        total_spent += total

        cursor.execute("UPDATE buku SET stok = stok - ? WHERE id_buku=?", (int(qty), id_buku))
        cursor.execute(
            """
            INSERT INTO transaksi (id_user, id_buku, jumlah_jual, total_harga, tanggal_transaksi)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, id_buku, int(qty), total, tanggal),
        )

    cursor.execute("DELETE FROM keranjang WHERE id_user=?", (user_id,))

    conn.commit()
    conn.close()
    return total_spent

