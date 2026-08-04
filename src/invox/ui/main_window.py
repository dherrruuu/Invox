from __future__ import annotations

from datetime import date

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QFrame, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMainWindow, QMessageBox, QPushButton, QScrollArea, QStackedWidget, QTextEdit, QVBoxLayout, QWidget

from ..constants import APP_NAME, APP_TAGLINE, LUXURY_PRIMARY, WINDOW_HEIGHT, WINDOW_WIDTH
from ..services.backup_service import BackupService
from ..services.company_service import CompanyService
from ..services.customer_service import CustomerService
from ..services.invoice_service import InvoiceService
from ..services.product_service import ProductService
from ..services.quotation_service import QuotationService
from ..services.report_service import ReportService
from .customers_window import CustomersWindow
from .invoices_window import InvoicesWindow
from .products_window import ProductsWindow
from .quotations_window import QuotationsWindow


class StatCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str = ""):
        super().__init__()
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"color: {LUXURY_PRIMARY}; font-size: 10pt; font-weight: 600;")
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 22pt; font-weight: 700;")
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("Muted")
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)

    def set_value(self, value: str):
        self.value_label.setText(value)


class DashboardPage(QWidget):
    def __init__(self, report_service: ReportService, company_service: CompanyService):
        super().__init__()
        self.report_service = report_service
        self.company_service = company_service
        layout = QVBoxLayout(self)
        hero = QFrame()
        hero.setObjectName("Card")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(20, 20, 20, 20)
        title_block = QVBoxLayout()
        self.brand = QLabel(f"{APP_NAME} - Dashboard")
        self.brand.setStyleSheet("font-size: 24pt; font-weight: 700;")
        self.tagline = QLabel(APP_TAGLINE)
        self.tagline.setObjectName("Muted")
        title_block.addWidget(self.brand)
        title_block.addWidget(self.tagline)
        hero_layout.addLayout(title_block)
        hero_layout.addStretch(1)
        self.company_label = QLabel("")
        self.company_label.setStyleSheet(f"color: {LUXURY_PRIMARY}; font-size: 11pt; font-weight: 600;")
        hero_layout.addWidget(self.company_label)

        self.sales_card = StatCard("Total Sales", "0.00", "All invoices")
        self.bills_card = StatCard("Total Bills", "0", "Issued documents")
        self.customers_card = StatCard("Total Customers", "0", "Active records")
        self.revenue_card = StatCard("Monthly Revenue", "0.00", "Current month")

        stats = QHBoxLayout()
        stats.addWidget(self.sales_card)
        stats.addWidget(self.bills_card)
        stats.addWidget(self.customers_card)
        stats.addWidget(self.revenue_card)

        self.summary_label = QLabel("")
        self.summary_label.setObjectName("Muted")
        self.summary_label.setWordWrap(True)

        layout.addWidget(hero)
        layout.addLayout(stats)
        layout.addWidget(self.summary_label)
        layout.addStretch(1)
        self.refresh()

    def refresh(self):
        company = self.company_service.get_profile()
        report = self.report_service.generate_sales_report(date(2000, 1, 1), date.today())
        customers = self.report_service.generate_customer_report()
        self.company_label.setText(company.company_name)
        self.sales_card.set_value(f"{report['total_sales']:.2f}")
        self.bills_card.set_value(str(len(report["invoices"])))
        self.customers_card.set_value(str(customers["total_customers"]))
        self.revenue_card.set_value(f"{report['total_sales']:.2f}")
        self.summary_label.setText(f"Dashboard ready. Invoices: {len(report['invoices'])}. Customers: {customers['total_customers']}.")


class SettingsPage(QWidget):
    def __init__(self, company_service: CompanyService):
        super().__init__()
        self.company_service = company_service
        layout = QVBoxLayout(self)
        card = QFrame()
        card.setObjectName("Card")
        form = QFormLayout(card)
        self.company_name_input = QLineEdit()
        self.address_input = QTextEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.gst_input = QLineEdit()
        self.bank_input = QTextEdit()
        self.terms_input = QTextEdit()
        form.addRow("Company Name", self.company_name_input)
        form.addRow("Address", self.address_input)
        form.addRow("Phone", self.phone_input)
        form.addRow("Email", self.email_input)
        form.addRow("GST Number", self.gst_input)
        form.addRow("Bank Details", self.bank_input)
        form.addRow("Terms & Conditions", self.terms_input)
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(card)
        layout.addWidget(self.save_button)
        layout.addStretch(1)
        self.refresh()

    def refresh(self):
        profile = self.company_service.get_profile()
        self.company_name_input.setText(profile.company_name)
        self.address_input.setPlainText(profile.address)
        self.phone_input.setText(profile.phone_number)
        self.email_input.setText(profile.email)
        self.gst_input.setText(profile.gst_number)
        self.bank_input.setPlainText(profile.bank_details)
        self.terms_input.setPlainText(profile.terms_and_conditions)

    def save_settings(self, *_args):
        self.company_service.update_profile(
            company_name=self.company_name_input.text().strip(),
            address=self.address_input.toPlainText().strip(),
            phone_number=self.phone_input.text().strip(),
            email=self.email_input.text().strip(),
            gst_number=self.gst_input.text().strip(),
            bank_details=self.bank_input.toPlainText().strip(),
            terms_and_conditions=self.terms_input.toPlainText().strip(),
        )
        QMessageBox.information(self, "Saved", "Company settings updated.")


