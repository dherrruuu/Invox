from __future__ import annotations

from datetime import date, datetime

from sqlalchemy.orm import Session

from ..constants import DEFAULT_TAX_RATE
from ..db.connection import get_session
from ..models.customer import Customer
from ..models.invoice import Invoice
from ..models.invoice_item import InvoiceItem
from ..repositories.invoice_repository import InvoiceRepository


class InvoiceService:
    def __init__(self, db_session: Session | None = None):
        self.db_session = db_session or get_session()
        self.invoice_repository = InvoiceRepository(self.db_session)

    def _next_invoice_number(self) -> int:
        latest = self.db_session.query(Invoice).order_by(Invoice.invoice_number.desc()).first()
        return 1 if latest is None else int(latest.invoice_number) + 1

    def create_invoice(self, customer_or_invoice, items=None, total_amount=None, invoice_number=None, date_value=None):
        if isinstance(customer_or_invoice, Invoice):
            invoice = customer_or_invoice
        else:
            customer_id = customer_or_invoice.customer_id if isinstance(customer_or_invoice, Customer) else int(customer_or_invoice)
            invoice = Invoice(
                invoice_number=invoice_number or self._next_invoice_number(),
                customer_id=customer_id,
                date=date_value or date.today(),
                total_amount=total_amount or 0,
            )
            for item in items or []:
                invoice.add_item(item)
        invoice.refresh_totals()
        return self.invoice_repository.add_invoice(invoice)

    def calculate_total(self, invoice_or_items):
        if isinstance(invoice_or_items, Invoice):
            invoice_or_items.refresh_totals()
            return invoice_or_items.subtotal
        subtotal = 0.0
        for item in invoice_or_items:
            quantity = float(item.get("quantity", 0))
            rate = float(item.get("rate", 0))
            amount = quantity * rate
            subtotal += amount
        return subtotal

    def generate_invoice_pdf(self, invoice):
        from .pdf_service import PDFService

        pdf_service = PDFService()
        invoice_data = invoice.generate_invoice() if isinstance(invoice, Invoice) else invoice
        return pdf_service.generate_invoice_pdf(invoice_data)

    def get_invoice(self, invoice_id):
        return self.invoice_repository.get_invoice(invoice_id)

    def update_invoice(self, invoice_id, updated_data):
        invoice = self.invoice_repository.get_invoice(invoice_id)
        if invoice is None:
            return None
        for key, value in updated_data.items():
            setattr(invoice, key, value)
        invoice.refresh_totals()
        return self.invoice_repository.update_invoice(invoice)

    def delete_invoice(self, invoice_id):
        return self.invoice_repository.delete_invoice(invoice_id)

    def list_invoices(self):
        return self.invoice_repository.get_all_invoices()