from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db.connection import Base


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(120), default="")
    unit: Mapped[str] = mapped_column(String(50), default="Nos")
    rate: Mapped[float] = mapped_column(Float, default=0.0)
    gst_percentage: Mapped[float] = mapped_column(Float, default=18.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        if "product_name" in kwargs and "name" not in kwargs:
            kwargs["name"] = kwargs.pop("product_name")
        super().__init__(**kwargs)

    def __str__(self):
        return f"Product({self.product_id}, {self.name}, {self.category}, {self.rate})"

    def __eq__(self, other):
        return isinstance(other, Product) and self.product_id == other.product_id

    def __hash__(self):
        return hash(self.product_id)