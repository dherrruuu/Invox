from typing import Dict, Any, List

from invox.repositories.product_repository import ProductRepository


class ProductService:

    def __init__(self):
        self.product_repository = ProductRepository()


    # Get all products
    def get_products(self) -> List[Dict[str, Any]]:
        return self.product_repository.get_all()


    # Get product by ID
    def get_product(self, product_id: int):

        return self.product_repository.get_by_id(
            product_id
        )


    # Search products
    def search_product(self, keyword: str):

        if not keyword:
            return []

        return self.product_repository.search(
            keyword
        )


    # Add product
    def add_product(
        self,
        name: str,
        code: str,
        price: float,
        stock: int = 0
    ):

        if not name:
            raise ValueError(
                "Product name is required"
            )

        if not code:
            raise ValueError(
                "Product code is required"
            )

        if price < 0:
            raise ValueError(
                "Price cannot be negative"
            )


        existing = self.product_repository.get_by_code(
            code
        )


        if existing:
            raise ValueError(
                "Product with this code already exists"
            )


        return self.product_repository.create_product(
            name=name,
            code=code,
            price=price,
            stock=stock
        )


    # Update product
    def update_product(
        self,
        product_id: int,
        data: Dict[str, Any]
    ):

        return self.product_repository.update_product(
            product_id,
            data
        )


    # Delete product
    def delete_product(
        self,
        product_id: int
    ):

        return self.product_repository.delete_product(
            product_id
        )