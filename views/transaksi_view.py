from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, QDate
from models import database_manager
from utils import exporters

class TransaksiPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        
        title = QLabel("🛒 Formulir Transaksi Kasir & Riwayat Penjualan")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1E293B; margin-bottom: 10px;")
        layout.addWidget(title)
        
        form_layout = QHBoxLayout()
        self.cb_buku = QComboBox()
        self.txt_jumlah = QLineEdit()
        self.txt_jumlah.setPlaceholderText("Jumlah Qty")
        
        btn_proses = QPushButton("Proses Transaksi")
        btn_proses.setStyleSheet("background-color: #10B981;")
        btn_proses.clicked.connect(self.proses_transaksi)
        
        form_layout.addWidget(QLabel("Pilih Buku :"))
        form_layout.addWidget(self.cb_buku, stretch=3)
        form_layout.addWidget(QLabel("Jumlah :"))
        form_layout.addWidget(self.txt_jumlah, stretch=1)
        form_layout.addWidget(btn_proses)
        layout.addLayout(form_layout)

        self.lbl_detail = QLabel()
        self.lbl_detail.setStyleSheet("""
        font-size:14px;
        padding:10px;""")
        
        layout.addWidget(self.lbl_detail)
        self.lbl_total = QLabel("Total Bayar : Rp 0")
        self.lbl_total.setStyleSheet("""font-size:16px;font-weight:bold;""")
        layout.addWidget(self.lbl_total)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID Transaksi", "Judul Buku Terjual", "Jumlah Jual", "Total Harga (Rp)", "Tanggal"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        export_layout = QHBoxLayout()
        btn_export = QPushButton("📤 Export Log Penjualan (CSV)")
        btn_export.setStyleSheet("background-color: #4F46E5;")
        btn_export.clicked.connect(self.export_csv)
        export_layout.addWidget(btn_export)
        export_layout.addStretch()
        layout.addLayout(export_layout)
        
        self.cb_buku.currentIndexChanged.connect(
        self.update_info)
        self.txt_jumlah.textChanged.connect(
        self.update_total)
        
        self.load_buku_combobox()
        self.load_transaksi()

    def load_buku_combobox(self):
        self.cb_buku.clear()
        books = database_manager.get_all_buku()
        for b in books:
            self.cb_buku.addItem(f"{b[0]} - {b[1]} (Stok: {b[5]} | Rp {b[4]})", userData=b)

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
        if self.cb_buku.currentIndex() < 0:
            return
            
        book_data = self.cb_buku.currentData()
        id_buku, _, _, _, harga_satuan, stok_sekarang = book_data
        jumlah_raw = self.txt_jumlah.text().strip()
        
        if not jumlah_raw:
            QMessageBox.warning(self, "Validasi Gagal", "Jumlah beli harus diisi!")
            return
            
        try:
            jumlah = int(jumlah_raw)
            if jumlah <= 0: raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Error", "Jumlah harus berupa angka bulat positif!")
            return
            
        if jumlah > stok_sekarang:
            QMessageBox.warning(self, "Stok Kurang", "Stok buku tidak mencukupi!")
            return
            
        database_manager.insert_transaksi(id_buku, jumlah, jumlah * harga_satuan, QDate.currentDate().toString("yyyy-MM-dd"))
        self.txt_jumlah.clear()
        self.load_buku_combobox()
        self.load_transaksi()

    def export_csv(self):
        transactions = database_manager.get_all_transaksi()
        if not transactions:
            QMessageBox.warning(self, "Batal Export", "Tidak ada data transaksi!")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, "Simpan File Ekspor", "", "CSV Files (*.csv)")
        if file_path:
            success, msg = exporters.export_to_csv(file_path, transactions)
            if success:
                QMessageBox.information(self, "Berhasil", "Laporan berhasil diexport!")
            else:
                QMessageBox.critical(self, "Gagal", f"Gagal mengekspor data: {msg}")
    
    def update_info(self):
        data = self.cb_buku.currentData()
        if not data:
            return
        self.lbl_detail.setText(
            f"""
            Judul : {data[1]}
            Penulis : {data[2]}
            Kategori : {data[3]}
            Harga : Rp {data[4]:,.0f}
            Stok : {data[5]}
            """
        )

    def update_total(self):
        data = self.cb_buku.currentData()
        if not data:
            return
        try:
            jumlah = int(
                self.txt_jumlah.text()
            )
        except:
            jumlah = 0
            total = jumlah * data[4]
            
            self.lbl_total.setText(
                f"Total Bayar : Rp {total:,.0f}"
                )   