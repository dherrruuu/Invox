"""Quotation routes."""
from __future__ import annotations

import os
import re
from datetime import date
from pathlib import Path

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   send_file, session, url_for)

from src.invox.db.connection import get_session
from src.invox.models.quotation import Quotation as QModel
from src.invox.models.quotation_item import QuotationItem
from src.invox.services.customer_service import CustomerService
from src.invox.services.product_service import ProductService
from src.invox.services.quotation_service import QuotationService

from .auth import login_required

quotations_bp = Blueprint("quotations", __name__, url_prefix="/quotations")

STATUSES = ["draft", "partial", "final", "cancelled"]


def _parse_items(form):
    """Parse line items — non-contiguous index safe."""
    indices = sorted({
        int(m.group(1))
        for key in form
        for m in [re.match(r"^items\[(\d+)\]\[description\]$", key)]
        if m
    })
    items = []
    for i in indices:
        try:
            length = float(form.get(f"items[{i}][length]", 0) or 0)
            height = float(form.get(f"items[{i}][height]", 0) or 0)
            nos    = float(form.get(f"items[{i}][nos]",    0) or 0)
            qty    = length * height * nos if (length or height or nos) else float(form.get(f"items[{i}][quantity]", 0) or 0)
            rate   = float(form.get(f"items[{i}][rate]",   0) or 0)
        except ValueError:
            length = height = nos = qty = rate = 0.0
        amount = rate * qty
        items.append({
            "description": form.get(f"items[{i}][description]", "").strip(),
            "length": length,
            "height": height,
            "nos":    nos,
            "quantity": qty,
            "rate":   rate,
            "amount": amount,
            "gst_percentage": 0.0,
            "remarks": form.get(f"items[{i}][remarks]", "").strip(),
        })
    return items


def _save_quotation_items(db, quotation_id, items, notes, status, discount, gst_rate):
    q = db.query(QModel).filter_by(id=quotation_id).first()
    if not q:
        return
    for li in list(q.line_items):
        db.delete(li)
    db.flush()
    for it in items:
        li = QuotationItem(
            quotation_id=quotation_id,
            description=it["description"],
            length=it["length"],
            height=it["height"],
            nos=it["nos"],
            quantity=it["quantity"],
            rate=it["rate"],
            amount=it["amount"],
            gst_percentage=0.0,
            remarks=it["remarks"],
        )
        db.add(li)
    db.flush()
    subtotal    = sum(it["amount"] for it in items)
    gst_amount  = subtotal * float(gst_rate or 0) / 100.0
    grand_total = subtotal + gst_amount - float(discount or 0)
    q.notes          = notes
    q.status         = status
    q.discount_amount = float(discount or 0)
    q.subtotal        = subtotal
    q.gst_amount      = gst_amount
    q.grand_total     = grand_total
    db.commit()


@quotations_bp.route("/")
@login_required
def index():
    quotations = QuotationService().list_quotations()
    return render_template("quotations/list.html", quotations=quotations, user=session["user"])


