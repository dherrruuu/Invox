from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from .db.connection import init_database
from .services.auth_service import AuthService
from .ui.login_window import LoginWindow
from .ui.main_window import MainWindow
from .ui.theme import APP_STYLESHEET


class App:
    def __init__(self):
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        self.qt_app.setStyleSheet(APP_STYLESHEET)
        init_database()
        self.auth_service = AuthService()
        self.auth_service.seed_default_admin()
        self.main_window = None

    def run(self):
        while True:
            login = LoginWindow(self.auth_service)
            if login.exec() != LoginWindow.DialogCode.Accepted:
                return 0
            self.main_window = MainWindow(login.current_user)
            logout_state = {"requested": False}

            def _mark_logout():
                logout_state["requested"] = True

            self.main_window.logout_requested.connect(_mark_logout)
            self.main_window.show()
            exit_code = self.qt_app.exec()
            if not logout_state["requested"]:
                return exit_code


if __name__ == "__main__":
    raise SystemExit(App().run())