class ReportsPage(QWidget):
    def __init__(self, report_service: ReportService):
        super().__init__()
        self.report_service = report_service
        layout = QVBoxLayout(self)
        self.summary = QLabel("")
        self.summary.setWordWrap(True)
        self.summary.setObjectName("Muted")
        self.refresh_button = QPushButton("Refresh Reports")
        self.refresh_button.clicked.connect(self.refresh)
        layout.addWidget(self.summary)
        layout.addWidget(self.refresh_button)
        layout.addStretch(1)
        self.refresh()

    def refresh(self, *_args):
        sales = self.report_service.generate_sales_report(date(2000, 1, 1), date.today())
        quotations = self.report_service.generate_quotation_report(date(2000, 1, 1), date.today())
        self.summary.setText(
            f"Sales total: {sales['total_sales']:.2f}\n"
            f"Invoices: {len(sales['invoices'])}\n"
            f"Quotations: {quotations['total_quotations']} | Value: {quotations['total_value']:.2f}"
        )


class BackupPage(QWidget):
    def __init__(self, backup_service: BackupService):
        super().__init__()
        self.backup_service = backup_service
        layout = QVBoxLayout(self)
        self.status_label = QLabel("Create a secure copy of the database or restore from an existing backup.")
        self.status_label.setWordWrap(True)
        self.create_button = QPushButton("Create Backup")
        self.restore_button = QPushButton("Restore Backup")
        self.create_button.clicked.connect(self.create_backup)
        self.restore_button.clicked.connect(self.restore_backup)
        layout.addWidget(self.status_label)
        layout.addWidget(self.create_button)
        layout.addWidget(self.restore_button)
        layout.addStretch(1)

    def create_backup(self, *_args):
        backup_path = self.backup_service.create_backup()
        self.status_label.setText(f"Backup created at {backup_path}")
        QMessageBox.information(self, "Backup Created", str(backup_path))

    def restore_backup(self, *_args):
        backup_file, _ = QFileDialog.getOpenFileName(self, "Restore Backup", str(self.backup_service.backup_dir), "SQLite Database (*.db)")
        if backup_file:
            restored = self.backup_service.restore_backup(backup_file)
            QMessageBox.information(self, "Backup Restored", f"Database restored to {restored}")


class MainWindow(QMainWindow):
    logout_requested = pyqtSignal()

    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.customer_service = CustomerService()
        self.product_service = ProductService()
        self.invoice_service = InvoiceService()
        self.quotation_service = QuotationService()
        self.report_service = ReportService()
        self.company_service = CompanyService()
        self.backup_service = BackupService()
        self.setWindowTitle(f"{APP_NAME} - {self.current_user.username}")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self._build_ui()

    def _build_ui(self):
        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(18)

        sidebar = QFrame()
        sidebar.setObjectName("Card")
        sidebar.setFixedWidth(230)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(10)

        brand = QLabel(APP_NAME)
        brand.setStyleSheet(f"font-size: 22pt; font-weight: 800; color: {LUXURY_PRIMARY};")
        sidebar_layout.addWidget(brand)
        sidebar_layout.addWidget(QLabel("ERP Billing Suite"))

        self.nav_list = QListWidget()
        self.nav_items = [
            "Dashboard",
            "Invoices",
            "Quotations",
            "Customers",
            "Products",
            "Reports",
            "Settings",
            "Backup",
            "Logout",
        ]
        self.nav_list.addItems(self.nav_items)
        self.nav_list.currentRowChanged.connect(self._change_page)
        sidebar_layout.addWidget(self.nav_list, 1)

        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage(self.report_service, self.company_service)
        self.invoices_page = InvoicesWindow()
        self.quotations_page = QuotationsWindow()
        self.customers_page = CustomersWindow()
        self.products_page = ProductsWindow()
        self.reports_page = ReportsPage(self.report_service)
        self.settings_page = SettingsPage(self.company_service)
        self.backup_page = BackupPage(self.backup_service)

        for page in [
            self.dashboard_page,
            self.invoices_page,
            self.quotations_page,
            self.customers_page,
            self.products_page,
            self.reports_page,
            self.settings_page,
            self.backup_page,
        ]:
            self.stack.addWidget(page)

        self.stack.addWidget(QWidget())

        layout.addWidget(sidebar)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.nav_list.setCurrentRow(0)

    def _change_page(self, index: int):
        if index < 0:
            return
        if index == 8:
            self.logout_requested.emit()
            return
        self.stack.setCurrentIndex(index)
        if index == 0:
            self.dashboard_page.refresh()
        elif index == 5:
            self.reports_page.refresh()
        elif index == 6:
            self.settings_page.refresh()

    def request_logout(self):
        self.logout_requested.emit()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Logout", "Close INVOX and return to the login screen?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.request_logout()
            event.accept()
        else:
            event.ignore()