@quotations_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    customers = CustomerService().get_all_customers()
    products  = ProductService().list_products()

    if request.method == "POST":
        try:
            customer_id     = int(request.form.get("customer_id", 0))
            quotation_date  = request.form.get("quotation_date") or str(date.today())
            notes           = request.form.get("notes", "").strip()
            status          = request.form.get("status", "draft")
            discount        = float(request.form.get("discount_amount", 0) or 0)
            gst_rate        = float(request.form.get("gst_rate", 18) or 18)
            items           = _parse_items(request.form)

            if not items:
                raise ValueError("At least one line item is required.")

            svc       = QuotationService()
            quotation = svc.create_quotation(customer_id, items=[], date_value=date.fromisoformat(quotation_date))

            db = get_session()
            try:
                _save_quotation_items(db, quotation.id, items, notes, status, discount, gst_rate)
            finally:
                db.close()

            flash("Quotation created successfully.", "success")
            return redirect(url_for("quotations.view", quotation_id=quotation.id))
        except Exception as e:
            flash(str(e), "error")

    return render_template("quotations/form.html",
                           customers=customers, products=products,
                           data={}, items=[], user=session["user"],
                           editing=False, statuses=STATUSES)


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
    customers = CustomerService().get_all_customers()
    products  = ProductService().list_products()

    db = get_session()
    try:
        q = db.query(QModel).filter_by(id=quotation_id).first()
        if not q:
            abort(404)

        if request.method == "POST":
            try:
                customer_id    = int(request.form.get("customer_id", q.customer_id))
                quotation_date = request.form.get("quotation_date") or str(q.quotation_date)
                notes          = request.form.get("notes", "").strip()
                status         = request.form.get("status", q.status)
                discount       = float(request.form.get("discount_amount", 0) or 0)
                gst_rate       = float(request.form.get("gst_rate", 18) or 18)
                items          = _parse_items(request.form)

                if not items:
                    raise ValueError("At least one line item is required.")

                q.customer_id    = customer_id
                q.quotation_date = date.fromisoformat(quotation_date)
                _save_quotation_items(db, quotation_id, items, notes, status, discount, gst_rate)

                flash("Quotation updated.", "success")
                return redirect(url_for("quotations.view", quotation_id=quotation_id))
            except Exception as e:
                flash(str(e), "error")

        data = {
            "customer_id":    q.customer_id,
            "quotation_date": str(q.quotation_date),
            "notes":          q.notes,
            "status":         q.status,
            "discount_amount": q.discount_amount,
            "gst_rate":       18.0,
        }
        items = [
            {
                "description": li.description,
                "length":      li.length,
                "height":      li.height,
                "nos":         li.nos,
                "quantity":    li.quantity,
                "rate":        li.rate,
                "amount":      li.amount,
                "remarks":     li.remarks,
            }
            for li in q.line_items
        ]
    finally:
        db.close()

    return render_template("quotations/form.html",
                           customers=customers, products=products,
                           data=data, items=items, user=session["user"],
                           editing=True, quotation_id=quotation_id,
                           quotation_code=q.quotation_code,
                           statuses=STATUSES)


@quotations_bp.route("/<int:quotation_id>/delete", methods=["POST"])
@login_required
def delete(quotation_id):
    QuotationService().delete_quotation(quotation_id)
    flash("Quotation deleted.", "success")
    return redirect(url_for("quotations.index"))


@quotations_bp.route("/<int:quotation_id>/pdf")
@login_required
def pdf(quotation_id):
    db = get_session()
    try:
        q = db.query(QModel).filter_by(id=quotation_id).first()
        if not q:
            abort(404)
        items_data = [
            {
                "description": li.description,
                "length":      li.length,
                "height":      li.height,
                "nos":         li.nos,
                "quantity":    li.quantity,
                "rate":        li.rate,
                "amount":      li.amount,
                "remarks":     li.remarks,
            }
            for li in q.line_items
        ]
        quotation_data = {
            "quotation_number": q.quotation_number,
            "quotation_code":   q.quotation_code,
            "date":             q.quotation_date,
            "subtotal":         q.subtotal,
            "gst_amount":       q.gst_amount,
            "discount_amount":  q.discount_amount,
            "grand_total":      q.grand_total,
            "items":            items_data,
        }
    finally:
        db.close()

    try:
        c = CustomerService().get_customer_by_id(q.customer_id)
        quotation_data.update(customer_name=c.name, customer_address=c.address,
                              customer_phone=c.phone, customer_gst=c.gst_number)
    except Exception:
        pass

    from src.invox.services.company_service import CompanyService
    co = CompanyService().get_profile()
    quotation_data.update(company_name=co.company_name, company_address=co.address,
                          company_phone=co.phone_number, company_gst=co.gst_number,
                          bank_details=co.bank_details,
                          terms_and_conditions=co.terms_and_conditions)

    from src.invox.services.pdf_service import PDFService
    path = PDFService().generate_quotation_pdf(quotation_data)
    abs_path = str(Path(path).resolve())
    return send_file(abs_path, as_attachment=True, download_name=os.path.basename(abs_path))
