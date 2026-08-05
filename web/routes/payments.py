"""Payment recording routes for invoices."""
from __future__ import annotations

from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.invox.db.connection import get_session
from src.invox.models.invoice import Invoice
from src.invox.models.payment import Payment
from src.invox.services.invoice_service import InvoiceService

from .auth import login_required

payments_bp = Blueprint("payments", __name__, url_prefix="/invoices")


@payments_bp.route("/<int:invoice_id>/payments")
@login_required
def index(invoice_id):
    from sqlalchemy.orm import joinedload
    db = get_session()
    try:
        invoice = (
            db.query(Invoice)
            .options(joinedload(Invoice.customer))
            .filter_by(id=invoice_id)
            .first()
        )
        if not invoice:
            flash("Invoice not found.", "error")
            return redirect(url_for("invoices.index"))
        pmts = db.query(Payment).filter_by(invoice_id=invoice_id).order_by(Payment.payment_date).all()
        paid = sum(p.amount for p in pmts)
        pending = max(0, (invoice.grand_total or 0) - paid)
        cust_name = invoice.customer.name if invoice.customer else "—"
    finally:
        db.close()
    return render_template(
        "invoices/payments.html",
        invoice=invoice,
        cust_name=cust_name,
        payments=pmts,
        paid=paid,
        pending=pending,
        user=session["user"],
    )


@payments_bp.route("/<int:invoice_id>/payments/add", methods=["POST"])
@login_required
def add(invoice_id):
    db = get_session()
    try:
        invoice = db.query(Invoice).filter_by(id=invoice_id).first()
        if not invoice:
            flash("Invoice not found.", "error")
            return redirect(url_for("invoices.index"))
        try:
            amount = float(request.form.get("amount", 0) or 0)
        except ValueError:
            amount = 0.0
        if amount <= 0:
            flash("Payment amount must be greater than zero.", "error")
            return redirect(url_for("payments.index", invoice_id=invoice_id))
        pay_date = request.form.get("payment_date") or str(date.today())
        pmt = Payment(
            invoice_id=invoice_id,
            amount=amount,
            payment_date=date.fromisoformat(pay_date),
            method=request.form.get("method", "Cash").strip(),
            reference=request.form.get("reference", "").strip(),
            notes=request.form.get("notes", "").strip(),
        )
        db.add(pmt)
        # Update invoice status based on payment
        pmts = db.query(Payment).filter_by(invoice_id=invoice_id).all()
        paid = sum(p.amount for p in pmts) + amount
        if paid >= (invoice.grand_total or 0):
            invoice.status = "final"
        elif paid > 0:
            invoice.status = "partial"
        db.commit()
        flash(f"Payment of ₹{amount:,.2f} recorded.", "success")
    finally:
        db.close()
    return redirect(url_for("payments.index", invoice_id=invoice_id))


@payments_bp.route("/<int:invoice_id>/payments/<int:payment_id>/delete", methods=["POST"])
@login_required
def delete(invoice_id, payment_id):
    db = get_session()
    try:
        pmt = db.query(Payment).filter_by(id=payment_id, invoice_id=invoice_id).first()
        if pmt:
            db.delete(pmt)
            # Recompute status
            invoice = db.query(Invoice).filter_by(id=invoice_id).first()
            if invoice:
                remaining = db.query(Payment).filter_by(invoice_id=invoice_id).all()
                remaining = [p for p in remaining if p.id != payment_id]
                paid = sum(p.amount for p in remaining)
                if paid <= 0:
                    invoice.status = "draft"
                elif paid < (invoice.grand_total or 0):
                    invoice.status = "partial"
                else:
                    invoice.status = "final"
            db.commit()
            flash("Payment deleted.", "success")
    finally:
        db.close()
    return redirect(url_for("payments.index", invoice_id=invoice_id))
