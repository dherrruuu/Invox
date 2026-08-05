"""Invoice routes."""
from __future__ import annotations

import os
import re
from datetime import date
from pathlib import Path

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   send_file, session, url_for)

from src.invox.db.connection import get_session
from src.invox.models.invoice import Invoice as InvoiceModel
from src.invox.models.invoice_item import InvoiceItem
from src.invox.services.customer_service import CustomerService
from src.invox.services.invoice_service import InvoiceService
from src.invox.services.product_service import ProductService

from .auth import login_required

invoices_bp = Blueprint("invoices", __name__, url_prefix="/invoices")

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
            "width":  nos,        # stored as width in DB
            "quantity": qty,
            "rate": rate,
            "amount": amount,
            "gst_percentage": 0.0,
            "remarks": form.get(f"items[{i}][remarks]", "").strip(),
        })
    return items


def _save_invoice_items(db, invoice_id, items, notes, status, discount, gst_rate):
    """Replace all line items and recompute totals."""
    inv = db.query(InvoiceModel).filter_by(id=invoice_id).first()
    if not inv:
        return
    for li in list(inv.line_items):
        db.delete(li)
    db.flush()
    for it in items:
        li = InvoiceItem(
            invoice_id=invoice_id,
            description=it["description"],
            length=it["length"],
            height=it["height"],
            width=it["width"],
            quantity=it["quantity"],
            rate=it["rate"],
            amount=it["amount"],
            gst_percentage=0.0,
            remarks=it["remarks"],
        )
        db.add(li)
    db.flush()
    subtotal = sum(it["amount"] for it in items)
    gst_amount = subtotal * float(gst_rate or 0) / 100.0
    grand_total = subtotal + gst_amount - float(discount or 0)
    inv.notes = notes
    inv.status = status
    inv.discount_amount = float(discount or 0)
    inv.subtotal = subtotal
    inv.gst_amount = gst_amount
    inv.grand_total = grand_total
    db.commit()


@invoices_bp.route("/")
@login_required
def index():
    from sqlalchemy.orm import joinedload
    from src.invox.models.payment import Payment
    db = get_session()
    try:
        invoices = (
            db.query(InvoiceModel)
            .options(joinedload(InvoiceModel.customer))
            .order_by(InvoiceModel.id.desc())
            .all()
        )
        paid_map = {}
        for inv in invoices:
            pmts = db.query(Payment).filter_by(invoice_id=inv.id).all()
            paid_map[inv.id] = sum(p.amount for p in pmts)
        # Detach safely: snapshot what the template needs
        rows = []
        for inv in invoices:
            rows.append({
                "obj":          inv,
                "customer_name": inv.customer.name if inv.customer else "—",
                "paid":          paid_map.get(inv.id, 0),
                "pending":       max(0, (inv.grand_total or 0) - paid_map.get(inv.id, 0)),
            })
    finally:
        db.close()
    return render_template("invoices/list.html", rows=rows, user=session["user"])


@invoices_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    customers = CustomerService().get_all_customers()
    products  = ProductService().list_products()

    if request.method == "POST":
        try:
            customer_id  = int(request.form.get("customer_id", 0))
            invoice_date = request.form.get("invoice_date") or str(date.today())
            notes        = request.form.get("notes", "").strip()
            status       = request.form.get("status", "draft")
            discount     = float(request.form.get("discount_amount", 0) or 0)
            gst_rate     = float(request.form.get("gst_rate", 18) or 18)
            items        = _parse_items(request.form)

            if not items:
                raise ValueError("At least one line item is required.")

            svc     = InvoiceService()
            invoice = svc.create_invoice(customer_id, items=[], date_value=date.fromisoformat(invoice_date))

            db = get_session()
            try:
                _save_invoice_items(db, invoice.id, items, notes, status, discount, gst_rate)
            finally:
                db.close()

            flash("Invoice created successfully.", "success")
            return redirect(url_for("invoices.view", invoice_id=invoice.id))
        except Exception as e:
            flash(str(e), "error")

    return render_template("invoices/form.html",
                           customers=customers, products=products,
                           data={}, items=[], user=session["user"],
                           editing=False, statuses=STATUSES)


@invoices_bp.route("/<int:invoice_id>")
@login_required
def view(invoice_id):
    from sqlalchemy.orm import joinedload
    from src.invox.models.payment import Payment
    db = get_session()
    try:
        invoice = (
            db.query(InvoiceModel)
            .options(joinedload(InvoiceModel.customer), joinedload(InvoiceModel.line_items))
            .filter_by(id=invoice_id)
            .first()
        )
        if not invoice:
            abort(404)
        pmts    = db.query(Payment).filter_by(invoice_id=invoice_id).order_by(Payment.payment_date).all()
        paid    = sum(p.amount for p in pmts)
        pending = max(0, (invoice.grand_total or 0) - paid)
        # snapshot customer name so template doesn't lazy-load after close
        cust_name    = invoice.customer.name if invoice.customer else "—"
        cust_company = (invoice.customer.company_name or "") if invoice.customer else ""
        items_snap = [
            {"description": li.description, "length": li.length, "height": li.height,
             "width": li.width, "quantity": li.quantity, "rate": li.rate,
             "amount": li.amount, "remarks": li.remarks}
            for li in invoice.line_items
        ]
    finally:
        db.close()
    return render_template("invoices/view.html", invoice=invoice,
                           cust_name=cust_name, cust_company=cust_company,
                           items_snap=items_snap,
                           payments=pmts, paid=paid, pending=pending,
                           user=session["user"])


