from __future__ import annotations

from datetime import date, datetime
from typing import Iterable

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..constants import DEFAULT_DISCOUNT_RATE, DEFAULT_TAX_RATE
from ..db.connection import Base
from ..utils.formatting import format_invoice_number


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_number: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    invoice_code: Mapped[str] = mapped_column(String(40), unique=True, index=True, default="")
    invoice_date: Mapped[date] = mapped_column(Date, default=date.today)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id", ondelete="RESTRICT"), index=True)
    subtotal: Mapped[float] = mapped_column(Float, default=0.0)
    gst_amount: Mapped[float] = mapped_column(Float, default=0.0)
    discount_amount: Mapped[float] = mapped_column(Float, default=DEFAULT_DISCOUNT_RATE)
    grand_total: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(30), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="invoices")
    line_items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan", order_by="InvoiceItem.id")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan", order_by="Payment.payment_date")

    def __init__(self, **kwargs):
        customer = kwargs.pop("customer", None)
        date_value = kwargs.pop("date", None)
        if date_value is not None and "invoice_date" not in kwargs:
            kwargs["invoice_date"] = self._coerce_date(date_value)
        if "total_amount" in kwargs and "grand_total" not in kwargs:
            kwargs["grand_total"] = kwargs.pop("total_amount")
        if "invoice_code" not in kwargs and "invoice_number" in kwargs:
            kwargs["invoice_code"] = format_invoice_number(kwargs["invoice_number"])
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
        return self.invoice_date

    @date.setter
    def date(self, value):
        self.invoice_date = self._coerce_date(value)

    @property
    def items(self):
        return [
            {
                "description": item.description,
                "size": item.size,
                "unit": item.unit,
                "quantity": item.quantity,
                "rate": item.rate,
                "amount": item.amount,
                "gst_percentage": item.gst_percentage,
            }
            for item in self.line_items
        ]

    def add_item(self, description, quantity=None, rate=None, size="", unit="", length=0, width=0, height=0, gst_percentage=DEFAULT_TAX_RATE):
        from .invoice_item import InvoiceItem

        if isinstance(description, dict):
            payload = description
            description = payload.get("description", "")
            quantity = payload.get("quantity", quantity)
            rate = payload.get("rate", rate)
            size = payload.get("size", size)
            unit = payload.get("unit", unit)
            length = payload.get("length", length)
            width = payload.get("width", width)
            height = payload.get("height", height)
            gst_percentage = payload.get("gst_percentage", gst_percentage)

        if quantity in (None, "") and all(value not in (None, "", 0) for value in (length, width, height)):
            quantity = float(length) * float(width) * float(height)

        quantity = float(quantity or 0)
        rate = float(rate or 0)
        amount = quantity * rate
        item = InvoiceItem(
            description=str(description),
            size=str(size),
            unit=str(unit),
            length=float(length or 0),
            width=float(width or 0),
            height=float(height or 0),
            quantity=quantity,
            rate=rate,
            amount=amount,
            gst_percentage=float(gst_percentage or 0),
        )
        self.line_items.append(item)
        self.refresh_totals()
        return item

    def remove_item(self, index: int) -> None:
        if 0 <= index < len(self.line_items):
            self.line_items.pop(index)
            self.refresh_totals()

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

    def generate_invoice(self):
        self.refresh_totals()
        return {
            "invoice_number": self.invoice_number,
            "invoice_code": self.invoice_code,
            "date": self.invoice_date,
            "customer_id": self.customer_id,
            "items": self.items,
            "subtotal": self.subtotal,
            "gst_amount": self.gst_amount,
            "discount_amount": self.discount_amount,
            "grand_total": self.grand_total,
        }

    def __str__(self):
        return f"Invoice {self.invoice_code or self.invoice_number} for Customer {self.customer_id} on {self.invoice_date}"