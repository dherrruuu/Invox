from __future__ import annotations

import re
from collections.abc import Iterable, Mapping


EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def _get_value(data, key: str, default=""):
    if isinstance(data, Mapping):
        return data.get(key, default)
    return getattr(data, key, default)


def validate_email(email: str | None) -> bool:
    if not email:
        return True
    return re.match(EMAIL_REGEX, str(email)) is not None


def validate_required_fields(fields: Iterable[object]) -> bool:
    return all(str(field).strip() != "" for field in fields)


def validate_positive_number(value) -> bool:
    return isinstance(value, (int, float)) and value >= 0


def validate_customer_data(customer_data) -> bool:
    return validate_required_fields([_get_value(customer_data, "name")]) and validate_email(_get_value(customer_data, "email"))


def validate_product_data(product_data) -> bool:
    name = _get_value(product_data, "name")
    rate = _get_value(product_data, "rate", 0)
    return validate_required_fields([name]) and validate_positive_number(rate)


def validate_invoice_number(invoice_number) -> bool:
    return isinstance(invoice_number, (str, int))


def validate_quotation_number(quotation_number) -> bool:
    return isinstance(quotation_number, (str, int))