@invoices_bp.route("/<int:invoice_id>/edit", methods=["GET", "POST"])
@login_required
def edit(invoice_id):
    customers = CustomerService().get_all_customers()
    products  = ProductService().list_products()

    db = get_session()
    try:
        invoice = db.query(InvoiceModel).filter_by(id=invoice_id).first()
        if not invoice:
            abort(404)

        if request.method == "POST":
            try:
                customer_id  = int(request.form.get("customer_id", invoice.customer_id))
                invoice_date = request.form.get("invoice_date") or str(invoice.invoice_date)
                notes        = request.form.get("notes", "").strip()
                status       = request.form.get("status", invoice.status)
                discount     = float(request.form.get("discount_amount", 0) or 0)
                gst_rate     = float(request.form.get("gst_rate", 18) or 18)
                items        = _parse_items(request.form)

                if not items:
                    raise ValueError("At least one line item is required.")

                invoice.customer_id  = customer_id
                invoice.invoice_date = date.fromisoformat(invoice_date)
                _save_invoice_items(db, invoice_id, items, notes, status, discount, gst_rate)

                flash("Invoice updated.", "success")
                return redirect(url_for("invoices.view", invoice_id=invoice_id))
            except Exception as e:
                flash(str(e), "error")

        data = {
            "customer_id":    invoice.customer_id,
            "invoice_date":   str(invoice.invoice_date),
            "notes":          invoice.notes,
            "status":         invoice.status,
            "discount_amount": invoice.discount_amount,
            "gst_rate":       18.0,
        }
        items = [
            {
                "description": li.description,
                "length":      li.length,
                "height":      li.height,
                "nos":         li.width,
                "quantity":    li.quantity,
                "rate":        li.rate,
                "amount":      li.amount,
                "remarks":     li.remarks,
            }
            for li in invoice.line_items
        ]
    finally:
        db.close()

    return render_template("invoices/form.html",
                           customers=customers, products=products,
                           data=data, items=items, user=session["user"],
                           editing=True, invoice_id=invoice_id,
                           invoice_code=invoice.invoice_code,
                           statuses=STATUSES)


@invoices_bp.route("/<int:invoice_id>/delete", methods=["POST"])
@login_required
def delete(invoice_id):
    InvoiceService().delete_invoice(invoice_id)
    flash("Invoice deleted.", "success")
    return redirect(url_for("invoices.index"))


@invoices_bp.route("/<int:invoice_id>/pdf")
@login_required
def pdf(invoice_id):
    db = get_session()
    try:
        invoice = db.query(InvoiceModel).filter_by(id=invoice_id).first()
        if not invoice:
            abort(404)

        # Build items list with all fields
        items_data = []
        for li in invoice.line_items:
            items_data.append({
                "description": li.description,
                "length":      li.length,
                "height":      li.height,
                "nos":         li.width,
                "quantity":    li.quantity,
                "rate":        li.rate,
                "amount":      li.amount,
                "remarks":     li.remarks,
            })

        invoice_data = {
            "invoice_number": invoice.invoice_number,
            "invoice_code":   invoice.invoice_code,
            "date":           invoice.invoice_date,
            "subtotal":       invoice.subtotal,
            "gst_amount":     invoice.gst_amount,
            "discount_amount":invoice.discount_amount,
            "grand_total":    invoice.grand_total,
            "items":          items_data,
        }
    finally:
        db.close()

    try:
        c = CustomerService().get_customer_by_id(invoice.customer_id)
        invoice_data.update(customer_name=c.name, customer_address=c.address,
                            customer_phone=c.phone, customer_gst=c.gst_number)
    except Exception:
        pass

    from src.invox.services.company_service import CompanyService
    co = CompanyService().get_profile()
    invoice_data.update(company_name=co.company_name, company_address=co.address,
                        company_phone=co.phone_number, company_gst=co.gst_number,
                        bank_details=co.bank_details,
                        terms_and_conditions=co.terms_and_conditions)

    from src.invox.services.pdf_service import PDFService
    path = PDFService().generate_invoice_pdf(invoice_data)
    abs_path = str(Path(path).resolve())
    return send_file(abs_path, as_attachment=True, download_name=os.path.basename(abs_path))
