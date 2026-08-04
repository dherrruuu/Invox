"""Quotation routes."""
from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   send_file, session, url_for)

from src.invox.services.customer_service import CustomerService
from src.invox.services.product_service import ProductService
from src.invox.services.quotation_service import QuotationService

from .auth import login_required

quotations_bp = Blueprint("quotations", __name__, url_prefix="/quotations")


def _parse_items(form):
    """Parse line items from form, collecting all present indices (non-contiguous safe)."""
    import re
    indices = sorted({
        int(m.group(1))
        for key in form
        for m in [re.match(r"^items\[(\d+)\]\[description\]$", key)]
        if m
    })
    items = []
    for i in indices:
        try:
            qty = float(form.get(f"items[{i}][quantity]", 0) or 0)
            rate = float(form.get(f"items[{i}][rate]", 0) or 0)
            gst = float(form.get(f"items[{i}][gst_percentage]", 18) or 18)
        except ValueError:
            qty, rate, gst = 0.0, 0.0, 18.0
        items.append({
            "description": form.get(f"items[{i}][description]", "").strip(),
            "unit": form.get(f"items[{i}][unit]", "").strip(),
            "quantity": qty,
            "rate": rate,
            "amount": qty * rate,
            "gst_percentage": gst,
        })
    return items


@quotations_bp.route("/")
@login_required
def index():
    quotations = QuotationService().list_quotations()
    return render_template("quotations/list.html", quotations=quotations, user=session["user"])


@quotations_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    customers = CustomerService().get_all_customers()
    products = ProductService().list_products()

    if request.method == "POST":
        try:
            customer_id = int(request.form.get("customer_id", 0))
            quotation_date = request.form.get("quotation_date") or str(date.today())
            notes = request.form.get("notes", "").strip()
            status = request.form.get("status", "draft")
            try:
                discount = float(request.form.get("discount_amount", 0) or 0)
            except ValueError:
                discount = 0.0
            items = _parse_items(request.form)
            if not items:
                raise ValueError("At least one line item is required.")

            svc = QuotationService()
            quotation = svc.create_quotation(
                customer_id,
                items=items,
                date_value=date.fromisoformat(quotation_date),
            )
            # Update notes, status, discount
            from src.invox.db.connection import get_session
            from src.invox.models.quotation import Quotation as QModel
            db = get_session()
            q = db.query(QModel).filter_by(id=quotation.id).first()
            if q:
                q.notes = notes
                q.status = status
                q.discount_amount = discount
                q.refresh_totals()
                db.commit()
            db.close()

            flash("Quotation created successfully.", "success")
            return redirect(url_for("quotations.view", quotation_id=quotation.id))
        except Exception as e:
            flash(str(e), "error")

    return render_template("quotations/form.html",
                           customers=customers, products=products,
                           data={}, items=[], user=session["user"], editing=False)


@quotations_bp.route("/<int:quotation_id>")
@login_required
def view(quotation_id):
    quotation = QuotationService().get_quotation(quotation_id)
    if not quotation:
        abort(404)
    return render_template("quotations/view.html", quotation=quotation, user=session["user"])


@quotations_bp.route("/<int:quotation_id>/edit", methods=["GET", "POST"])
@login_required
def edit(quotation_id):
    svc = QuotationService()
    quotation = svc.get_quotation(quotation_id)
    if not quotation:
        abort(404)
    customers = CustomerService().get_all_customers()
    products = ProductService().list_products()

    if request.method == "POST":
        try:
            customer_id = int(request.form.get("customer_id", quotation.customer_id))
            quotation_date = request.form.get("quotation_date") or str(quotation.quotation_date)
            notes = request.form.get("notes", "").strip()
            status = request.form.get("status", quotation.status)
            try:
                discount = float(request.form.get("discount_amount", 0) or 0)
            except ValueError:
                discount = 0.0
            items = _parse_items(request.form)
            if not items:
                raise ValueError("At least one line item is required.")

            from src.invox.db.connection import get_session
            from src.invox.models.quotation import Quotation as QModel
            from src.invox.models.quotation_item import QuotationItem
            db = get_session()
            db_q = db.query(QModel).filter_by(id=quotation_id).first()
            if db_q:
                db_q.customer_id = customer_id
                db_q.quotation_date = date.fromisoformat(quotation_date)
                db_q.notes = notes
                db_q.status = status
                db_q.discount_amount = discount
                for li in list(db_q.line_items):
                    db.delete(li)
                db.flush()
                for it in items:
                    li = QuotationItem(
                        quotation_id=quotation_id,
                        description=it["description"],
                        unit=it["unit"],
                        quantity=it["quantity"],
                        rate=it["rate"],
                        amount=it["amount"],
                        gst_percentage=it["gst_percentage"],
                    )
                    db.add(li)
                db.flush()
                db_q.refresh_totals()
                db.commit()
            db.close()

            flash("Quotation updated.", "success")
            return redirect(url_for("quotations.view", quotation_id=quotation_id))
        except Exception as e:
            flash(str(e), "error")

    data = {
        "customer_id": quotation.customer_id,
        "quotation_date": str(quotation.quotation_date),
        "notes": quotation.notes,
        "status": quotation.status,
        "discount_amount": quotation.discount_amount,
    }
    items = [
        {
            "description": li.description,
            "unit": li.unit,
            "quantity": li.quantity,
            "rate": li.rate,
            "amount": li.amount,
            "gst_percentage": li.gst_percentage,
        }
        for li in quotation.line_items
    ]
    return render_template("quotations/form.html",
                           customers=customers, products=products,
                           data=data, items=items, user=session["user"],
                           editing=True, quotation_id=quotation_id,
                           quotation_code=quotation.quotation_code)


@quotations_bp.route("/<int:quotation_id>/delete", methods=["POST"])
@login_required
def delete(quotation_id):
    QuotationService().delete_quotation(quotation_id)
    flash("Quotation deleted.", "success")
    return redirect(url_for("quotations.index"))


@quotations_bp.route("/<int:quotation_id>/pdf")
@login_required
def pdf(quotation_id):
    svc = QuotationService()
    quotation = svc.get_quotation(quotation_id)
    if not quotation:
        abort(404)
    quotation_data = quotation.generate_quotation()
    try:
        c = CustomerService().get_customer_by_id(quotation.customer_id)
        quotation_data["customer_name"] = c.name
        quotation_data["customer_address"] = c.address
        quotation_data["customer_phone"] = c.phone
        quotation_data["customer_gst"] = c.gst_number
    except Exception:
        pass
    from src.invox.services.company_service import CompanyService
    company = CompanyService().get_profile()
    quotation_data["company_name"] = company.company_name
    quotation_data["company_address"] = company.address
    quotation_data["company_phone"] = company.phone_number
    quotation_data["company_gst"] = company.gst_number
    quotation_data["bank_details"] = company.bank_details
    quotation_data["terms_and_conditions"] = company.terms_and_conditions

    path = svc.generate_quotation_pdf(quotation_data)
    abs_path = str(Path(path).resolve())
    return send_file(abs_path, as_attachment=True, download_name=os.path.basename(abs_path))
