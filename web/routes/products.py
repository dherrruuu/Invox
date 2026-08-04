"""Product CRUD routes."""
from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.invox.services.product_service import ProductService

from .auth import login_required

products_bp = Blueprint("products", __name__, url_prefix="/products")


@products_bp.route("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    svc = ProductService()
    products = svc.search_products(q) if q else svc.list_products()
    return render_template("products/list.html", products=products, q=q, user=session["user"])


@products_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        unit = request.form.get("unit", "Nos").strip()
        try:
            rate = float(request.form.get("rate", 0))
            gst = float(request.form.get("gst_percentage", 18.0))
        except ValueError:
            rate, gst = 0.0, 18.0
        data = {"name": name, "category": category, "unit": unit, "rate": rate, "gst_percentage": gst}
        try:
            ProductService().add_product(name, category=category, rate=rate, unit=unit, gst_percentage=gst)
            flash("Product added successfully.", "success")
            return redirect(url_for("products.index"))
        except ValueError as e:
            return render_template("products/form.html", error=str(e), data=data, user=session["user"], editing=False)
    return render_template("products/form.html", data={}, user=session["user"], editing=False)


@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def edit(product_id):
    svc = ProductService()
    try:
        product = svc.get_product(product_id)
    except ValueError:
        flash("Product not found.", "error")
        return redirect(url_for("products.index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        unit = request.form.get("unit", "Nos").strip()
        try:
            rate = float(request.form.get("rate", 0))
            gst = float(request.form.get("gst_percentage", 18.0))
        except ValueError:
            rate, gst = 0.0, 18.0
        data = {"name": name, "category": category, "unit": unit, "rate": rate, "gst_percentage": gst}
        try:
            svc.edit_product(product_id, name=name, category=category, rate=rate, unit=unit, gst_percentage=gst)
            flash("Product updated successfully.", "success")
            return redirect(url_for("products.index"))
        except ValueError as e:
            return render_template("products/form.html", error=str(e), data=data, user=session["user"], editing=True, product_id=product_id)

    data = {
        "name": product.name,
        "category": product.category,
        "unit": product.unit,
        "rate": product.rate,
        "gst_percentage": product.gst_percentage,
    }
    return render_template("products/form.html", data=data, user=session["user"], editing=True, product_id=product_id)


@products_bp.route("/<int:product_id>/delete", methods=["POST"])
@login_required
def delete(product_id):
    try:
        ProductService().delete_product(product_id)
        flash("Product deleted.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("products.index"))
