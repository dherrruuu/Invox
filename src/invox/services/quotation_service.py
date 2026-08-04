from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from ..db.connection import get_session
from ..models.customer import Customer
from ..models.quotation import Quotation
from ..models.quotation_item import QuotationItem
from ..repositories.quotation_repository import QuotationRepository


class QuotationService:
    def __init__(self, db_session: Session | None = None):
        self.db_session = db_session or get_session()
        self.quotation_repository = QuotationRepository(self.db_session)

    def _next_quotation_number(self) -> int:
        latest = self.db_session.query(Quotation).order_by(Quotation.quotation_number.desc()).first()
        return 1 if latest is None else int(latest.quotation_number) + 1

    def create_quotation(self, customer_or_id, items=None, total_amount=None, quotation_number=None, date_value=None):
        if isinstance(customer_or_id, Quotation):
            quotation = customer_or_id
        else:
            customer_id = customer_or_id.customer_id if isinstance(customer_or_id, Customer) else int(customer_or_id)
            quotation = Quotation(
                quotation_number=quotation_number or self._next_quotation_number(),
                customer_id=customer_id,
                date=date_value or date.today(),
                total_amount=total_amount or 0,
            )
            for item in items or []:
                quotation.add_item(item)
        quotation.refresh_totals()
        return self.quotation_repository.add_quotation(quotation)

    def get_quotation(self, quotation_id):
        return self.quotation_repository.get_quotation(quotation_id)

    def update_quotation(self, quotation_id, updated_data):
        quotation = self.quotation_repository.get_quotation(quotation_id)
        if quotation is None:
            return None
        for key, value in updated_data.items():
            setattr(quotation, key, value)
        quotation.refresh_totals()
        return self.quotation_repository.update_quotation(quotation)

    def delete_quotation(self, quotation_id):
        return self.quotation_repository.delete_quotation(quotation_id)

    def list_quotations(self):
        return self.quotation_repository.get_all_quotations()

    def generate_quotation_pdf(self, quotation):
        from .pdf_service import PDFService

        pdf_service = PDFService()
        quotation_data = quotation.generate_quotation() if isinstance(quotation, Quotation) else quotation
        return pdf_service.generate_quotation_pdf(quotation_data)