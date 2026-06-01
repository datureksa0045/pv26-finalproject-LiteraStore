import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QPushButton, QLabel, QStackedWidget, 
                             QStatusBar, QMessageBox)
from PySide6.QtCore import Qt

from models import database_manager
from views.dashboard_view import DashboardPage
from views.buku_view import ManajemenBukuPage
from views.transaksi_view import TransaksiPage

class LiteraStoreApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LiteraStore - Sistem Informasi & Manajemen Toko Buku Digital")
        self.resize(1050, 650)
        
        database_manager.init_db()
        self.load_stylesheet(os.path.join("assets", "styles.qss"))
        
        self.init_menu_bar()
        self.init_status_bar()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setAlignment(Qt.AlignTop)
        
        lbl_logo = QLabel("📚 LiteraStore")
        lbl_logo.setObjectName("logo")
        sidebar_layout.addWidget(lbl_logo)
        
        self.btn_dash = QPushButton("Dashboard Analitik")
        self.btn_buku = QPushButton("Manajemen Buku")
        self.btn_transaksi = QPushButton("Kasir & Transaksi")
        
        for btn in [self.btn_dash, self.btn_buku, self.btn_transaksi]:
            btn.setCheckable(True)
            sidebar_layout.addWidget(btn)
            
        main_layout.addWidget(sidebar)
        
        self.pages = QStackedWidget()
        self.page_dashboard = DashboardPage()
        self.page_buku = ManajemenBukuPage()
        self.page_transaksi = TransaksiPage()
        
        self.pages.addWidget(self.page_dashboard)
        self.pages.addWidget(self.page_buku)
        self.pages.addWidget(self.page_transaksi)
        main_layout.addWidget(self.pages)
        
        self.btn_dash.clicked.connect(lambda: self.switch_page(0))
        self.btn_buku.clicked.connect(lambda: self.switch_page(1))
        self.btn_transaksi.clicked.connect(lambda: self.switch_page(2))
        
        self.switch_page(0)

    def load_stylesheet(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as file:
                self.setStyleSheet(file.read())

    def init_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        help_menu = menu_bar.addMenu("&Help")
        
        action_exit = file_menu.addAction("Exit")
        action_exit.setShortcut("Ctrl+Q")
        action_exit.triggered.connect(self.close)
        
        action_about = help_menu.addAction("About App")
        action_about.triggered.connect(lambda: QMessageBox.information(
            self, "Tentang Aplikasi", "LiteraStore v1.0.0\nSistem Manajemen Toko Buku Digital Berbasis PySide6."
        ))

    def init_status_bar(self):
        status = QStatusBar()
        self.setStatusBar(status)
        lbl_credits = QLabel("  Kelompok Mandiri LiteraStore | Anggota: [Nama - NIM] & [Nama Rekan - NIM]  ")
        lbl_credits.setStyleSheet("font-weight: 500; color: #475569; font-size: 11px;")
        status.addPermanentWidget(lbl_credits)

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
        self.btn_dash.setChecked(index == 0)
        self.btn_buku.setChecked(index == 1)
        self.btn_transaksi.setChecked(index == 2)
        
        if index == 0: self.page_dashboard.refresh_stats()
        elif index == 1: self.page_buku.load_data()
        elif index == 2:
            self.page_transaksi.load_buku_combobox()
            self.page_transaksi.load_transaksi()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LiteraStoreApp()
    window.show()
    sys.exit(app.exec())