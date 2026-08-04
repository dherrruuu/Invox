"""Customer CRUD routes."""
from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.invox.services.customer_service import CustomerService

from .auth import login_required

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    svc = CustomerService()
    customers = svc.search_customers(q) if q else svc.get_all_customers()
    return render_template("customers/list.html", customers=customers, q=q, user=session["user"])


@customers_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        data = {
            "name": request.form.get("name", "").strip(),
            "company_name": request.form.get("company_name", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "email": request.form.get("email", "").strip(),
            "address": request.form.get("address", "").strip(),
            "gst_number": request.form.get("gst_number", "").strip(),
        }
        try:
            CustomerService().add_customer(data)
            flash("Customer added successfully.", "success")
            return redirect(url_for("customers.index"))
        except ValueError as e:
            return render_template("customers/form.html", error=str(e), data=data, user=session["user"], editing=False)
    return render_template("customers/form.html", data={}, user=session["user"], editing=False)


@customers_bp.route("/<int:customer_id>/edit", methods=["GET", "POST"])
@login_required
def edit(customer_id):
    svc = CustomerService()
    try:
        customer = svc.get_customer_by_id(customer_id)
    except ValueError:
        flash("Customer not found.", "error")
        return redirect(url_for("customers.index"))

    if request.method == "POST":
        data = {
            "name": request.form.get("name", "").strip(),
            "company_name": request.form.get("company_name", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "email": request.form.get("email", "").strip(),
            "address": request.form.get("address", "").strip(),
            "gst_number": request.form.get("gst_number", "").strip(),
        }
        try:
            svc.edit_customer(customer_id, data)
            flash("Customer updated successfully.", "success")
            return redirect(url_for("customers.index"))
        except ValueError as e:
            return render_template("customers/form.html", error=str(e), data=data, user=session["user"], editing=True, customer_id=customer_id)

    return render_template("customers/form.html", data=customer.to_dict(), user=session["user"], editing=True, customer_id=customer_id)


@customers_bp.route("/<int:customer_id>/delete", methods=["POST"])
@login_required
def delete(customer_id):
    try:
        CustomerService().delete_customer(customer_id)
        flash("Customer deleted.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("customers.index"))
