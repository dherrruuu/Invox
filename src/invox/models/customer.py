from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.connection import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(200), default="")
    address: Mapped[str] = mapped_column(Text, default="")
    phone: Mapped[str] = mapped_column(String(32), default="")
    email: Mapped[str] = mapped_column(String(150), default="")
    gst_number: Mapped[str] = mapped_column(String(32), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    invoices = relationship("Invoice", back_populates="customer")
    quotations = relationship("Quotation", back_populates="customer")

    def __init__(self, **kwargs):
        if "customer_name" in kwargs and "name" not in kwargs:
            kwargs["name"] = kwargs.pop("customer_name")
        super().__init__(**kwargs)

    def update_info(self, name=None, address=None, email=None, phone=None, company_name=None, gst_number=None):
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if company_name is not None:
            self.company_name = company_name
        if gst_number is not None:
            self.gst_number = gst_number

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "company_name": self.company_name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "gst_number": self.gst_number,
        }

    def __repr__(self):
        return f"Customer({self.customer_id}, {self.name})"

    def __eq__(self, other):
        return isinstance(other, Customer) and self.customer_id == other.customer_id

    def __hash__(self):
        return hash(self.customer_id)