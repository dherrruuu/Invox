from __future__ import annotations

from .connection import Base, get_engine


def create_all_tables(engine=None) -> None:
    from ..models.company_profile import CompanyProfile  # noqa: F401
    from ..models.customer import Customer  # noqa: F401
    from ..models.invoice import Invoice  # noqa: F401
    from ..models.invoice_item import InvoiceItem  # noqa: F401
    from ..models.product import Product  # noqa: F401
    from ..models.quotation import Quotation  # noqa: F401
    from ..models.quotation_item import QuotationItem  # noqa: F401
    from ..models.user import User  # noqa: F401

    Base.metadata.create_all(bind=engine or get_engine())