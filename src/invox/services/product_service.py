"""
Product Service
"""

from invox.repositories.product_repository import ProductRepository


class ProductService:

    def __init__(self):

        self.product_repository = ProductRepository()

    # --------------------------------
    # Create Product
    # --------------------------------

    def create_product(
        self,
        data: dict,
    ):

        return self.product_repository.create(
            data
        )

    # --------------------------------
    # Get Product
    # --------------------------------

    def get_product(
        self,
        product_id: int,
    ):

        return self.product_repository.get_by_id(
            product_id
        )

    # --------------------------------
    # Get All Products
    # --------------------------------

    def get_all_products(self):

        return self.product_repository.get_all()

    # --------------------------------
    # Search Products
    # --------------------------------

    def search_products(
        self,
        keyword: str,
    ):

        products = self.product_repository.get_all()

        keyword = keyword.lower()

        return [

            product

            for product in products

            if keyword in str(
                product.get("name", "")
            ).lower()

            or keyword in str(
                product.get("description", "")
            ).lower()

        ]

    # --------------------------------
    # Update Product
    # --------------------------------

    def update_product(
        self,
        product_id: int,
        data: dict,
    ):

        return self.product_repository.update(
            product_id,
            data,
        )

    # --------------------------------
    # Delete Product
    # --------------------------------

    def delete_product(
        self,
        product_id: int,
    ):

        return self.product_repository.delete(
            product_id
        )