from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QGridLayout,
    QFrame,
    QPushButton,
    QMessageBox,
    QHBoxLayout
)

from PySide6.QtCore import Qt

from models import database_manager


class DashboardPembeliPage(QWidget):
    def __init__(self):
        super().__init__()

        self.cart_count = 0
        self.cart_items = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("📚 LiteraStore")
        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
            color:#8B5E3C;
        """)
        layout.addWidget(title)

        subtitle = QLabel(
            "Selamat datang, jelajahi koleksi buku terbaik kami"
        )
        subtitle.setStyleSheet("""
            color:#6B7280;
            font-size:14px;
        """)
        layout.addWidget(subtitle)

        self.info = QLabel()
        self.info.setStyleSheet("""
            font-size:14px;
            font-weight:600;
            color:#374151;
        """)
        layout.addWidget(self.info)

        self.btn_keranjang = QPushButton("🛒 Keranjang (0)")
        self.btn_keranjang.setStyleSheet("""
            QPushButton{
                background:#B78652;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
                font-weight:bold;
                min-height:40px;
            }
            QPushButton:hover{
                background:#9E6F3D;
            }
        """)

        self.btn_keranjang.clicked.connect(
            self.lihat_keranjang
        )

        layout.addWidget(self.btn_keranjang)
        self.btn_keranjang.setFixedHeight(35)

        kategori_title = QLabel("📂 Kategori")
        kategori_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:#1F2937;
        """)
        layout.addWidget(kategori_title)

        kategori_layout = QHBoxLayout()

        self.kategori_aktif = "Semua"
        
        kategori_semua = QPushButton("Semua")
        kategori_fiksi = QPushButton("Fiksi")
        kategori_non = QPushButton("Non-Fiksi")
        kategori_tekno = QPushButton("Teknologi")
        kategori_sains = QPushButton("Sains")
        
        kategori_semua.clicked.connect(
            lambda: self.filter_kategori("Semua")
            )
        kategori_fiksi.clicked.connect(
             lambda: self.filter_kategori("Fiksi")
            )
        kategori_non.clicked.connect(
             lambda: self.filter_kategori("Non-Fiksi")
            )
        kategori_tekno.clicked.connect(
             lambda: self.filter_kategori("Teknologi")
            )
        kategori_sains.clicked.connect(
             lambda: self.filter_kategori("Sains")
            )
        
        for btn in [
             kategori_semua,
             kategori_fiksi,
             kategori_non,
             kategori_tekno,
             kategori_sains
             ]:
             
             btn.setStyleSheet(""" QPushButton{
                               background:#F3E8D5;
                               color:#8B5E3C;
                               border:1px solid #D6B48A;
                               border-radius:12px;
                               padding:10px;
                               font-weight:bold;
                               }
                               QPushButton:hover{
                               background:#D6B48A;
                            }
                               """)
             kategori_layout.addWidget(btn)
             
             layout.addLayout(kategori_layout)

        best_title = QLabel("🔥 Buku Terlaris")
        best_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:#DC2626;
        """)
        layout.addWidget(best_title)
        best_title.setFixedHeight(25)

        try:
            best_books = database_manager.get_best_selling_books()

            if best_books:

                for idx, buku in enumerate(best_books):

                    item = QLabel(
                        f"⭐  {buku[0]}"
                    )

                    item.setFixedHeight(20)

                    item.setStyleSheet("""
                        font-size:14px;
                        color:#374151;
                        font-weight:600;
                    """)

                    layout.addWidget(item)

            else:
                layout.addWidget(
                    QLabel("Belum ada data penjualan.")
                )

        except:
            layout.addWidget(
                QLabel("Belum ada data penjualan.")
            )

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "🔍 Cari judul atau penulis buku..."
        )

        self.search.textChanged.connect(
            self.load_data
        )

        layout.addWidget(self.search)

        semua_buku = QLabel("📖 Semua Buku")
        semua_buku.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:#1F2937;
        """)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        container = QWidget()
        
        scroll = QScrollArea()
        
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        container = QWidget()
        container.setStyleSheet("""
                                QWidget{
                                background:#F8F5EF;
                                }
                                """)
        scroll_layout = QVBoxLayout(container)
        scroll_layout.setContentsMargins(20,20,20,20)
        scroll_layout.setSpacing(15)
        
        scroll_layout.addWidget(self.search)
        scroll_layout.addWidget(best_title)
        scroll_layout.addWidget(semua_buku)
        
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(10,10,10,10)
        
        books_widget = QWidget()
        books_widget.setLayout(self.grid)
        
        scroll_layout.addWidget(books_widget)
        scroll.setWidget(container)
        
        layout.addWidget(scroll,1)

        self.load_data()

    def tambah_ke_keranjang(self, judul):

        self.cart_count += 1

        self.cart_items.append(judul)

        self.btn_keranjang.setText(
            f"🛒 Keranjang ({self.cart_count})"
        )

        QMessageBox.information(
            self,
            "Keranjang",
            f"{judul} berhasil ditambahkan ke keranjang."
        )

    def lihat_keranjang(self):

        if not self.cart_items:

            QMessageBox.information(
                self,
                "Keranjang",
                "Keranjang masih kosong."
            )

            return

        isi = "\n".join(
            [f"{i+1}. {item}" for i, item in enumerate(self.cart_items)]
        )

        QMessageBox.information(
            self,
            "Isi Keranjang",
            isi
        )

    def filter_kategori(self, kategori):
        self.kategori_aktif = kategori
        self.load_data()

    def load_data(self):

        books = database_manager.get_all_buku(
            search=self.search.text(),
        )

        if self.kategori_aktif != "Semua":
            books = [
                book for book in books
                if book[3] == self.kategori_aktif
            ]
            
        self.info.setText(
            f"Jumlah Buku Tersedia : {len(books)}"
        )

        while self.grid.count():

            item = self.grid.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        row = 0
        col = 0

        for book in books:
            
            card = QFrame()
            card.setObjectName("card")
            
            card.setMinimumSize(280, 280)
            card.setMaximumHeight(300)

            card.setMinimumHeight(250)
            card.setMaximumHeight(250)

            card_layout = QVBoxLayout(card)

            judul = QLabel(book[1])
            judul.setWordWrap(True)

            judul.setStyleSheet("""
                color:#1F2937;
                font-size:16px;
                font-weight:bold;
                background:transparent;
            """)

            penulis = QLabel(
                f"✍ Penulis : {book[2]}"
            )

            penulis.setStyleSheet("""
                color:#374151;
                background:transparent;                  
            """)


            kategori = QLabel(
                f"📂 Kategori : {book[3]}"
            )
            kategori.setStyleSheet("""
                color:#374151;
                background:transparent;
            """)

            harga = QLabel(
                f"💰 Harga : Rp {book[4]:,.0f}"
            )
            harga.setStyleSheet("""
                color:#059669;
                font-size:15px;
                font-weight:bold;
                background:transparent; 
            """)

            stok = QLabel(
                f"📦 Stok : {book[5]}"
            )
            stok.setStyleSheet("""
                color:#374151;
                background:transparent;
            """)

            btn_beli = QPushButton(
                "🛒 Tambah ke Keranjang"
            )

            btn_beli.setFixedHeight(40)

            btn_beli.setStyleSheet("""
                QPushButton{
                    background:#B78652;
                    color:white;
                    border:none;
                    border-radius:10px;
                    padding:12px;
                    font-weight:bold;
                    min-height:40px;
                }

                QPushButton:hover{
                    background:#9E6F3D;
                }
            """)

            btn_beli.clicked.connect(
                lambda checked, judul=book[1]:
                self.tambah_ke_keranjang(judul)
            )

            card_layout.addWidget(judul)
            card_layout.addWidget(penulis)
            card_layout.addWidget(kategori)
            card_layout.addWidget(harga)
            card_layout.addWidget(stok)
            card_layout.addWidget(btn_beli)

            self.grid.addWidget(
                card,
                row,
                col,
                alignment=Qt.AlignTop
            )

            self.grid.setColumnStretch(col, 1)

            col += 1

            if col == 3:
                col = 0
                row += 1