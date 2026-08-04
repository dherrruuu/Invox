from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db.connection import Base


class CompanyProfile(Base):
    __tablename__ = "company_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    company_name: Mapped[str] = mapped_column(String(200), default="INVOX Pvt Ltd")
    logo_path: Mapped[str] = mapped_column(String(500), default="")
    address: Mapped[str] = mapped_column(Text, default="")
    phone_number: Mapped[str] = mapped_column(String(32), default="")
    email: Mapped[str] = mapped_column(String(150), default="")
    gst_number: Mapped[str] = mapped_column(String(32), default="")
    bank_details: Mapped[str] = mapped_column(Text, default="")
    terms_and_conditions: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
