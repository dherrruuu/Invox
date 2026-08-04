from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from ..models.invoice import Invoice
from .base_repository import BaseRepository


class InvoiceRepository(BaseRepository[Invoice]):
    def __init__(self, db_session: Session):
        super().__init__(db_session)

    def add_invoice(self, invoice: Invoice) -> Invoice:
        return self.add(invoice)

    def get_invoice(self, invoice_id: int) -> Invoice | None:
        return (
            self.db_session.query(Invoice)
            .options(joinedload(Invoice.line_items), joinedload(Invoice.customer))
            .filter(Invoice.id == invoice_id)
            .first()
        )

    def get_by_number(self, invoice_number: int) -> Invoice | None:
        return (
            self.db_session.query(Invoice)
            .options(joinedload(Invoice.line_items), joinedload(Invoice.customer))
            .filter(Invoice.invoice_number == invoice_number)
            .first()
        )

    def update_invoice(self, invoice: Invoice) -> Invoice | None:
        existing_invoice = self.get_invoice(invoice.id)
        if existing_invoice is None:
            return None
        existing_invoice.invoice_date = invoice.invoice_date
        existing_invoice.customer_id = invoice.customer_id
        existing_invoice.subtotal = invoice.subtotal
        existing_invoice.gst_amount = invoice.gst_amount
        existing_invoice.discount_amount = invoice.discount_amount
        existing_invoice.grand_total = invoice.grand_total
        existing_invoice.notes = invoice.notes
        existing_invoice.status = invoice.status
        self.db_session.commit()
        self.db_session.refresh(existing_invoice)
        return existing_invoice

    def delete_invoice(self, invoice_id: int) -> bool:
        invoice = self.get_invoice(invoice_id)
        if invoice is None:
            return False
        self.db_session.delete(invoice)
        self.db_session.commit()
        return True

    def get_all_invoices(self) -> list[Invoice]:
        return list(
            self.db_session.query(Invoice)
            .options(joinedload(Invoice.line_items), joinedload(Invoice.customer))
            .order_by(Invoice.id.desc())
            .all()
        )