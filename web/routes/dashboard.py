"""Dashboard route."""
from __future__ import annotations

from flask import Blueprint, render_template, session

from src.invox.db.connection import get_session
from src.invox.models.customer import Customer
from src.invox.models.invoice import Invoice
from src.invox.models.product import Product
from src.invox.models.quotation import Quotation
from src.invox.services.company_service import CompanyService

from .auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    db = get_session()
    try:
        total_customers = db.query(Customer).count()
        total_products = db.query(Product).count()
        total_invoices = db.query(Invoice).count()
        total_quotations = db.query(Quotation).count()

        recent_invoices = (
            db.query(Invoice)
            .order_by(Invoice.id.desc())
            .limit(5)
            .all()
        )
        recent_quotations = (
            db.query(Quotation)
            .order_by(Quotation.id.desc())
            .limit(5)
            .all()
        )

        # Revenue from finalized invoices
        invoices_all = db.query(Invoice).all()
        total_revenue = sum(i.grand_total or 0 for i in invoices_all if i.status in ("finalized", "paid"))

        company = CompanyService(db).get_profile()
    finally:
        db.close()

    return render_template(
        "dashboard.html",
        total_customers=total_customers,
        total_products=total_products,
        total_invoices=total_invoices,
        total_quotations=total_quotations,
        total_revenue=total_revenue,
        recent_invoices=recent_invoices,
        recent_quotations=recent_quotations,
        company=company,
        user=session["user"],
    )
