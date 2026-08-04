from __future__ import annotations

from PyQt6.QtWidgets import QComboBox, QDialog, QFormLayout, QLineEdit, QMessageBox, QPushButton, QVBoxLayout

from ...models.product import Product
from ...services.product_service import ProductService

class ProductDialog(QDialog):
    def __init__(self, product: Product | None = None, parent=None):
        super(ProductDialog, self).__init__(parent)
        self.product = product
        self.product_service = ProductService()
        self.setWindowTitle("Product Management")
        self.setMinimumWidth(500)

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.product_name_input = QLineEdit(self)
        self.product_category_input = QLineEdit(self)
        self.product_unit_input = QLineEdit(self)
        self.product_rate_input = QLineEdit(self)
        self.product_gst_input = QLineEdit(self)

        self.form_layout.addRow("Product Name", self.product_name_input)
        self.form_layout.addRow("Category", self.product_category_input)
        self.form_layout.addRow("Unit", self.product_unit_input)
        self.form_layout.addRow("Rate", self.product_rate_input)
        self.form_layout.addRow("GST %", self.product_gst_input)

        self.layout.addLayout(self.form_layout)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_product)
        self.layout.addWidget(self.save_button)

        if self.product is not None:
            self.product_name_input.setText(self.product.name)
            self.product_category_input.setText(self.product.category)
            self.product_unit_input.setText(self.product.unit)
            self.product_rate_input.setText(str(self.product.rate))
            self.product_gst_input.setText(str(self.product.gst_percentage))

    def save_product(self):
        name = self.product_name_input.text().strip()
        category = self.product_category_input.text().strip()
        unit = self.product_unit_input.text().strip() or "Nos"
        try:
            rate = float(self.product_rate_input.text().strip() or 0)
            gst = float(self.product_gst_input.text().strip() or 18)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Rate and GST must be numeric.")
            return
        if not name:
            QMessageBox.warning(self, "Input Error", "Product name is required.")
            return
        try:
            if self.product is None:
                self.product_service.add_product(name, category, rate, unit=unit, gst_percentage=gst)
            else:
                self.product_service.edit_product(self.product.product_id, name=name, category=category, rate=rate, unit=unit, gst_percentage=gst)
            self.accept()
        except Exception as exc:
            QMessageBox.critical(self, "Save Failed", str(exc))