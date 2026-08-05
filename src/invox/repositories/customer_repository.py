from typing import Dict, Any, List, Optional

from invox.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):

    def __init__(self):
        super().__init__("customers")


    # Get customer by phone number
    def get_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        results = self.find(
            "phone",
            phone
        )

        return results[0] if results else None


    # Search customers
    def search(self, keyword: str) -> List[Dict[str, Any]]:

        customers = self.get_all()

        keyword = keyword.lower()

        return [
            customer
            for customer in customers
            if keyword in str(customer.get("name", "")).lower()
            or keyword in str(customer.get("phone", ""))
        ]


    # Create customer
    def create_customer(
        self,
        name: str,
        phone: str,
        address: str = None
    ):

        data = {
            "name": name,
            "phone": phone,
            "address": address
        }

        return self.create(data)


    # Update customer
    def update_customer(
        self,
        customer_id: int,
        data: Dict[str, Any]
    ):

        return self.update(
            customer_id,
            data
        )


    # Delete customer
    def delete_customer(
        self,
        customer_id: int
    ):

        return self.delete(customer_id)