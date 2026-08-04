from __future__ import annotations

from datetime import date, datetime

from ..constants import DEFAULT_CURRENCY, INVOICE_PREFIX, QUOTATION_PREFIX


def format_currency(amount, currency: str = DEFAULT_CURRENCY) -> str:
    return f"{currency} {float(amount):,.2f}"


def format_date(value) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return str(value)


def format_invoice_number(invoice_number, year: int | None = None) -> str:
    if isinstance(invoice_number, str) and invoice_number.startswith(INVOICE_PREFIX):
        return invoice_number
    if year is None:
        year = datetime.now().year
    return f"{INVOICE_PREFIX}-{year}-{int(invoice_number):04d}"


def format_quotation_number(quotation_number, year: int | None = None) -> str:
    if isinstance(quotation_number, str) and quotation_number.startswith(QUOTATION_PREFIX):
        return quotation_number
    if year is None:
        year = datetime.now().year
    return f"{QUOTATION_PREFIX}-{year}-{int(quotation_number):04d}"