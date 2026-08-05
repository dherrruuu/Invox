from typing import Dict, Any, List, Optional

from invox.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository):

    def __init__(self):
        super().__init__("products")


    # Find product by product code
    def get_by_code(self, code: str) -> Optional[Dict[str, Any]]:

        results = self.find(
            "code",
            code
        )

        return results[0] if results else None


    # Search products
    def search(self, keyword: str) -> List[Dict[str, Any]]:

        products = self.get_all()

        keyword = keyword.lower()

        return [
            product
            for product in products
            if keyword in str(product.get("name", "")).lower()
            or keyword in str(product.get("code", "")).lower()
        ]


    # Create product
    def create_product(
        self,
        name: str,
        code: str,
        price: float,
        stock: int = 0
    ):

        data = {
            "name": name,
            "code": code,
            "price": price,
            "stock": stock
        }

        return self.create(data)


    # Update product
    def update_product(
        self,
        product_id: int,
        data: Dict[str, Any]
    ):

        return self.update(
            product_id,
            data
        )


    # Delete product
    def delete_product(
        self,
        product_id: int
    ):

        return self.delete(product_id)