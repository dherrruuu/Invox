from __future__ import annotations

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QMessageBox, QPushButton, QTableWidgetItem, QVBoxLayout

from ..services.customer_service import CustomerService
from .dialogs.customer_dialog import CustomerDialog
from .ui_helpers import centered_item, make_table, plain_item

class CustomersWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Management")
        self.service = CustomerService()
        self.layout = QVBoxLayout(self)

        toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search customers")
        self.search_input.textChanged.connect(self.load_customers)
        self.add_button = QPushButton("Add Customer")
        self.add_button.clicked.connect(self.add_customer)
        self.edit_button = QPushButton("Edit Customer")
        self.edit_button.clicked.connect(self.edit_customer)
        self.delete_button = QPushButton("Delete Customer")
        self.delete_button.clicked.connect(self.delete_customer)
        toolbar.addWidget(self.search_input, 1)
        toolbar.addWidget(self.add_button)
        toolbar.addWidget(self.edit_button)
        toolbar.addWidget(self.delete_button)
        self.layout.addLayout(toolbar)

        self.table = QtWidgets.QTableWidget()
        make_table(self.table, ["Customer ID", "Name", "Company", "Phone", "Email", "GST"])
        self.layout.addWidget(self.table)

        self.load_customers()

    def load_customers(self, *_args):
        query = self.search_input.text().strip()
        customers = self.service.search_customers(query) if query else self.service.get_all_customers()
        self.table.setRowCount(len(customers))
        for row, customer in enumerate(customers):
            self.table.setItem(row, 0, centered_item(str(customer.customer_id)))
            self.table.setItem(row, 1, plain_item(customer.name))
            self.table.setItem(row, 2, plain_item(customer.company_name))
            self.table.setItem(row, 3, centered_item(customer.phone))
            self.table.setItem(row, 4, plain_item(customer.email))
            self.table.setItem(row, 5, centered_item(customer.gst_number))

    def add_customer(self, *_args):
        dialog = CustomerDialog(parent=self)
        if dialog.exec():
            self.load_customers()

    def edit_customer(self, *_args):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a customer to edit.")
            return
        customer_id = int(self.table.item(selected_row, 0).text())
        customer = self.service.get_customer_by_id(customer_id)
        dialog = CustomerDialog(customer=customer, parent=self)
        if dialog.exec():
            self.load_customers()

    def delete_customer(self, *_args):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a customer to delete.")
            return
        customer_id = int(self.table.item(selected_row, 0).text())
        if QMessageBox.question(self, "Delete", "Delete selected customer?") == QMessageBox.StandardButton.Yes:
            self.service.delete_customer(customer_id)
            self.load_customers()