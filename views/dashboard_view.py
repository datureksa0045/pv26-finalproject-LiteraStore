from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from models import database_manager

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        title = QLabel("📊 Dashboard Analitik LiteraStore")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1E293B;")
        layout.addWidget(title)
        
        card_layout = QHBoxLayout()
        card_layout.setSpacing(20)
        
        total_buku, total_stok, pendapatan = database_manager.get_dashboard_stats()
        
        self.card1 = self.create_card("Total Judul Buku", f"{total_buku} Buku", "#3B82F6")
        self.card2 = self.create_card("Total Stok Toko", f"{total_stok} Eksemplar", "#10B981")
        self.card3 = self.create_card("Total Pendapatan", f"Rp {pendapatan:,.0f}", "#F59E0B")
        
        card_layout.addWidget(self.card1)
        card_layout.addWidget(self.card2)
        card_layout.addWidget(self.card3)
        layout.addLayout(card_layout)
        
        info_frame = QFrame()
        info_frame.setObjectName("card")
        info_layout = QVBoxLayout(info_frame)
        
        welcome_lbl = QLabel("Selamat Datang di Sistem Informasi LiteraStore")
        welcome_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #0F172A;")
        desc_lbl = QLabel("Gunakan menu sidebar di sebelah kiri untuk mengelola entitas buku, memproses transaksi penjualan, serta mengekspor laporan akhir ke dalam format CSV.")
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("color: #64748B; font-size: 13px; line-height: 1.5;")
        
        info_layout.addWidget(welcome_lbl)
        info_layout.addWidget(desc_lbl)
        layout.addWidget(info_frame)
        layout.addStretch()

    def create_card(self, title, value, accent_color):
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(120)
        
        v_layout = QVBoxLayout(card)
        v_layout.setAlignment(Qt.AlignCenter)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #64748B; font-size: 13px; font-weight: 500;")
        
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet(f"color: {accent_color}; font-size: 24px; font-weight: bold; margin-top: 5px;")
        
        v_layout.addWidget(lbl_title)
        v_layout.addWidget(lbl_val)
        return card

    def refresh_stats(self):
        total_buku, total_stok, pendapatan = database_manager.get_dashboard_stats()
        self.card1.findChildren(QLabel)[1].setText(f"{total_buku} Buku")
        self.card2.findChildren(QLabel)[1].setText(f"{total_stok} Eksemplar")
        self.card3.findChildren(QLabel)[1].setText(f"Rp {pendapatan:,.0f}")