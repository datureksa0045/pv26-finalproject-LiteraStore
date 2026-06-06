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
        layout.setSpacing(20)

        title = QLabel("📊 Dashboard Penjual")
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#1E293B;
        """)

        layout.addWidget(title)

        subtitle = QLabel(
            "Ringkasan aktivitas dan performa toko buku"
        )

        subtitle.setStyleSheet("""
            color:#64748B;
            font-size:14px;
        """)

        layout.addWidget(subtitle)

        total_buku, total_stok, pendapatan = database_manager.get_dashboard_stats()

        total_transaksi = database_manager.get_total_transaksi()

        buku_terlaris = database_manager.get_best_selling_book()

        stok_menipis = database_manager.get_low_stock_book()

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()

        self.card1 = self.create_card(
            "📚 Total Buku",
            str(total_buku),
            "#3B82F6"
        )

        self.card2 = self.create_card(
            "📦 Total Stok",
            str(total_stok),
            "#10B981"
        )

        self.card3 = self.create_card(
            "💰 Pendapatan",
            f"Rp {pendapatan:,.0f}",
            "#F59E0B"
        )

        self.card4 = self.create_card(
            "🛒 Total Transaksi",
            str(total_transaksi),
            "#8B5CF6"
        )

        self.card5 = self.create_card(
            "🔥 Buku Terlaris",
            buku_terlaris,
            "#EF4444"
        )

        self.card6 = self.create_card(
            "⚠️ Stok Menipis",
            stok_menipis,
            "#F97316"
        )

        row1.addWidget(self.card1)
        row1.addWidget(self.card2)
        row1.addWidget(self.card3)

        row2.addWidget(self.card4)
        row2.addWidget(self.card5)
        row2.addWidget(self.card6)

        layout.addLayout(row1)
        layout.addLayout(row2)

        layout.addStretch()

    def create_card(self, title, value, color):

        card = QFrame()

        card.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #E2E8F0;
                border-radius:18px;
            }
        """)

        card.setMinimumHeight(140)

        vbox = QVBoxLayout(card)
        vbox.setAlignment(Qt.AlignCenter)

        lbl_title = QLabel(title)

        lbl_title.setStyleSheet("""
            color:#64748B;
            font-size:13px;
            font-weight:600;
        """)

        lbl_value = QLabel(value)

        lbl_value.setStyleSheet(f"""
            color:{color};
            font-size:22px;
            font-weight:bold;
        """)

        vbox.addWidget(lbl_title)
        vbox.addWidget(lbl_value)

        return card

    def refresh_stats(self):
        pass