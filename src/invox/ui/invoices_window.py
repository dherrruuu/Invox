from __future__ import annotations

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QMessageBox, QPushButton

from ..services.invoice_service import InvoiceService
from .dialogs.invoice_dialog import InvoiceDialog
from .ui_helpers import centered_item, make_table, plain_item

class InvoicesWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invoices Management")
        self.service = InvoiceService()
        self.layout = QtWidgets.QVBoxLayout(self)

        toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search invoices")
        self.search_input.textChanged.connect(self.load_invoices)
        self.btn_add_invoice = QPushButton("Add Invoice")
        self.btn_add_invoice.clicked.connect(self.add_invoice)
        self.btn_delete = QPushButton("Delete Invoice")
        self.btn_delete.clicked.connect(self.delete_invoice)
        toolbar.addWidget(self.search_input, 1)
        toolbar.addWidget(self.btn_add_invoice)
        toolbar.addWidget(self.btn_delete)
        self.layout.addLayout(toolbar)

        self.table = QtWidgets.QTableWidget()
        make_table(self.table, ["Invoice Number", "Date", "Customer", "Total Amount", "Status"])
        self.layout.addWidget(self.table)

        self.load_invoices()

    def load_invoices(self, *_args):
        invoices = self.service.list_invoices()
        query = self.search_input.text().strip().lower()
        if query:
            invoices = [invoice for invoice in invoices if query in str(invoice.invoice_code).lower() or query in str(invoice.customer.name).lower()]
        self.table.setRowCount(len(invoices))
        for row, invoice in enumerate(invoices):
            self.table.setItem(row, 0, centered_item(str(invoice.invoice_code)))
            self.table.setItem(row, 1, centered_item(invoice.invoice_date.strftime("%Y-%m-%d")))
            self.table.setItem(row, 2, plain_item(invoice.customer.name if invoice.customer else ""))
            self.table.setItem(row, 3, centered_item(f"{invoice.grand_total:.2f}"))
            self.table.setItem(row, 4, centered_item(invoice.status))

    def add_invoice(self, *_args):
        dialog = InvoiceDialog(parent=self)
        if dialog.exec():
            self.load_invoices()

    def delete_invoice(self, *_args):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select an invoice to delete.")
            return
        invoice_code = self.table.item(selected_row, 0).text()
        invoice = next((item for item in self.service.list_invoices() if str(item.invoice_code) == invoice_code), None)
        if invoice and QMessageBox.question(self, "Delete", "Delete selected invoice?") == QMessageBox.StandardButton.Yes:
            self.service.delete_invoice(invoice.id)
            self.load_invoices()