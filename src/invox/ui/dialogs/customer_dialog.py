from __future__ import annotations

from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout

from ...models.customer import Customer
from ...services.customer_service import CustomerService

class CustomerDialog(QDialog):
    def __init__(self, customer: Customer | None = None, parent=None):
        super().__init__(parent)
        self.customer = customer
        self.customer_service = CustomerService()
        self.setWindowTitle("Customer Information")
        self.setMinimumWidth(520)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.company_input = QLineEdit()
        self.address_input = QTextEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.gst_input = QLineEdit()

        form.addRow("Customer Name", self.name_input)
        form.addRow("Company Name", self.company_input)
        form.addRow("Address", self.address_input)
        form.addRow("Phone Number", self.phone_input)
        form.addRow("Email", self.email_input)
        form.addRow("GST Number", self.gst_input)

        layout.addLayout(form)

        self.save_button = QPushButton("Save Customer")
        self.save_button.clicked.connect(self.save_customer)
        layout.addWidget(self.save_button)

        if self.customer is not None:
            self.name_input.setText(self.customer.name)
            self.company_input.setText(self.customer.company_name)
            self.address_input.setPlainText(self.customer.address)
            self.phone_input.setText(self.customer.phone)
            self.email_input.setText(self.customer.email)
            self.gst_input.setText(self.customer.gst_number)

    def save_customer(self):
        payload = {
            "name": self.name_input.text().strip(),
            "company_name": self.company_input.text().strip(),
            "address": self.address_input.toPlainText().strip(),
            "phone": self.phone_input.text().strip(),
            "email": self.email_input.text().strip(),
            "gst_number": self.gst_input.text().strip(),
        }
        if not payload["name"]:
            QMessageBox.warning(self, "Input Error", "Customer name is required.")
            return
        try:
            if self.customer is None:
                self.customer_service.add_customer(payload)
            else:
                payload["customer_id"] = self.customer.customer_id
                self.customer_service.edit_customer(self.customer.customer_id, payload)
            self.accept()
        except Exception as exc:
            QMessageBox.critical(self, "Save Failed", str(exc))