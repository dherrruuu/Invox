from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from ..models.quotation import Quotation
from .base_repository import BaseRepository


class QuotationRepository(BaseRepository[Quotation]):
    def __init__(self, db_session: Session):
        super().__init__(db_session)

    def add_quotation(self, quotation: Quotation) -> Quotation:
        return self.add(quotation)

    def get_quotation(self, quotation_id: int) -> Quotation | None:
        return (
            self.db_session.query(Quotation)
            .options(joinedload(Quotation.line_items), joinedload(Quotation.customer))
            .filter(Quotation.id == quotation_id)
            .first()
        )

    def get_by_number(self, quotation_number: int) -> Quotation | None:
        return (
            self.db_session.query(Quotation)
            .options(joinedload(Quotation.line_items), joinedload(Quotation.customer))
            .filter(Quotation.quotation_number == quotation_number)
            .first()
        )

    def update_quotation(self, quotation: Quotation) -> Quotation | None:
        existing = self.get_quotation(quotation.id)
        if existing is None:
            return None
        existing.quotation_date = quotation.quotation_date
        existing.customer_id = quotation.customer_id
        existing.subtotal = quotation.subtotal
        existing.gst_amount = quotation.gst_amount
        existing.discount_amount = quotation.discount_amount
        existing.grand_total = quotation.grand_total
        existing.notes = quotation.notes
        existing.status = quotation.status
        self.db_session.commit()
        self.db_session.refresh(existing)
        return existing

    def delete_quotation(self, quotation_id: int) -> bool:
        quotation = self.get_quotation(quotation_id)
        if quotation is None:
            return False
        self.db_session.delete(quotation)
        self.db_session.commit()
        return True

    def get_all_quotations(self):
        return list(
            self.db_session.query(Quotation)
            .options(joinedload(Quotation.line_items), joinedload(Quotation.customer))
            .order_by(Quotation.id.desc())
            .all()
        )