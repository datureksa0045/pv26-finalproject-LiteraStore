from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QGridLayout,
    QFrame
)

from models import database_manager


class DashboardPembeliPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Judul
        title = QLabel("📚 Dashboard Pembeli")
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#1E293B;
        """)
        layout.addWidget(title)

        subtitle = QLabel("Temukan buku favoritmu hari ini")
        subtitle.setStyleSheet("""
            color:#64748B;
            font-size:14px;
        """)
        layout.addWidget(subtitle)

        # Info jumlah buku
        self.info = QLabel()
        self.info.setStyleSheet("""
            font-size:14px;
            font-weight:bold;
            color:#334155;
        """)
        layout.addWidget(self.info)

        # Search
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Cari judul atau penulis buku...")
        self.search.textChanged.connect(self.load_data)
        layout.addWidget(self.search)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setSpacing(20)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.load_data()

    def load_data(self):

        books = database_manager.get_all_buku()

        keyword = self.search.text().lower()

        if keyword:
            books = [
                b for b in books
                if keyword in b[1].lower()
                or keyword in b[2].lower()
            ]

        self.info.setText(
            f"Jumlah Buku Tersedia : {len(books)}"
        )

        # Hapus card lama
        while self.grid.count():
            item = self.grid.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        row = 0
        col = 0

        for book in books:

            card = QFrame()

            card.setStyleSheet("""
                QFrame{
                    background-color:white;
                    border:1px solid #E2E8F0;
                    border-radius:15px;
                }
            """)

            card.setMinimumHeight(220)

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(15,15,15,15)
            card_layout.setSpacing(8)

            judul = QLabel(book[1])
            judul.setStyleSheet("""
                color:#0F172A;
                font-size:18px;
                font-weight:bold;
                border:none;
            """)

            penulis = QLabel(
                f"✍ Penulis : {book[2]}"
            )
            penulis.setStyleSheet("""
                color:#475569;
                font-size:13px;
                border:none;
            """)

            kategori = QLabel(
                f"📂 Kategori : {book[3]}"
            )
            kategori.setStyleSheet("""
                color:#475569;
                font-size:13px;
                border:none;
            """)

            harga = QLabel(
                f"💰 Rp {book[4]:,.0f}"
            )
            harga.setStyleSheet("""
                color:#10B981;
                font-size:16px;
                font-weight:bold;
                border:none;
            """)

            stok = QLabel(
                f"📦 Stok : {book[5]}"
            )
            stok.setStyleSheet("""
                color:#475569;
                font-size:13px;
                border:none;
            """)

            card_layout.addWidget(judul)
            card_layout.addWidget(penulis)
            card_layout.addWidget(kategori)
            card_layout.addStretch()
            card_layout.addWidget(harga)
            card_layout.addWidget(stok)

            self.grid.addWidget(
                card,
                row,
                col
            )

            col += 1

            if col == 3:
                col = 0
                row += 1