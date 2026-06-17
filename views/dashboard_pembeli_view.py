from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QGridLayout,
    QFrame,
    QDialog,
    QPushButton,
    QMessageBox,
    QCheckBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

import base64
import urllib.request

from models import database_manager


def load_pixmap_from_url(url: str):
    pixmap = QPixmap()
    if not url:
        return pixmap

    if url.startswith("data:"):
        try:
            _, encoded = url.split(",", 1)
            image_bytes = base64.b64decode(encoded)
            pixmap.loadFromData(image_bytes)
        except Exception:
            return QPixmap()
        return pixmap

    try:
        pixmap.loadFromData(urllib.request.urlopen(url).read())
    except Exception:
        return QPixmap()
    return pixmap


class BookDetailDialog(QDialog):
    def __init__(self, book, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sinopsis Buku")
        self.setModal(True)
        self.resize(520, 620)
        self.setStyleSheet(
            """
            QDialog { background-color: #FFFDFB; }
            QLabel { color: #5A4127; }
            QPushButton { background-color: #A67C52; color: #FFFDF9; border-radius: 10px; padding: 8px 14px; }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        cover = QLabel()
        cover.setAlignment(Qt.AlignCenter)
        cover.setFixedHeight(180)
        cover.setStyleSheet("background-color: #F5EBE1; border-radius: 14px;")
        pixmap = load_pixmap_from_url(book[6] if len(book) > 6 else "")
        if pixmap.isNull():
            cover.setText("📚 Gambar buku tidak tersedia")
        else:
            cover.setPixmap(
                pixmap.scaled(140, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        layout.addWidget(cover, alignment=Qt.AlignCenter)

        title = QLabel(book[1])
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #5A4127;")
        layout.addWidget(title)

        meta = QLabel(
            f"Penulis: {book[2]}   •   Kategori: {book[3]}   •   Harga: Rp {int(book[4])}"
        )
        meta.setStyleSheet("font-size: 12px; color: #7A6651;")
        meta.setWordWrap(True)
        layout.addWidget(meta)

        synopsis = QLabel(book[7] if len(book) > 7 else "Sinopsis belum tersedia.")
        synopsis.setWordWrap(True)
        synopsis.setStyleSheet(
            "font-size: 13px; color: #5A4127; line-height: 1.45;"
        )
        layout.addWidget(synopsis)

        btn_close = QPushButton("Tutup")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignRight)


class DashboardPembeliPage(QWidget):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data or {"id": None}
        self.user_id = self.user_data.get("id")

        self.setObjectName("buyerShell")
        self.setStyleSheet(
            """
            QWidget#buyerShell {
                background-color: #ECE4DB;
                background-image: url("assets/books_blur.svg");
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
            QWidget#buyerShell::before {
                content: "";
                position: absolute;
                inset: 0;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 249, 242, 0.10),
                    stop:0.30 rgba(235, 224, 213, 0.28),
                    stop:0.65 rgba(97, 71, 49, 0.38),
                    stop:1 rgba(45, 31, 21, 0.52));
                pointer-events: none;
            }
            QLineEdit {
                border: 1px solid #D8C8B6;
                border-radius: 12px;
                padding: 10px 12px;
                background-color: rgba(255, 255, 255, 0.95);
                color: #4B3522;
            }
            QPushButton { font-weight: 900; }
            QPushButton#btnCheckout {
                background-color: #10B981;
                color: #FFFDF9;
                border: none;
                border-radius: 12px;
                padding: 10px 14px;
            }
            QPushButton#btnCheckout:hover { background-color: #0E9B6E; }
            QPushButton#btnQty {
                background-color: #EFE2D1;
                border: 1px solid #DCCBB4;
                border-radius: 10px;
                color: #5A4127;
                font-weight: 900;
                font-size: 16px;
            }
            QCheckBox#checkoutStatusBox {
                color: #5A4127;
                font-size: 13px;
                font-weight: 800;
                spacing: 8px;
            }
            QCheckBox#checkoutStatusBox::indicator {
                width: 18px;
                height: 18px;
            }
            QFrame#buyerCard {
                background-color: rgba(255, 252, 248, 0.96);
                border: 1px solid #E2D1BE;
                border-radius: 18px;
                box-shadow: 0 10px 24px rgba(63, 46, 32, 0.18);
            }
            QLabel#buyerInfo {
                color: #5A4127;
                font-size: 14px;
                font-weight: 700;
            }
            QLabel#buyerSectionTitle {
                font-size: 20px;
                font-weight: 900;
                color: #5A4127;
            }
            QLabel#cartTotal {
                font-size: 16px;
                font-weight: 900;
                color: #A67C52;
            }
            QLabel#checkoutStatus {
                color: #0E9B6E;
                font-size: 13px;
                font-weight: 800;
                padding: 6px 0;
            }
            QLabel#receiptTitle {
                color: #0F766E;
                font-size: 18px;
                font-weight: 900;
            }
            QLabel#receiptMeta {
                color: #5A4127;
                font-size: 13px;
                font-weight: 700;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(14)

        header = QHBoxLayout()
        username = self.user_data.get("username") or "Pembeli"
        title = QLabel(f"Halo {username}")
        header_title_style = "color:#5A4127; font-size:28px; font-weight:800;"
        title.setStyleSheet(header_title_style)
        badge = QLabel("Book Discovery")
        badge.setStyleSheet(
            "background-color: rgba(242, 230, 217, 0.92); color:#8A6A49; border:1px solid #E4D4C2; border-radius:12px; padding:6px 10px; font-size:11px; font-weight:700;"
        )
        header.addWidget(title)
        header.addStretch()
        header.addWidget(badge)
        layout.addLayout(header)

        subtitle = QLabel(
            "Temukan buku favoritmu hari ini dan pilih yang paling cocok untuk dibaca."
        )
        subtitle.setStyleSheet("color:#7A6651; font-size:14px;")
        layout.addWidget(subtitle)

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Cari judul atau penulis buku...")
        self.search.textChanged.connect(self.load_data)
        layout.addWidget(self.search)

        self.panel_dashboard = QFrame()
        self.panel_dashboard_layout = QVBoxLayout(self.panel_dashboard)
        self.panel_dashboard_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_dashboard_layout.setSpacing(12)

        self.panel_cart = QFrame()
        self.panel_cart_layout = QVBoxLayout(self.panel_cart)
        self.panel_cart_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_cart_layout.setSpacing(12)

        self.panel_cart_scroll = QScrollArea()
        self.panel_cart_scroll.setWidgetResizable(True)
        self.panel_cart_scroll.setFrameShape(QFrame.NoFrame)
        self.panel_cart_scroll.setWidget(self.panel_cart)

        self.panel_history = QFrame()
        self.panel_history_layout = QVBoxLayout(self.panel_history)
        self.panel_history_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_history_layout.setSpacing(12)

        self.panel_history_scroll = QScrollArea()
        self.panel_history_scroll.setWidgetResizable(True)
        self.panel_history_scroll.setFrameShape(QFrame.NoFrame)
        self.panel_history_scroll.setWidget(self.panel_history)

        layout.addWidget(self.panel_dashboard)
        layout.addWidget(self.panel_cart_scroll)
        layout.addWidget(self.panel_history_scroll)

        # Panel dashboard: stats + etalase
        self.info = QLabel()
        self.info.setObjectName("buyerInfo")
        self.panel_dashboard_layout.addWidget(self.info)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setSpacing(20)
        scroll.setWidget(container)
        self.panel_dashboard_layout.addWidget(scroll)

        # Panel cart
        cart_title = QLabel("Keranjang Saya")
        cart_title.setObjectName("buyerSectionTitle")
        self.panel_cart_layout.addWidget(cart_title)

        active_cart_title = QLabel("Keranjang Aktif")
        active_cart_title.setObjectName("buyerInfo")
        self.panel_cart_layout.addWidget(active_cart_title)

        self.cart_frame = QFrame()
        self.cart_frame.setObjectName("buyerCard")
        self.cart_frame_layout = QVBoxLayout(self.cart_frame)
        self.cart_frame_layout.setContentsMargins(15, 15, 15, 15)
        self.cart_frame_layout.setSpacing(10)

        self.cart_rows_container = QWidget()
        self.cart_rows_layout = QVBoxLayout(self.cart_rows_container)
        self.cart_rows_layout.setContentsMargins(0, 0, 0, 0)
        self.cart_rows_layout.setSpacing(8)
        self.cart_frame_layout.addWidget(self.cart_rows_container)

        bottom_bar = QHBoxLayout()
        self.cart_total_label = QLabel("Total Bayar: Rp 0")
        self.cart_total_label.setObjectName("cartTotal")
        bottom_bar.addWidget(self.cart_total_label)
        bottom_bar.addStretch()

        self.btn_checkout = QPushButton("Checkout")
        self.btn_checkout.setObjectName("btnCheckout")
        self.btn_checkout.clicked.connect(self.checkout)
        bottom_bar.addWidget(self.btn_checkout)

        self.cart_frame_layout.addLayout(bottom_bar)

        self.checkout_status_box = QCheckBox("Checkout belum dilakukan")
        self.checkout_status_box.setObjectName("checkoutStatusBox")
        self.checkout_status_box.setEnabled(False)
        self.cart_frame_layout.addWidget(self.checkout_status_box)

        self.panel_cart_layout.addWidget(self.cart_frame)

        self.receipt_frame = QFrame()
        self.receipt_frame.setObjectName("buyerCard")
        self.receipt_frame_layout = QVBoxLayout(self.receipt_frame)
        self.receipt_frame_layout.setContentsMargins(16, 16, 16, 16)
        self.receipt_frame_layout.setSpacing(10)

        self.checkout_status_label = QLabel("")
        self.checkout_status_label.setObjectName("receiptTitle")
        self.checkout_status_label.setWordWrap(True)
        self.receipt_frame_layout.addWidget(self.checkout_status_label)

        self.receipt_meta_label = QLabel("")
        self.receipt_meta_label.setObjectName("receiptMeta")
        self.receipt_meta_label.setWordWrap(True)
        self.receipt_frame_layout.addWidget(self.receipt_meta_label)

        self.receipt_rows_container = QWidget()
        self.receipt_rows_layout = QVBoxLayout(self.receipt_rows_container)
        self.receipt_rows_layout.setContentsMargins(0, 0, 0, 0)
        self.receipt_rows_layout.setSpacing(6)
        self.receipt_frame_layout.addWidget(self.receipt_rows_container)

        receipt_actions = QHBoxLayout()
        receipt_actions.addStretch()
        self.btn_continue_shopping = QPushButton("Lanjut Belanja")
        self.btn_continue_shopping.setObjectName("btnCheckout")
        self.btn_continue_shopping.clicked.connect(self.show_home)
        receipt_actions.addWidget(self.btn_continue_shopping)
        self.receipt_frame_layout.addLayout(receipt_actions)

        self.receipt_frame.hide()
        self.panel_cart_layout.addWidget(self.receipt_frame)

        history_title = QLabel("Riwayat Transaksi")
        history_title.setObjectName("buyerSectionTitle")
        self.panel_history_layout.addWidget(history_title)

        self.history_frame = QFrame()
        self.history_frame.setObjectName("buyerCard")
        self.history_frame_layout = QVBoxLayout(self.history_frame)
        self.history_frame_layout.setContentsMargins(15, 15, 15, 15)
        self.history_frame_layout.setSpacing(8)

        self.history_rows_container = QWidget()
        self.history_rows_layout = QVBoxLayout(self.history_rows_container)
        self.history_rows_layout.setContentsMargins(0, 0, 0, 0)
        self.history_rows_layout.setSpacing(8)
        self.history_frame_layout.addWidget(self.history_rows_container)

        self.panel_history_layout.addWidget(self.history_frame)
        self.panel_history_layout.addStretch()

        # default panel
        self.show_home()

        self.load_cart()
        self.load_history()

    def _format_rp(self, value: float) -> str:
        # tanpa titik/koma ribuan
        return f"Rp {int(value)}"

    def _set_visible_panel(self, panel_name: str):
        is_home = panel_name == "home"
        is_cart = panel_name == "cart"
        is_history = panel_name == "history"

        self.panel_dashboard.setVisible(is_home)
        self.panel_cart_scroll.setVisible(is_cart)
        self.panel_history_scroll.setVisible(is_history)
        self.search.setVisible(is_home)

    def show_home(self):
        self._set_visible_panel("home")
        self.panel_dashboard.show()
        self.load_data()

    def show_cart(self):
        self._set_visible_panel("cart")
        self.load_cart()

    def show_history(self):
        self._set_visible_panel("history")
        self.load_history()

    def refresh_stats(self):
        self.load_data()
        self.load_cart()
        self.load_history()

    def show_book_detail(self, book):
        dialog = BookDetailDialog(book, self)
        dialog.exec()

    def clear_receipt(self):
        self.receipt_frame.hide()
        if hasattr(self, "checkout_status_box"):
            self.checkout_status_box.setChecked(False)
            self.checkout_status_box.setText("Checkout belum dilakukan")
        self.checkout_status_label.setText("")
        self.receipt_meta_label.setText("")
        while self.receipt_rows_layout.count():
            item = self.receipt_rows_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_checkout_receipt(self, items, total):
        while self.receipt_rows_layout.count():
            item = self.receipt_rows_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        total_items = sum(int(item[4]) for item in items)
        self.checkout_status_label.setText("Checkout Berhasil")
        self.receipt_meta_label.setText(
            f"{total_items} item selesai diproses | Total pembayaran: {self._format_rp(float(total))}"
        )

        for _, judul, harga, _, jumlah, subtotal in items:
            row = QFrame()
            row.setObjectName("buyerCard")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 8, 10, 8)
            row_layout.setSpacing(10)

            detail = QLabel(f"{judul}\n{jumlah} x {self._format_rp(float(harga))}")
            detail.setStyleSheet("color:#5A4127; font-weight:800;")

            lbl_subtotal = QLabel(self._format_rp(float(subtotal)))
            lbl_subtotal.setStyleSheet("color:#10B981; font-weight:900;")

            row_layout.addWidget(detail, stretch=2)
            row_layout.addStretch(1)
            row_layout.addWidget(lbl_subtotal)
            self.receipt_rows_layout.addWidget(row)

        self.receipt_frame.show()

    def _get_cart_qty_map(self):
        """Return dict: {id_buku: jumlah} for current user."""
        if not self.user_id:
            return {}
        try:
            items = database_manager.cart_get_items(self.user_id)
            return {itm[0]: int(itm[4]) for itm in items}
        except Exception:
            return {}

    def load_data(self):
        books = database_manager.get_all_buku()
        keyword = self.search.text().lower()
        if keyword:
            books = [b for b in books if keyword in b[1].lower() or keyword in b[2].lower()]

        qty_map = self._get_cart_qty_map()

        try:
            total_tx = database_manager.get_total_transaksi_user(self.user_id)
        except Exception:
            total_tx = 0

        self.info.setText(
            f"Jumlah Buku Tersedia: {len(books)}   |   Total Transaksi Anda: {total_tx}"
        )

        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        row = 0
        col = 0
        for book in books:
            card = QFrame()
            card.setObjectName("buyerCard")
            card.setCursor(Qt.PointingHandCursor)
            card.setMinimumHeight(260)
            card.setMaximumWidth(360)

            card.mousePressEvent = lambda event, b=book: self.show_book_detail(b)

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(15, 15, 15, 15)
            card_layout.setSpacing(8)

            title_chip = QLabel("📖")
            title_chip.setStyleSheet("font-size:16px; color:#A67C52; font-weight:800;")

            judul = QLabel(book[1])
            judul.setWordWrap(True)
            judul.setStyleSheet(
                "color:#5A4127; font-size:17px; font-weight:800; border:none; line-height: 1.2;"
            )

            penulis = QLabel(f"✍ Penulis : {book[2]}")
            penulis.setWordWrap(True)
            penulis.setStyleSheet("color:#6F5A43; font-size:13px; border:none;")

            kategori = QLabel(f"📂 Kategori : {book[3]}")
            kategori.setWordWrap(True)
            kategori.setStyleSheet("color:#6F5A43; font-size:13px; border:none;")

            harga = QLabel(f"💰 Rp {int(book[4])}")
            harga.setStyleSheet("color:#A67C52; font-size:16px; font-weight:800; border:none;")

            stok = QLabel(f"📦 Stok : {book[5]}")
            stok.setStyleSheet("color:#6F5A43; font-size:13px; border:none;")

            badge_status = QLabel("Featured")
            badge_status.setStyleSheet(
                "background-color:#F4E7D8; color:#8A6A49; border:1px solid #E4D4C2; border-radius:10px; padding:4px 8px; font-size:10px; font-weight:700;"
            )

            title_row = QHBoxLayout()
            title_row.setSpacing(8)
            title_row.addWidget(title_chip)
            title_row.addWidget(judul)
            title_row.addStretch()
            title_row.addWidget(badge_status)
            card_layout.addLayout(title_row)

            card_layout.addWidget(penulis)
            card_layout.addWidget(kategori)
            card_layout.addStretch()
            card_layout.addWidget(harga)
            card_layout.addWidget(stok)

            # quantity control
            qty_row = QHBoxLayout()
            qty_row.setSpacing(8)

            btn_minus = QPushButton("-")
            btn_plus = QPushButton("+")
            for b in (btn_minus, btn_plus):
                b.setObjectName("btnQty")
                b.setFixedSize(52, 34)

            initial_qty = qty_map.get(book[0], 0)
            qty_label = QLabel(str(initial_qty))
            qty_label.setStyleSheet("color:#6F5A43; font-weight:800;")

            btn_minus.clicked.connect(
                lambda _, bid=book[0], lbl=qty_label: self.etalase_change_qty(bid, -1, lbl)
            )
            btn_plus.clicked.connect(
                lambda _, bid=book[0], lbl=qty_label: self.etalase_change_qty(bid, +1, lbl)
            )

            qty_row.addWidget(btn_minus)
            qty_row.addWidget(qty_label)
            qty_row.addWidget(btn_plus)
            qty_row.addStretch(1)

            card_layout.addLayout(qty_row)

            self.grid.addWidget(card, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

    def etalase_change_qty(self, id_buku: int, delta: int, qty_label: QLabel):
        if not self.user_id:
            return
        self.clear_receipt()
        try:
            database_manager.cart_add_or_update(self.user_id, id_buku, qty_delta=delta)
        except Exception:
            return
        qty_map = self._get_cart_qty_map()
        qty_label.setText(str(qty_map.get(id_buku, 0)))
        self.load_cart()

    def load_cart(self):
        while self.cart_rows_layout.count():
            item = self.cart_rows_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.user_id:
            self.cart_total_label.setText("Total Bayar: Rp 0")
            self.btn_checkout.setEnabled(False)
            return

        try:
            items = database_manager.cart_get_items(self.user_id)
        except Exception:
            items = []

        total = 0.0
        if not items:
            empty = QLabel("Keranjang masih kosong.")
            empty.setStyleSheet("color:#7A6651; font-weight:700;")
            self.cart_rows_layout.addWidget(empty)
            self.btn_checkout.setEnabled(False)
        else:
            self.btn_checkout.setEnabled(True)
            for (id_buku, judul, harga, stok, jumlah, subtotal) in items:
                total += float(subtotal)

                row = QFrame()
                row.setObjectName("buyerCard")
                row_layout = QHBoxLayout(row)
                row_layout.setContentsMargins(10, 10, 10, 10)
                row_layout.setSpacing(10)

                lbl_title = QLabel(f"{judul}")
                lbl_title.setStyleSheet("font-weight:900; color:#5A4127;")

                lbl_price = QLabel(self._format_rp(float(harga)))
                lbl_price.setStyleSheet("color:#A67C52; font-weight:900;")

                btn_minus = QPushButton("-")
                btn_plus = QPushButton("+")
                for b in (btn_minus, btn_plus):
                    b.setObjectName("btnQty")
                    b.setFixedSize(52, 34)

                qty_label = QLabel(str(jumlah))
                qty_label.setStyleSheet("color:#6F5A43; font-weight:800;")

                btn_minus.clicked.connect(lambda _, bid=id_buku: self.change_qty(bid, -1))
                btn_plus.clicked.connect(lambda _, bid=id_buku: self.change_qty(bid, +1))

                lbl_subtotal = QLabel(self._format_rp(float(subtotal)))
                lbl_subtotal.setStyleSheet("color:#10B981; font-weight:900;")

                row_layout.addWidget(lbl_title, stretch=2)
                row_layout.addWidget(lbl_price)
                row_layout.addStretch(1)

                qty_box = QHBoxLayout()
                qty_box.setSpacing(6)
                qty_box.addWidget(btn_minus)
                qty_box.addWidget(qty_label)
                qty_box.addWidget(btn_plus)
                row_layout.addLayout(qty_box)

                row_layout.addWidget(lbl_subtotal)
                self.cart_rows_layout.addWidget(row)

        self.cart_total_label.setText(f"Total Bayar: {self._format_rp(total)}")

    def load_history(self):
        while self.history_rows_layout.count():
            item = self.history_rows_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.user_id:
            empty = QLabel("Belum ada transaksi.")
            empty.setStyleSheet("color:#7A6651; font-weight:700;")
            self.history_rows_layout.addWidget(empty)
            return

        try:
            rows = database_manager.get_transaksi_user_items(self.user_id)
        except Exception:
            rows = []

        if not rows:
            empty = QLabel("Belum ada transaksi.")
            empty.setStyleSheet("color:#7A6651; font-weight:700;")
            self.history_rows_layout.addWidget(empty)
            return

        for id_transaksi, judul, jumlah, total_harga, tanggal in rows:
            row = QFrame()
            row.setObjectName("buyerCard")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 10, 10, 10)
            row_layout.setSpacing(10)

            lbl_title = QLabel(judul)
            lbl_title.setStyleSheet("font-weight:900; color:#5A4127;")

            lbl_meta = QLabel(f"#{id_transaksi} | {tanggal} | {jumlah} item")
            lbl_meta.setStyleSheet("color:#7A6651; font-weight:700;")

            lbl_total = QLabel(self._format_rp(float(total_harga)))
            lbl_total.setStyleSheet("color:#10B981; font-weight:900;")

            detail_box = QVBoxLayout()
            detail_box.setSpacing(3)
            detail_box.addWidget(lbl_title)
            detail_box.addWidget(lbl_meta)

            row_layout.addLayout(detail_box, stretch=2)
            row_layout.addStretch(1)
            row_layout.addWidget(lbl_total)

            self.history_rows_layout.addWidget(row)

    def change_qty(self, id_buku: int, delta: int):
        if not self.user_id:
            return
        self.clear_receipt()
        try:
            database_manager.cart_add_or_update(self.user_id, id_buku, qty_delta=delta)
        except Exception:
            return
        self.load_cart()

    def checkout(self):
        if not self.user_id:
            return
        try:
            checkout_items = database_manager.cart_get_items(self.user_id)
        except Exception:
            checkout_items = []

        try:
            total = database_manager.checkout_cart(self.user_id)
        except Exception:
            self.checkout_status_box.setChecked(False)
            self.checkout_status_box.setText("Checkout gagal")
            QMessageBox.warning(self, "Checkout Gagal", "Keranjang kosong atau stok tidak mencukupi.")
            return

        self.checkout_status_box.setChecked(True)
        self.checkout_status_box.setText("Checkout berhasil")
        self.show_checkout_receipt(checkout_items, total)
        self.load_cart()
        self.load_history()
        self.load_data()

