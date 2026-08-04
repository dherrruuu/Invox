from __future__ import annotations

from datetime import date, datetime

from sqlalchemy.orm import Session

from ..db.connection import get_session
from ..models.customer import Customer
from ..models.invoice import Invoice
from ..models.quotation import Quotation
from ..repositories.customer_repository import CustomerRepository
from ..repositories.invoice_repository import InvoiceRepository
from ..repositories.quotation_repository import QuotationRepository


class ReportService:
    def __init__(self, db_session: Session | None = None):
        self.db_session = db_session or get_session()
        self.invoice_repo = InvoiceRepository(self.db_session)
        self.quotation_repo = QuotationRepository(self.db_session)
        self.customer_repo = CustomerRepository(self.db_session)

    def _between(self, model, start_date: date | datetime, end_date: date | datetime, column_name: str):
        column = getattr(model, column_name)
        return list(
            self.db_session.query(model)
            .filter(column >= start_date, column <= end_date)
            .order_by(column.asc())
            .all()
        )

    def generate_sales_report(self, start_date: datetime, end_date: datetime):
        invoices = self._between(Invoice, start_date, end_date, "invoice_date")
        total_sales = sum(float(invoice.grand_total or 0) for invoice in invoices)
        return {"total_sales": total_sales, "invoices": invoices}

    def generate_customer_report(self):
        customers = self.customer_repo.get_all_customers()
        return {"total_customers": len(customers), "customers": customers}

    def generate_quotation_report(self, start_date: datetime, end_date: datetime):
        quotations = self._between(Quotation, start_date, end_date, "quotation_date")
        total_quotations = len(quotations)
        total_value = sum(float(quotation.grand_total or 0) for quotation in quotations)
        return {"total_quotations": total_quotations, "total_value": total_value, "quotations": quotations}