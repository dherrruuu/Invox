from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QDialog, QFormLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from ..constants import APP_NAME, LUXURY_PRIMARY
from ..services.auth_service import AuthService


class LoginWindow(QDialog):
    def __init__(self, auth_service: AuthService, parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.current_user = None
        self.setWindowTitle(f"{APP_NAME} | Login")
        self.setMinimumWidth(440)
        self.setModal(True)
        self._build_ui()
        self._load_remembered_user()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        header = QLabel(f"{APP_NAME}")
        header.setStyleSheet(f"font-size: 26pt; font-weight: 700; color: {LUXURY_PRIMARY};")
        subtitle = QLabel("Luxury billing, quotations, and ERP control")
        subtitle.setObjectName("Muted")

        card = QFrame()
        card.setObjectName("Card")
        form = QFormLayout(card)
        form.setContentsMargins(20, 20, 20, 20)
        form.setVerticalSpacing(14)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.remember_me = QCheckBox("Remember me")
        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("color: #ffb4b4;")

        self.login_button = QPushButton("Sign In")
        self.login_button.clicked.connect(self._attempt_login)
        self.username_edit.returnPressed.connect(self._attempt_login)
        self.password_edit.returnPressed.connect(self._attempt_login)

        form.addRow("Username", self.username_edit)
        form.addRow("Password", self.password_edit)
        form.addRow("", self.remember_me)

        footer = QHBoxLayout()
        footer.addWidget(self.message_label, 1)
        footer.addWidget(self.login_button)

        root.addWidget(header)
        root.addWidget(subtitle)
        root.addWidget(card)
        root.addLayout(footer)

    def _load_remembered_user(self):
        remembered = self.auth_service.load_remembered_user()
        if remembered:
            self.username_edit.setText(remembered)
            self.remember_me.setChecked(True)
            self.password_edit.setFocus()

    def _attempt_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        if not username or not password:
            self.message_label.setText("Enter a username and password.")
            return
        user = self.auth_service.authenticate(username, password, self.remember_me.isChecked())
        if user is None:
            self.message_label.setText("Invalid credentials.")
            return
        self.current_user = user
        self.accept()
