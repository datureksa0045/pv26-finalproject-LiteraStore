import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QStatusBar,
    QMessageBox,
    QDialog,
)
from PySide6.QtCore import Qt, QTimer

from models import database_manager
from views.dashboard_view import DashboardPage
from views.dashboard_pembeli_view import DashboardPembeliPage
from views.buku_view import ManajemenBukuPage
from views.transaksi_view import TransaksiPage
from views.login_view import LoginDialog


class LiteraStoreApp(QMainWindow):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data or {"username": "Guest", "role": "Penjual"}
        self.setWindowTitle(
            f"LiteraStore - {self.user_data['role']} ({self.user_data['username']})"
        )
        self.resize(1050, 650)

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

        self.is_pembeli = self.user_data.get("role") == "Pembeli"

        self.btn_dash = QPushButton("Home" if self.is_pembeli else "Dashboard Analitik")
        self.btn_cart = QPushButton("Keranjang")
        self.btn_history = QPushButton("Riwayat")
        self.btn_buku = QPushButton("Manajemen Buku")
        self.btn_transaksi = QPushButton("Kasir & Transaksi")

        menu_buttons = (
            [self.btn_dash, self.btn_cart, self.btn_history]
            if self.is_pembeli
            else [self.btn_dash, self.btn_buku, self.btn_transaksi]
        )
        for btn in menu_buttons:
            btn.setCheckable(True)
            sidebar_layout.addWidget(btn)

        main_layout.addWidget(sidebar)

        self.pages = QStackedWidget()

        if self.is_pembeli:
            # Pembeli: Home, keranjang, dan riwayat dikelola dari sidebar utama.
            self.page_dashboard = DashboardPembeliPage(self.user_data)
            self.page_buku = None
            self.page_transaksi = None

            self.pages.addWidget(self.page_dashboard)  # index 0
            main_layout.addWidget(self.pages)

            self.btn_dash.clicked.connect(lambda: self.switch_page(0))
            self.btn_cart.clicked.connect(lambda: self.switch_page(1))
            self.btn_history.clicked.connect(lambda: self.switch_page(2))
            self.switch_page(0)
        else:
            # Penjual: buka dashboard dulu, halaman lain dibuat saat diklik.
            self.page_dashboard = DashboardPage()
            self.page_buku = None
            self.page_transaksi = None
            self.placeholder_buku = QWidget()
            self.placeholder_transaksi = QWidget()

            self.pages.addWidget(self.page_dashboard)  # index 0
            self.pages.addWidget(self.placeholder_buku)  # index 1
            self.pages.addWidget(self.placeholder_transaksi)  # index 2
            main_layout.addWidget(self.pages)

            self.btn_dash.clicked.connect(lambda: self.switch_page(0))
            self.btn_buku.clicked.connect(lambda: self.switch_page(1))
            self.btn_transaksi.clicked.connect(lambda: self.switch_page(2))

            self.switch_page(0)

    def _replace_page(self, index, old_widget, new_widget):
        current = self.pages.currentIndex()
        self.pages.removeWidget(old_widget)
        old_widget.deleteLater()
        self.pages.insertWidget(index, new_widget)
        self.pages.setCurrentIndex(current)

    def ensure_seller_page(self, index):
        if index == 1 and self.page_buku is None:
            self.page_buku = ManajemenBukuPage()
            self._replace_page(1, self.placeholder_buku, self.page_buku)
        elif index == 2 and self.page_transaksi is None:
            self.page_transaksi = TransaksiPage()
            self._replace_page(2, self.placeholder_transaksi, self.page_transaksi)

    def load_stylesheet(self, filename):
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                self.setStyleSheet(file.read())

    def init_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        help_menu = menu_bar.addMenu("&Help")

        action_exit = file_menu.addAction("Exit")
        action_exit.setShortcut("Ctrl+Q")
        action_exit.triggered.connect(self.close)

        action_about = help_menu.addAction("About App")
        action_about.triggered.connect(
            lambda: QMessageBox.information(
                self,
                "Tentang Aplikasi",
                "LiteraStore v1.0.0\nSistem Manajemen Toko Buku Digital Berbasis PySide6.",
            )
        )

    def init_status_bar(self):
        status = QStatusBar()
        self.setStatusBar(status)

        lbl_credits = QLabel(
            "  LiteraStore | Datu Reksa Hamza Putra (F1D02310045) | "
            "Nabila Zahirani (F1D02310019) | Rosida Asri Ardiani (F1D02410142)  "
        )
        status.showMessage(
            f"Login sebagai {self.user_data['role']} - {self.user_data['username']}"
        )
        lbl_credits.setStyleSheet("font-weight: 500; color: #475569; font-size: 11px;")
        status.addPermanentWidget(lbl_credits)

    def switch_page(self, index):
        if self.is_pembeli:
            self.pages.setCurrentIndex(0)
            self.btn_dash.setChecked(index == 0)
            self.btn_cart.setChecked(index == 1)
            self.btn_history.setChecked(index == 2)

            if index == 0:
                self.page_dashboard.show_home()
            elif index == 1:
                self.page_dashboard.show_cart()
            elif index == 2:
                self.page_dashboard.show_history()
            return

        self.btn_dash.setChecked(index == 0)
        self.btn_buku.setChecked(index == 1)
        self.btn_transaksi.setChecked(index == 2)

        self.ensure_seller_page(index)
        self.pages.setCurrentIndex(index)

        if index == 0 and self.page_dashboard is not None:
            if hasattr(self.page_dashboard, "refresh_stats"):
                self.page_dashboard.refresh_stats()
        elif index == 1 and self.page_buku is not None:
            self.page_buku.load_data()
        elif index == 2 and self.page_transaksi is not None:
            self.page_transaksi.load_buku_combobox()
            self.page_transaksi.load_transaksi()


def main():
    database_manager.init_db()
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec() != QDialog.Accepted or not login_dialog.user_data:
        return 0

    window = LiteraStoreApp(login_dialog.user_data)

    def open_dashboard():
        window.showMaximized()
        window.raise_()
        window.activateWindow()

    QTimer.singleShot(0, open_dashboard)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

