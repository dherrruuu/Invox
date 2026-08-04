from __future__ import annotations

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QMessageBox, QPushButton

from ..models.product import Product
from ..services.product_service import ProductService
from .dialogs.product_dialog import ProductDialog
from .ui_helpers import centered_item, make_table, plain_item

class ProductsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Management")
        self.service = ProductService()
        self.layout = QtWidgets.QVBoxLayout(self)

        toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search products")
        self.search_input.textChanged.connect(self.load_products)
        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)
        self.edit_button = QPushButton("Edit Product")
        self.edit_button.clicked.connect(self.edit_product)
        self.delete_button = QPushButton("Delete Product")
        self.delete_button.clicked.connect(self.delete_product)
        toolbar.addWidget(self.search_input, 1)
        toolbar.addWidget(self.add_button)
        toolbar.addWidget(self.edit_button)
        toolbar.addWidget(self.delete_button)
        self.layout.addLayout(toolbar)

        self.table = QtWidgets.QTableWidget()
        make_table(self.table, ["Product ID", "Name", "Category", "Unit", "Rate", "GST %"])
        self.layout.addWidget(self.table)

        self.load_products()

    def load_products(self, *_args):
        query = self.search_input.text().strip()
        products = self.service.search_products(query) if query else self.service.list_products()
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, centered_item(str(product.product_id)))
            self.table.setItem(row, 1, plain_item(product.name))
            self.table.setItem(row, 2, plain_item(product.category))
            self.table.setItem(row, 3, centered_item(product.unit))
            self.table.setItem(row, 4, centered_item(f"{product.rate:.2f}"))
            self.table.setItem(row, 5, centered_item(f"{product.gst_percentage:.2f}"))

    def add_product(self, *_args):
        dialog = ProductDialog(parent=self)
        if dialog.exec():
            self.load_products()

    def edit_product(self, *_args):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a product to edit.")
            return
        product_id = int(self.table.item(selected_row, 0).text())
        product = self.service.get_product(product_id)
        dialog = ProductDialog(product=product, parent=self)
        if dialog.exec():
            self.load_products()

    def delete_product(self, *_args):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            product_id = self.table.item(selected_row, 0).text()
            if QMessageBox.question(self, "Delete", "Delete selected product?") == QMessageBox.StandardButton.Yes:
                self.service.delete_product(int(product_id))
                self.load_products()
        else:
            QMessageBox.warning(self, "Warning", "Please select a product to delete.")