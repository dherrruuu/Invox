from __future__ import annotations

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QComboBox, QDateEdit, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout

from ...services.customer_service import CustomerService
from ...services.quotation_service import QuotationService
from ..ui_helpers import make_table

class QuotationDialog(QDialog):
    def __init__(self, parent=None):
        super(QuotationDialog, self).__init__(parent)
        self.setWindowTitle("Create/Edit Quotation")
        self.setMinimumSize(940, 660)
        self.customer_service = CustomerService()
        self.quotation_service = QuotationService()

        self.layout = QVBoxLayout(self)
        form = QFormLayout()

        self.quotation_number_input = QLineEdit()
        self.customer_combo = QComboBox()
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        form.addRow("Quotation Number", self.quotation_number_input)
        form.addRow("Customer", self.customer_combo)
        form.addRow("Date", self.date_input)
        self.layout.addLayout(form)

        self.items_label = QLabel("Items")
        self.layout.addWidget(self.items_label)
        self.items_table = QTableWidget()
        make_table(self.items_table, ["Description", "Unit", "Qty", "Rate", "GST %"])
        for _ in range(5):
            self.add_row()
        self.layout.addWidget(self.items_table)

        button_row = QHBoxLayout()
        self.add_row_button = QPushButton("Add Row")
        self.remove_row_button = QPushButton("Remove Row")
        self.save_button = QPushButton("Save")
        self.add_row_button.clicked.connect(self.add_row)
        self.remove_row_button.clicked.connect(self.remove_row)
        self.save_button.clicked.connect(self.save_quotation)
        button_row.addWidget(self.add_row_button)
        button_row.addWidget(self.remove_row_button)
        button_row.addStretch(1)
        button_row.addWidget(self.save_button)
        self.layout.addLayout(button_row)

        self.populate_customers([customer.name for customer in self.customer_service.get_all_customers()])

    def save_quotation(self):
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
                unit_item = self.items_table.item(row, 1)
                qty_item = self.items_table.item(row, 2)
                rate_item = self.items_table.item(row, 3)
                gst_item = self.items_table.item(row, 4)
                items.append({
                    "description": description_item.text().strip(),
                    "unit": unit_item.text().strip() if unit_item else "",
                    "quantity": float(qty_item.text() if qty_item and qty_item.text().strip() else 0),
                    "rate": float(rate_item.text() if rate_item and rate_item.text().strip() else 0),
                    "gst_percentage": float(gst_item.text() if gst_item and gst_item.text().strip() else 18),
                })
            quotation_number = int(self.quotation_number_input.text().strip() or 0) or None
            self.quotation_service.create_quotation(customer.customer_id, items, quotation_number=quotation_number, date_value=self.date_input.date().toPyDate())
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