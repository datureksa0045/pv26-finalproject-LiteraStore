from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                               QMessageBox, QFormLayout, QHBoxLayout, QWidget,
                               QFrame)
from PySide6.QtCore import Qt
from models import database_manager


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login LiteraStore")
        self.resize(1100, 680)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FFF8F0, stop:1 #E9D9C7);
            }
            QLabel { color: #5A4127; }
            QLineEdit {
                border: 1px solid #D8C8B6;
                border-radius: 12px;
                padding: 10px 12px;
                background-color: #FFFDFB;
                color: #4B3522;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #B98B5A;
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #A67C52;
                color: #FFFDF9;
                border: none;
                border-radius: 12px;
                padding: 10px 14px;
                font-weight: 700;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #8C6643;
            }
            QPushButton#btnBack {
                background-color: #EFE2D1;
                color: #5A4127;
                border: 1px solid #DCCBB4;
            }
            QPushButton#btnBack:hover {
                background-color: #E5D4BE;
            }
            QPushButton#btnLogin {
                background-color: #A67C52;
                color: #FFFDF9;
                border: 1px solid #A67C52;
            }
            QPushButton#btnLogin:hover {
                background-color: #8C6643;
            }
            QFrame#card {
                background-color: rgba(255, 253, 249, 0.96);
                border: 1px solid #E6D8C8;
                border-radius: 24px;
            }
        """)

        self.user_data = None

        outer_layout = QHBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(self.create_login_page(), 1)

    def create_login_page(self):
        page = QWidget()
        page.setObjectName("loginFormPage")
        page.setStyleSheet("QWidget#loginFormPage { background: transparent; }")

        main_layout = QHBoxLayout(page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        left = QFrame()
        left.setObjectName("heroPanel")
        left.setStyleSheet("QFrame#heroPanel { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C69A72, stop:1 #9A744F); border: none; }")
        left.setMinimumWidth(520)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(35, 35, 35, 35)
        left_layout.setSpacing(14)

        left_badge = QLabel("📚 LiteraStore")
        left_badge.setStyleSheet("font-size: 13px; font-weight: 800; color: #FFF8EE; letter-spacing: 2px;")
        left_title = QLabel("Masuk ke akun kamu\nuntuk melanjutkan")
        left_title.setWordWrap(True)
        left_title.setStyleSheet("font-size: 30px; font-weight: 800; color: #FFFDF9; line-height: 1.2;")
        left_desc = QLabel("Masuk untuk melihat etalase buku, keranjang, dan riwayat belanjamu.")
        left_desc.setWordWrap(True)
        left_desc.setStyleSheet("font-size: 14px; color: #FFF6EA; line-height: 1.5;")

        left_layout.addWidget(left_badge)
        left_layout.addStretch(1)
        left_layout.addWidget(left_title)
        left_layout.addWidget(left_desc)
        left_layout.addStretch(1)

        right = QWidget()
        right.setStyleSheet("background: transparent;")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(40, 40, 40, 40)
        right_layout.setSpacing(16)

        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet("QFrame#card { background-color: rgba(255, 253, 249, 0.96); border: 1px solid #E6D8C8; border-radius: 24px; box-shadow: 0 4px 18px rgba(91, 69, 45, 0.12); }")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(14)

        self.label_title = QLabel("Login LiteraStore")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 24px; font-weight: 800; color: #5A4127;")

        subtitle = QLabel("Masukkan username dan password untuk melanjutkan.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #7A6651; font-size: 13px; line-height: 1.4;")

        card_layout.addWidget(self.label_title)
        card_layout.addWidget(subtitle)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Username")
        self.txt_username.setClearButtonEnabled(True)
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Password")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.returnPressed.connect(self.login)

        form_layout.addRow("Username:", self.txt_username)
        form_layout.addRow("Password:", self.txt_password)

        card_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.setContentsMargins(0, 4, 0, 0)

        self.btn_login = QPushButton("Login")
        self.btn_login.setObjectName("btnLogin")
        self.btn_login.setMinimumHeight(46)
        self.btn_login.setMinimumWidth(120)
        self.btn_login.setDefault(True)
        self.btn_login.setStyleSheet(
            "QPushButton {"
            "background-color: #A97744; color: #FFFDF9; border: 1px solid #A97744;"
            "border-radius: 12px; padding: 10px 16px; font-weight: 700; font-size: 13px;"
            "}"
            "QPushButton:hover { background-color: #8E6641; }"
        )
        self.btn_login.clicked.connect(self.login)

        self.lbl_hint = QLabel("Sudah mengisi username & password? Klik tombol di atas untuk lanjut.")
        self.lbl_hint.setAlignment(Qt.AlignCenter)
        self.lbl_hint.setWordWrap(True)
        self.lbl_hint.setStyleSheet("color: #8C745C; font-size: 12px; line-height: 1.4;")
        card_layout.addWidget(self.lbl_hint)

        btn_layout.addWidget(self.btn_login)
        card_layout.addLayout(btn_layout)

        self.btn_login.setToolTip("Klik untuk masuk ke dashboard sesuai role Anda")

        right_layout.addStretch(1)
        right_layout.addWidget(card)
        right_layout.addStretch(1)

        main_layout.addWidget(left)
        main_layout.addWidget(right, 1)
        return page

    def login(self):
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Login Gagal", "Username dan password harus diisi.")
            return

        user = database_manager.validate_user(username, password)
        if not user:
            QMessageBox.critical(self, "Login Gagal", "Username atau password tidak valid.")
            return

        self.user_data = {
            "id": user[0],
            "username": user[1],
            "role": user[3]
        }
        self.accept()
