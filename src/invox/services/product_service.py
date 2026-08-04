from __future__ import annotations

from sqlalchemy.orm import Session

from ..db.connection import get_session
from ..models.product import Product
from ..repositories.product_repository import ProductRepository
from ..utils.validators import validate_product_data


class ProductService:
    def __init__(self, db_session: Session | None = None):
        self.db_session = db_session or get_session()
        self.product_repository = ProductRepository(self.db_session)

    def add_product(self, product_or_name, category=None, rate=None, unit="Nos", gst_percentage=18.0):
        product = product_or_name if isinstance(product_or_name, Product) else Product(
            name=product_or_name,
            category=category or "",
            rate=rate or 0.0,
            unit=unit,
            gst_percentage=gst_percentage,
        )
        if not validate_product_data(product):
            raise ValueError("Invalid product details")
        return self.product_repository.add_product(product)

    def edit_product(self, product_or_id, name=None, category=None, rate=None, unit="Nos", gst_percentage=18.0):
        if isinstance(product_or_id, Product):
            product = product_or_id
        else:
            existing = self.product_repository.get_product(product_or_id)
            if existing is None:
                raise ValueError("Invalid product ID")
            product = existing
            if name is not None:
                product.name = name
            if category is not None:
                product.category = category
            if rate is not None:
                product.rate = rate
            product.unit = unit
            product.gst_percentage = gst_percentage
        if not validate_product_data(product):
            raise ValueError("Invalid product details")
        return self.product_repository.edit_product(product)

    def delete_product(self, product_id):
        if not self.product_repository.delete_product(product_id):
            raise ValueError("Invalid product ID")
        return True

    def get_product(self, product_id):
        product = self.product_repository.get_product(product_id)
        if product is None:
            raise ValueError("Invalid product ID")
        return product

    def list_products(self):
        return self.product_repository.get_all_products()

    def get_all_products(self):
        return self.list_products()

    def search_products(self, query: str):
        return self.product_repository.search(query)

    def get_product_by_id(self, product_id):
        return self.get_product(product_id)