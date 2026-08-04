from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.product import Product
from .base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db_session: Session):
        super().__init__(db_session)

    def add_product(self, product: Product) -> Product:
        return self.add(product)

    def edit_product(self, product: Product) -> Product | None:
        existing_product = self.get_product(product.product_id)
        if existing_product is None:
            return None
        existing_product.name = product.name
        existing_product.category = product.category
        existing_product.unit = product.unit
        existing_product.rate = product.rate
        existing_product.gst_percentage = product.gst_percentage
        self.db_session.commit()
        self.db_session.refresh(existing_product)
        return existing_product

    def delete_product(self, product_id: int) -> bool:
        product = self.get_product(product_id)
        if product is None:
            return False
        self.db_session.delete(product)
        self.db_session.commit()
        return True

    def get_product(self, product_id: int) -> Product | None:
        return self.db_session.query(Product).filter(Product.product_id == product_id).first()

    def get_all_products(self) -> list[Product]:
        return list(self.db_session.query(Product).order_by(Product.name.asc()).all())

    def search(self, query: str) -> list[Product]:
        term = f"%{query.lower()}%"
        return list(
            self.db_session.query(Product)
            .filter(Product.name.ilike(term) | Product.category.ilike(term) | Product.unit.ilike(term))
            .order_by(Product.name.asc())
            .all()
        )