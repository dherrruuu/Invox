"""One-shot schema migration: adds new columns to existing tables."""
from __future__ import annotations

from sqlalchemy import text

from .connection import get_engine


_MIGRATIONS = [
    # invoice_items: add remarks column
    "ALTER TABLE invoice_items ADD COLUMN remarks TEXT DEFAULT ''",
    # quotation_items: add dimension + remarks columns
    "ALTER TABLE quotation_items ADD COLUMN size TEXT DEFAULT ''",
    "ALTER TABLE quotation_items ADD COLUMN length REAL DEFAULT 0.0",
    "ALTER TABLE quotation_items ADD COLUMN height REAL DEFAULT 0.0",
    "ALTER TABLE quotation_items ADD COLUMN nos REAL DEFAULT 0.0",
    "ALTER TABLE quotation_items ADD COLUMN remarks TEXT DEFAULT ''",
    # invoices: document-level gst_rate
    "ALTER TABLE invoices ADD COLUMN gst_rate REAL DEFAULT 18.0",
    # quotations: document-level gst_rate
    "ALTER TABLE quotations ADD COLUMN gst_rate REAL DEFAULT 18.0",
    # payments table is created by create_all; no alter needed
]


def run_migrations() -> None:
    """Apply each migration statement, ignoring duplicate-column errors."""
    engine = get_engine()
    with engine.connect() as conn:
        for stmt in _MIGRATIONS:
            try:
                conn.execute(text(stmt))
                conn.commit()
            except Exception:
                # Column already exists — safe to ignore
                conn.rollback()
