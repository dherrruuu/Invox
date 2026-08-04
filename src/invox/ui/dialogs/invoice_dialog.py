from __future__ import annotations

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QComboBox, QDateEdit, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout

from ...services.customer_service import CustomerService
from ...services.invoice_service import InvoiceService
from ..ui_helpers import centered_item, make_table, plain_item

class InvoiceDialog(QDialog):
    def __init__(self, parent=None):
        super(InvoiceDialog, self).__init__(parent)
        self.setWindowTitle("Invoice Dialog")
        self.setMinimumSize(980, 720)
        self.customer_service = CustomerService()
        self.invoice_service = InvoiceService()

        self.layout = QVBoxLayout(self)
        form = QFormLayout()

        self.invoice_number_input = QLineEdit()
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.customer_combo = QComboBox()
        self.discount_input = QLineEdit("0")
        self.notes_input = QLineEdit()

        form.addRow("Invoice Number", self.invoice_number_input)
        form.addRow("Invoice Date", self.date_edit)
        form.addRow("Customer", self.customer_combo)
        form.addRow("Discount", self.discount_input)
        form.addRow("Notes", self.notes_input)
        self.layout.addLayout(form)

        self.items_table = QTableWidget()
        make_table(self.items_table, ["Description", "Size", "Qty", "Rate", "GST %"])
        for _ in range(5):
            self.add_row()
        self.layout.addWidget(QLabel("Items"))
        self.layout.addWidget(self.items_table)

        button_row = QHBoxLayout()
        self.add_row_button = QPushButton("Add Row")
        self.remove_row_button = QPushButton("Remove Row")
        self.save_button = QPushButton("Save Invoice")
        self.add_row_button.clicked.connect(self.add_row)
        self.remove_row_button.clicked.connect(self.remove_row)
        self.save_button.clicked.connect(self.save_invoice)
        button_row.addWidget(self.add_row_button)
        button_row.addWidget(self.remove_row_button)
        button_row.addStretch(1)
        button_row.addWidget(self.save_button)
        self.layout.addLayout(button_row)

        self.populate_customers([customer.name for customer in self.customer_service.get_all_customers()])

    def save_invoice(self):
        try:
            customer_name = self.customer_combo.currentText()
            customer = next((item for item in self.customer_service.get_all_customers() if item.name == customer_name), None)
            if customer is None:
                QMessageBox.warning(self, "Input Error", "Choose a customer.")
                return
            items = []
            for row in range(self.items_table.rowCount()):
                description_item = self.items_table.item(row, 0)
                if description_item is None or not description_item.text().strip():
                    continue
                size_item = self.items_table.item(row, 1)
                qty_item = self.items_table.item(row, 2)
                rate_item = self.items_table.item(row, 3)
                gst_item = self.items_table.item(row, 4)
                items.append({
                    "description": description_item.text().strip(),
                    "size": size_item.text().strip() if size_item else "",
                    "quantity": float(qty_item.text() if qty_item and qty_item.text().strip() else 0),
                    "rate": float(rate_item.text() if rate_item and rate_item.text().strip() else 0),
                    "gst_percentage": float(gst_item.text() if gst_item and gst_item.text().strip() else 18),
                })
            invoice_number = int(self.invoice_number_input.text().strip() or 0) or None
            invoice = self.invoice_service.create_invoice(customer.customer_id, items, invoice_number=invoice_number, date_value=self.date_edit.date().toPyDate())
            if self.discount_input.text().strip():
                invoice.discount_amount = float(self.discount_input.text().strip())
                invoice.refresh_totals()
                self.invoice_service.update_invoice(invoice.id, {"discount_amount": invoice.discount_amount})
            self.accept()
        except Exception as exc:
            QMessageBox.critical(self, "Save Failed", str(exc))

    def populate_customers(self, customers):
        self.customer_combo.clear()
        self.customer_combo.addItems(customers)

    def add_row(self):
        row = self.items_table.rowCount()
        self.items_table.insertRow(row)
        for column in range(self.items_table.columnCount()):
            self.items_table.setItem(row, column, QTableWidgetItem(""))

    def remove_row(self):
        row = self.items_table.currentRow()
        if row >= 0:
            self.items_table.removeRow(row)