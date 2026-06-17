from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame
)

from PySide6.QtCore import Qt
from models import database_manager


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30,30,30,30)
        layout.setSpacing(18)

        header = QHBoxLayout()
        header.setSpacing(10)

        title = QLabel("📊 Dashboard Penjual")
        title.setStyleSheet("""
            font-size:28px;
            font-weight:800;
            color:#5A4127;
        """)

        badge = QLabel("Live Store Overview")
        badge.setStyleSheet("""
            background-color:#F2E6D9;
            color:#8A6A49;
            border:1px solid #E4D4C2;
            border-radius:12px;
            padding:6px 10px;
            font-size:11px;
            font-weight:700;
        """)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(badge)
        layout.addLayout(header)

        subtitle = QLabel("Ringkasan aktivitas dan performa toko buku yang nyaman dipantau.")
        subtitle.setStyleSheet("""
            color:#7A6651;
            font-size:14px;
        """)

        layout.addWidget(subtitle)

        total_buku, total_stok, pendapatan = database_manager.get_dashboard_stats()

        total_transaksi = database_manager.get_total_transaksi()

        buku_terlaris = database_manager.get_best_selling_book()

        stok_menipis = database_manager.get_low_stock_book()

        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()

        self.card1 = self.create_card("📚 Total Buku", str(total_buku), "#A67C52", "Jumlah judul buku tersedia")
        self.card2 = self.create_card("📦 Total Stok", str(total_stok), "#7C9A5C", "Stok keseluruhan di rak")
        self.card3 = self.create_card("💰 Pendapatan", f"Rp {pendapatan:,.0f}", "#D48A38", "Total omset penjualan")
        self.card4 = self.create_card("🛒 Total Transaksi", str(total_transaksi), "#8B5CF6", "Jumlah transaksi tercatat")
        self.card5 = self.create_card("🔥 Buku Terlaris", buku_terlaris, "#C96A4B", "Judul paling banyak terjual")
        self.card6 = self.create_card("⚠️ Stok Menipis", stok_menipis, "#CA7C3D", "Buku yang perlu segera diisi")

        self.row1.addWidget(self.card1)
        self.row1.addWidget(self.card2)
        self.row1.addWidget(self.card3)

        self.row2.addWidget(self.card4)
        self.row2.addWidget(self.card5)
        self.row2.addWidget(self.card6)

        layout.addLayout(self.row1)
        layout.addLayout(self.row2)

        layout.addStretch()

    def create_card(self, title, value, color, hint):
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet("""
            QFrame#card {
                background-color: #FFFDFB;
                border: 1px solid #E6D8C8;
                border-radius: 18px;
            }
        """)
        card.setMinimumHeight(152)
        card.setMaximumWidth(420)

        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(16, 16, 16, 16)
        vbox.setSpacing(6)

        icon = QLabel(title.split()[0])
        icon.setStyleSheet("font-size:14px; color:#A67C52; font-weight:800;")

        lbl_title = QLabel(title.replace(title.split()[0], "").strip())
        lbl_title.setStyleSheet("""
            color:#6F5A43;
            font-size:13px;
            font-weight:700;
        """)

        lbl_value = QLabel(value)
        lbl_value.setStyleSheet(f"""
            color:{color};
            font-size:22px;
            font-weight:800;
        """)

        badge_status = QLabel("Premium")
        badge_status.setStyleSheet("""
            background-color:#F4E7D8;
            color:#8A6A49;
            border:1px solid #E4D4C2;
            border-radius:10px;
            padding:4px 8px;
            font-size:10px;
            font-weight:700;
        """)

        lbl_hint = QLabel(hint)
        lbl_hint.setStyleSheet("""
            color:#8C745C;
            font-size:12px;
        """)

        title_row = QHBoxLayout()
        title_row.setSpacing(8)
        title_row.addWidget(icon)
        title_row.addWidget(lbl_title)
        title_row.addStretch()

        vbox.addLayout(title_row)
        vbox.addWidget(lbl_value)
        vbox.addWidget(badge_status)
        vbox.addWidget(lbl_hint)

        return card

    def refresh_stats(self):
        total_buku, total_stok, pendapatan = database_manager.get_dashboard_stats()
        total_transaksi = database_manager.get_total_transaksi()
        buku_terlaris = database_manager.get_best_selling_book()
        stok_menipis = database_manager.get_low_stock_book()

        for layout in (self.row1, self.row2):
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        self.card1 = self.create_card("📚 Total Buku", str(total_buku), "#A67C52", "Jumlah judul buku tersedia")
        self.card2 = self.create_card("📦 Total Stok", str(total_stok), "#7C9A5C", "Stok keseluruhan di rak")
        self.card3 = self.create_card("💰 Pendapatan", f"Rp {pendapatan:,.0f}", "#D48A38", "Total omset penjualan")
        self.card4 = self.create_card("🛒 Total Transaksi", str(total_transaksi), "#8B5CF6", "Jumlah transaksi tercatat")
        self.card5 = self.create_card("🔥 Buku Terlaris", buku_terlaris, "#C96A4B", "Judul paling banyak terjual")
        self.card6 = self.create_card("⚠️ Stok Menipis", stok_menipis, "#CA7C3D", "Buku yang perlu segera diisi")

        self.row1.addWidget(self.card1)
        self.row1.addWidget(self.card2)
        self.row1.addWidget(self.card3)
        self.row2.addWidget(self.card4)
        self.row2.addWidget(self.card5)
        self.row2.addWidget(self.card6)