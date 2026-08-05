from typing import Dict, Any, List

from invox.repositories.customer_repository import CustomerRepository


class CustomerService:

    def __init__(self):
        self.customer_repository = CustomerRepository()


    # Get all customers
    def get_customers(self) -> List[Dict[str, Any]]:
        return self.customer_repository.get_all()


    # Get customer by ID
    def get_customer(self, customer_id: int):
        return self.customer_repository.get_by_id(customer_id)


    # Search customers
    def search_customer(self, keyword: str):

        if not keyword:
            return []

        return self.customer_repository.search(keyword)


    # Add new customer
    def add_customer(
        self,
        name: str,
        phone: str,
        address: str = None
    ):

        if not name:
            raise ValueError("Customer name is required")

        if not phone:
            raise ValueError("Customer phone is required")


        existing = self.customer_repository.get_by_phone(phone)

        if existing:
            raise ValueError(
                "Customer with this phone already exists"
            )


        return self.customer_repository.create_customer(
            name=name,
            phone=phone,
            address=address
        )


    # Update customer
    def update_customer(
        self,
        customer_id: int,
        data: Dict[str, Any]
    ):

        return self.customer_repository.update_customer(
            customer_id,
            data
        )


    # Delete customer
    def delete_customer(
        self,
        customer_id: int
    ):

        return self.customer_repository.delete_customer(
            customer_id
        )