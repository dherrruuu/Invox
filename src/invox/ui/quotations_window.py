from __future__ import annotations

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QMessageBox, QPushButton

from ..services.quotation_service import QuotationService
from .dialogs.quotation_dialog import QuotationDialog
from .ui_helpers import centered_item, make_table, plain_item

class QuotationsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quotations Management")
        self.service = QuotationService()
        self.layout = QtWidgets.QVBoxLayout(self)

        toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search quotations")
        self.search_input.textChanged.connect(self.load_quotations)
        self.btn_add = QPushButton("Add Quotation")
        self.btn_add.clicked.connect(self.add_quotation)
        self.btn_delete = QPushButton("Delete Quotation")
        self.btn_delete.clicked.connect(self.delete_quotation)
        toolbar.addWidget(self.search_input, 1)
        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_delete)
        self.layout.addLayout(toolbar)

        self.table = QtWidgets.QTableWidget()
        make_table(self.table, ["Quotation Number", "Date", "Customer", "Total", "Status"])
        self.layout.addWidget(self.table)

        self.load_quotations()

    def load_quotations(self, *_args):
        quotations = self.service.list_quotations()
        query = self.search_input.text().strip().lower()
        if query:
            quotations = [quotation for quotation in quotations if query in str(quotation.quotation_code).lower() or query in str(quotation.customer.name).lower()]
        self.table.setRowCount(len(quotations))
        for row, quotation in enumerate(quotations):
            self.table.setItem(row, 0, centered_item(str(quotation.quotation_code)))
            self.table.setItem(row, 1, centered_item(quotation.quotation_date.strftime("%Y-%m-%d")))
            self.table.setItem(row, 2, plain_item(quotation.customer.name if quotation.customer else ""))
            self.table.setItem(row, 3, centered_item(f"{quotation.grand_total:.2f}"))
            self.table.setItem(row, 4, centered_item(quotation.status))

    def add_quotation(self, *_args):
        dialog = QuotationDialog(parent=self)
        if dialog.exec():
            self.load_quotations()

    def view_quotation(self, *_args):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a quotation to view.")
            return
        QMessageBox.information(self, "Quotation", f"Quotation {self.table.item(selected_row, 0).text()} selected.")

    def delete_quotation(self, *_args):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a quotation to delete.")
            return
        quotation_code = self.table.item(selected_row, 0).text()
        quotation = next((item for item in self.service.list_quotations() if str(item.quotation_code) == quotation_code), None)
        if quotation and QMessageBox.question(self, "Delete", "Delete selected quotation?") == QMessageBox.StandardButton.Yes:
            self.service.delete_quotation(quotation.id)
            self.load_quotations()