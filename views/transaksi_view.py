from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QFileDialog,
    QDialog,
    QFormLayout,
)
from PySide6.QtCore import Qt, QDate

from models import database_manager
from utils import exporters


class TransaksiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Transaksi")
        self.resize(520, 180)
        self.setModal(True)
        self.transaction_data = None

        layout = QFormLayout(self)
        layout.setVerticalSpacing(14)
        layout.setHorizontalSpacing(18)

        self.cb_buku = QComboBox()
        self.txt_jumlah = QLineEdit()
        self.txt_jumlah.setPlaceholderText("Jumlah Qty")

        layout.addRow("Pilih Buku :", self.cb_buku)
        layout.addRow("Jumlah :", self.txt_jumlah)

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Batal")
        btn_save = QPushButton("Proses Transaksi")
        btn_save.setStyleSheet("background-color: #10B981;")
        btn_cancel.clicked.connect(self.reject)
        btn_save.clicked.connect(self.validate_and_accept)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addRow(btn_layout)

        self.load_buku_combobox()

    def load_buku_combobox(self):
        self.cb_buku.clear()
        books = database_manager.get_all_buku()
        for book in books:
            self.cb_buku.addItem(
                f"{book[0]} - {book[1]} (Stok: {book[5]} | Rp {book[4]})",
                userData=book,
            )

    def validate_and_accept(self):
        if self.cb_buku.currentIndex() < 0:
            QMessageBox.warning(self, "Data Buku Kosong", "Tidak ada buku yang tersedia.")
            return

        book_data = self.cb_buku.currentData()
        id_buku, _, _, _, harga_satuan, stok_sekarang = book_data[:6]
        jumlah_raw = self.txt_jumlah.text().strip()

        if not jumlah_raw:
            QMessageBox.warning(self, "Validasi Gagal", "Jumlah beli harus diisi!")
            return

        try:
            jumlah = int(jumlah_raw)
            if jumlah <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Error", "Jumlah harus berupa angka bulat positif!")
            return

        if jumlah > stok_sekarang:
            QMessageBox.warning(self, "Stok Kurang", "Stok buku tidak mencukupi!")
            return

        self.transaction_data = (id_buku, jumlah, jumlah * harga_satuan)
        self.accept()


class TransaksiPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel("Formulir Transaksi Kasir & Riwayat Penjualan")
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #1E293B; margin-bottom: 10px;"
        )
        layout.addWidget(title)

        action_layout = QHBoxLayout()
        btn_proses = QPushButton("+ Tambah Transaksi")
        btn_proses.setStyleSheet("background-color: #10B981;")
        btn_proses.clicked.connect(self.proses_transaksi)
        action_layout.addWidget(btn_proses)
        action_layout.addStretch()
        layout.addLayout(action_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                "ID Transaksi",
                "Judul Buku Terjual",
                "Jumlah Jual",
                "Total Harga (Rp)",
                "Tanggal",
            ]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        export_layout = QHBoxLayout()
        btn_export_csv = QPushButton("Export Log Penjualan (CSV)")
        btn_export_csv.setStyleSheet("background-color: #4F46E5;")
        btn_export_csv.clicked.connect(self.export_csv)

        btn_export_pdf = QPushButton("Export Log Penjualan (PDF)")
        btn_export_pdf.setStyleSheet("background-color: #7C3AED;")
        btn_export_pdf.clicked.connect(self.export_pdf)

        export_layout.addWidget(btn_export_csv)
        export_layout.addWidget(btn_export_pdf)
        export_layout.addStretch()
        layout.addLayout(export_layout)

        self.load_transaksi()

    def load_buku_combobox(self):
        # Dipertahankan agar pemanggilan dari main.py tetap kompatibel.
        pass

    def load_transaksi(self):
        transactions = database_manager.get_all_transaksi()
        self.table.setRowCount(0)
        for row_idx, tx in enumerate(transactions):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(tx):
                item = QTableWidgetItem(str(value))
                if col_idx in [0, 2, 3]:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row_idx, col_idx, item)

    def proses_transaksi(self):
        dialog = TransaksiDialog(self)
        if dialog.exec() != QDialog.Accepted or not dialog.transaction_data:
            return

        id_buku, jumlah, total_harga = dialog.transaction_data
        database_manager.insert_transaksi(
            id_buku,
            jumlah,
            total_harga,
            QDate.currentDate().toString("yyyy-MM-dd"),
        )
        self.load_transaksi()

    def export_csv(self):
        transactions = database_manager.get_all_transaksi()
        if not transactions:
            QMessageBox.warning(self, "Batal Export", "Tidak ada data transaksi!")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Simpan File Ekspor", "", "CSV Files (*.csv)"
        )
        if file_path:
            if not file_path.lower().endswith(".csv"):
                file_path += ".csv"
            success, msg = exporters.export_to_csv(file_path, transactions)
            if success:
                QMessageBox.information(self, "Berhasil", "Laporan CSV berhasil diexport!")
            else:
                QMessageBox.critical(self, "Gagal", f"Gagal mengekspor data: {msg}")

    def export_pdf(self):
        transactions = database_manager.get_all_transaksi()
        if not transactions:
            QMessageBox.warning(self, "Batal Export", "Tidak ada data transaksi!")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Simpan File PDF", "", "PDF Files (*.pdf)"
        )
        if file_path:
            if not file_path.lower().endswith(".pdf"):
                file_path += ".pdf"
            success, msg = exporters.export_to_pdf(file_path, transactions)
            if success:
                QMessageBox.information(self, "Berhasil", "Laporan PDF berhasil diexport!")
            else:
                QMessageBox.critical(self, "Gagal", f"Gagal mengekspor PDF: {msg}")
