"""Invoice routes."""
from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   send_file, session, url_for)

from src.invox.services.customer_service import CustomerService
from src.invox.services.invoice_service import InvoiceService
from src.invox.services.product_service import ProductService

from .auth import login_required

invoices_bp = Blueprint("invoices", __name__, url_prefix="/invoices")


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
            "size": form.get(f"items[{i}][size]", "").strip(),
            "quantity": qty,
            "rate": rate,
            "amount": qty * rate,
            "gst_percentage": gst,
        })
    return items


@invoices_bp.route("/")
@login_required
def index():
    invoices = InvoiceService().list_invoices()
    return render_template("invoices/list.html", invoices=invoices, user=session["user"])


@invoices_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    customers = CustomerService().get_all_customers()
    products = ProductService().list_products()

    if request.method == "POST":
        try:
            customer_id = int(request.form.get("customer_id", 0))
            invoice_date = request.form.get("invoice_date") or str(date.today())
            notes = request.form.get("notes", "").strip()
            status = request.form.get("status", "draft")
            try:
                discount = float(request.form.get("discount_amount", 0) or 0)
            except ValueError:
                discount = 0.0
            items = _parse_items(request.form)
            if not items:
                raise ValueError("At least one line item is required.")

            svc = InvoiceService()
            invoice = svc.create_invoice(
                customer_id,
                items=items,
                date_value=date.fromisoformat(invoice_date),
            )
            # Update notes, status, discount
            from src.invox.db.connection import get_session
            db = get_session()
            inv = db.query(__import__("src.invox.models.invoice", fromlist=["Invoice"]).Invoice).filter_by(id=invoice.id).first()
            if inv:
                inv.notes = notes
                inv.status = status
                inv.discount_amount = discount
                inv.refresh_totals()
                db.commit()
            db.close()

            flash("Invoice created successfully.", "success")
            return redirect(url_for("invoices.view", invoice_id=invoice.id))
        except Exception as e:
            flash(str(e), "error")

    return render_template("invoices/form.html",
                           customers=customers, products=products,
                           data={}, items=[], user=session["user"], editing=False)


@invoices_bp.route("/<int:invoice_id>")
@login_required
def view(invoice_id):
    invoice = InvoiceService().get_invoice(invoice_id)
    if not invoice:
        abort(404)
    return render_template("invoices/view.html", invoice=invoice, user=session["user"])


@invoices_bp.route("/<int:invoice_id>/edit", methods=["GET", "POST"])
@login_required
def edit(invoice_id):
    svc = InvoiceService()
    invoice = svc.get_invoice(invoice_id)
    if not invoice:
        abort(404)
    customers = CustomerService().get_all_customers()
    products = ProductService().list_products()

    if request.method == "POST":
        try:
            customer_id = int(request.form.get("customer_id", invoice.customer_id))
            invoice_date = request.form.get("invoice_date") or str(invoice.invoice_date)
            notes = request.form.get("notes", "").strip()
            status = request.form.get("status", invoice.status)
            try:
                discount = float(request.form.get("discount_amount", 0) or 0)
            except ValueError:
                discount = 0.0
            items = _parse_items(request.form)
            if not items:
                raise ValueError("At least one line item is required.")

            invoice.customer_id = customer_id
            invoice.invoice_date = date.fromisoformat(invoice_date)
            invoice.notes = notes
            invoice.status = status
            invoice.discount_amount = discount
            invoice.set_items(items)
            invoice.refresh_totals()

            from src.invox.db.connection import get_session
            db = get_session()
            from src.invox.models.invoice import Invoice as InvoiceModel
            from src.invox.models.invoice_item import InvoiceItem
            db_inv = db.query(InvoiceModel).filter_by(id=invoice_id).first()
            if db_inv:
                db_inv.customer_id = customer_id
                db_inv.invoice_date = date.fromisoformat(invoice_date)
                db_inv.notes = notes
                db_inv.status = status
                db_inv.discount_amount = discount
                # Replace line items
                for li in list(db_inv.line_items):
                    db.delete(li)
                db.flush()
                for it in items:
                    li = InvoiceItem(
                        invoice_id=invoice_id,
                        description=it["description"],
                        unit=it["unit"],
                        size=it.get("size", ""),
                        quantity=it["quantity"],
                        rate=it["rate"],
                        amount=it["amount"],
                        gst_percentage=it["gst_percentage"],
                    )
                    db.add(li)
                db.flush()
                db_inv.refresh_totals()
                db.commit()
            db.close()

            flash("Invoice updated.", "success")
            return redirect(url_for("invoices.view", invoice_id=invoice_id))
        except Exception as e:
            flash(str(e), "error")

    data = {
        "customer_id": invoice.customer_id,
        "invoice_date": str(invoice.invoice_date),
        "notes": invoice.notes,
        "status": invoice.status,
        "discount_amount": invoice.discount_amount,
    }
    items = [
        {
            "description": li.description,
            "unit": li.unit,
            "size": li.size,
            "quantity": li.quantity,
            "rate": li.rate,
            "amount": li.amount,
            "gst_percentage": li.gst_percentage,
        }
        for li in invoice.line_items
    ]
    return render_template("invoices/form.html",
                           customers=customers, products=products,
                           data=data, items=items, user=session["user"],
                           editing=True, invoice_id=invoice_id,
                           invoice_code=invoice.invoice_code)


@invoices_bp.route("/<int:invoice_id>/delete", methods=["POST"])
@login_required
def delete(invoice_id):
    InvoiceService().delete_invoice(invoice_id)
    flash("Invoice deleted.", "success")
    return redirect(url_for("invoices.index"))


@invoices_bp.route("/<int:invoice_id>/pdf")
@login_required
def pdf(invoice_id):
    svc = InvoiceService()
    invoice = svc.get_invoice(invoice_id)
    if not invoice:
        abort(404)
    invoice_data = invoice.generate_invoice()
    # Attach customer name
    from src.invox.services.customer_service import CustomerService as CS
    try:
        c = CS().get_customer_by_id(invoice.customer_id)
        invoice_data["customer_name"] = c.name
        invoice_data["customer_address"] = c.address
        invoice_data["customer_phone"] = c.phone
        invoice_data["customer_gst"] = c.gst_number
    except Exception:
        pass
    # Company profile
    from src.invox.services.company_service import CompanyService
    company = CompanyService().get_profile()
    invoice_data["company_name"] = company.company_name
    invoice_data["company_address"] = company.address
    invoice_data["company_phone"] = company.phone_number
    invoice_data["company_gst"] = company.gst_number
    invoice_data["bank_details"] = company.bank_details
    invoice_data["terms_and_conditions"] = company.terms_and_conditions

    path = svc.generate_invoice_pdf(invoice_data)
    abs_path = str(Path(path).resolve())
    return send_file(abs_path, as_attachment=True, download_name=os.path.basename(abs_path))
