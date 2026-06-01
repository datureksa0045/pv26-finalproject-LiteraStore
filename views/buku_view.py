from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QDialog, QFormLayout)
from PySide6.QtCore import Qt
from models import database_manager

class BukuDialog(QDialog):
    def __init__(self, parent=None, data_buku=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Buku Baru" if not data_buku else "Edit Data Buku")
        self.resize(400, 300)
        self.setModal(True)
        
        form_layout = QFormLayout(self)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(20)
        
        self.txt_judul = QLineEdit()
        self.txt_penulis = QLineEdit()
        self.cb_kategori = QComboBox()
        self.cb_kategori.addItems(["Fiksi", "Non-Fiksi", "Teknologi", "Sains", "Komik"])
        self.txt_harga = QLineEdit()
        self.txt_stok = QLineEdit()
        
        form_layout.addRow("Judul Buku :", self.txt_judul)
        form_layout.addRow("Penulis :", self.txt_penulis)
        form_layout.addRow("Kategori :", self.cb_kategori)
        form_layout.addRow("Harga Satuan (Rp) :", self.txt_harga)
        form_layout.addRow("Stok Buku :", self.txt_stok)
        
        self.btn_simpan = QPushButton("Simpan")
        self.btn_simpan.clicked.connect(self.validate_and_save)
        form_layout.addRow(self.btn_simpan)
        
        self.id_buku = None
        if data_buku:
            self.id_buku = data_buku[0]
            self.txt_judul.setText(data_buku[1])
            self.txt_penulis.setText(data_buku[2])
            self.cb_kategori.setCurrentText(data_buku[3])
            self.txt_harga.setText(str(data_buku[4]))
            self.txt_stok.setText(str(data_buku[5]))

    def validate_and_save(self):
        judul = self.txt_judul.text().strip()
        penulis = self.txt_penulis.text().strip()
        harga_raw = self.txt_harga.text().strip()
        stok_raw = self.txt_stok.text().strip()
        
        if not judul or not penulis or not harga_raw or not stok_raw:
            QMessageBox.warning(self, "Validasi Gagal", "Semua field wajib diisi!")
            return
            
        try:
            harga = float(harga_raw)
            stok = int(stok_raw)
            if harga <= 0 or stok < 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Kesalahan Input", "Harga & Stok harus bernilai angka positif valid!")
            return
            
        if self.id_buku is None:
            database_manager.insert_buku(judul, penulis, self.cb_kategori.currentText(), harga, stok)
        else:
            database_manager.update_buku(self.id_buku, judul, penulis, self.cb_kategori.currentText(), harga, stok)
            
        self.accept()

class ManajemenBukuPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        
        title = QLabel("📚 Manajemen Stok & Katalog Buku")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1E293B; margin-bottom: 10px;")
        layout.addWidget(title)
        
        search_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Cari Judul Buku / Penulis...")
        self.txt_search.textChanged.connect(self.load_data)
        
        self.cb_filter = QComboBox()
        self.cb_filter.addItems(["Semua Kategori", "Fiksi", "Non-Fiksi", "Teknologi", "Sains", "Komik"])
        self.cb_filter.currentTextChanged.connect(self.load_data)
        
        self.cb_sort = QComboBox()
        self.cb_sort.addItems(["ID (Asc)", "ID (Desc)", "Judul (A-Z)", "Harga (Termurah)", "Stok (Tersisa)"])
        self.cb_sort.currentTextChanged.connect(self.load_data)
        
        btn_tambah = QPushButton("+ Tambah Buku")
        btn_tambah.clicked.connect(self.action_tambah)
        
        search_layout.addWidget(QLabel("Cari :"))
        search_layout.addWidget(self.txt_search, stretch=2)
        search_layout.addWidget(QLabel("Kategori :"))
        search_layout.addWidget(self.cb_filter, stretch=1)
        search_layout.addWidget(QLabel("Urutkan :"))
        search_layout.addWidget(self.cb_sort, stretch=1)
        search_layout.addWidget(btn_tambah)
        layout.addLayout(search_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID Buku", "Judul Buku", "Penulis", "Kategori", "Harga", "Stok"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        actions_layout = QHBoxLayout()
        btn_edit = QPushButton("Edit Buku Terpilih")
        btn_edit.setStyleSheet("background-color: #F59E0B;")
        btn_edit.clicked.connect(self.action_edit)
        
        btn_hapus = QPushButton("Hapus Buku Terpilih")
        btn_hapus.setObjectName("btnHapus")
        btn_hapus.clicked.connect(self.action_hapus)
        
        actions_layout.addWidget(btn_edit)
        actions_layout.addWidget(btn_hapus)
        actions_layout.addStretch()
        layout.addLayout(actions_layout)
        
        self.load_data()

    def load_data(self):
        books = database_manager.get_all_buku(self.txt_search.text().strip(), self.cb_filter.currentText(), self.cb_sort.currentText())
        self.table.setRowCount(0)
        for row_idx, book in enumerate(books):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(book):
                item = QTableWidgetItem(str(value))
                if col_idx in [0, 4, 5]: 
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row_idx, col_idx, item)

    def action_tambah(self):
        dialog = BukuDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_data()

    def action_edit(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Pilih Data", "Silakan pilih baris tabel dahulu!")
            return
            
        data_buku = [
            int(self.table.item(selected_row, 0).text()),
            self.table.item(selected_row, 1).text(),
            self.table.item(selected_row, 2).text(),
            self.table.item(selected_row, 3).text(),
            float(self.table.item(selected_row, 4).text()),
            int(self.table.item(selected_row, 5).text())
        ]
        
        dialog = BukuDialog(self, data_buku)
        if dialog.exec() == QDialog.Accepted:
            self.load_data()

    def action_hapus(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Pilih Data", "Silakan pilih baris tabel!")
            return
            
        id_buku = int(self.table.item(selected_row, 0).text())
        judul = self.table.item(selected_row, 1).text()
        
        confirm = QMessageBox.question(self, "Konfirmasi Hapus", f"Hapus permanen buku '{judul}'?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            database_manager.delete_buku(id_buku)
            self.load_data()