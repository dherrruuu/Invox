from __future__ import annotations

from datetime import date, datetime
from typing import Iterable

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..constants import DEFAULT_DISCOUNT_RATE, DEFAULT_TAX_RATE
from ..db.connection import Base
from ..utils.formatting import format_quotation_number


class Quotation(Base):
    __tablename__ = "quotations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quotation_number: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    quotation_code: Mapped[str] = mapped_column(String(40), unique=True, index=True, default="")
    quotation_date: Mapped[date] = mapped_column(Date, default=date.today)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id", ondelete="RESTRICT"), index=True)
    subtotal: Mapped[float] = mapped_column(Float, default=0.0)
    gst_amount: Mapped[float] = mapped_column(Float, default=0.0)
    discount_amount: Mapped[float] = mapped_column(Float, default=DEFAULT_DISCOUNT_RATE)
    grand_total: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(30), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="quotations")
    line_items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete-orphan", order_by="QuotationItem.id")

    def __init__(self, **kwargs):
        customer = kwargs.pop("customer", None)
        date_value = kwargs.pop("date", None)
        if date_value is not None and "quotation_date" not in kwargs:
            kwargs["quotation_date"] = self._coerce_date(date_value)
        if "total_amount" in kwargs and "grand_total" not in kwargs:
            kwargs["grand_total"] = kwargs.pop("total_amount")
        if "quotation_code" not in kwargs and "quotation_number" in kwargs:
            kwargs["quotation_code"] = format_quotation_number(kwargs["quotation_number"])
        if "discount" in kwargs and "discount_amount" not in kwargs:
            kwargs["discount_amount"] = kwargs.pop("discount")
        super().__init__(**kwargs)
        if customer is not None:
            self.customer = customer

    @staticmethod
    def _coerce_date(value) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        return datetime.fromisoformat(str(value)).date()

    @property
    def date(self):
        return self.quotation_date

    @date.setter
    def date(self, value):
        self.quotation_date = self._coerce_date(value)

    @property
    def items(self):
        return [
            {
                "description": item.description,
                "unit": item.unit,
                "quantity": item.quantity,
                "rate": item.rate,
                "amount": item.amount,
                "gst_percentage": item.gst_percentage,
            }
            for item in self.line_items
        ]

    def add_item(self, description, quantity=None, rate=None, unit="", gst_percentage=DEFAULT_TAX_RATE):
        from .quotation_item import QuotationItem

        if isinstance(description, dict):
            payload = description
            description = payload.get("description", "")
            quantity = payload.get("quantity", quantity)
            rate = payload.get("rate", rate)
            unit = payload.get("unit", unit)
            gst_percentage = payload.get("gst_percentage", gst_percentage)

        quantity = float(quantity or 0)
        rate = float(rate or 0)
        amount = quantity * rate
        item = QuotationItem(
            description=str(description),
            unit=str(unit),
            quantity=quantity,
            rate=rate,
            amount=amount,
            gst_percentage=float(gst_percentage or 0),
        )
        self.line_items.append(item)
        self.refresh_totals()
        return item

    def set_items(self, items: Iterable[dict]) -> None:
        self.line_items.clear()
        for item in items:
            self.add_item(item)

    def refresh_totals(self) -> None:
        subtotal = sum(float(item.amount or 0) for item in self.line_items)
        gst_amount = sum(float(item.amount or 0) * float(item.gst_percentage or 0) / 100.0 for item in self.line_items)
        self.subtotal = subtotal
        self.gst_amount = gst_amount
        self.grand_total = subtotal + gst_amount - float(self.discount_amount or 0)

    def generate_quotation(self):
        self.refresh_totals()
        return {
            "quotation_number": self.quotation_number,
            "quotation_code": self.quotation_code,
            "date": self.quotation_date,
            "customer_id": self.customer_id,
            "items": self.items,
            "subtotal": self.subtotal,
            "gst_amount": self.gst_amount,
            "discount_amount": self.discount_amount,
            "grand_total": self.grand_total,
        }
