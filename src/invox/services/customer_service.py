"""
Customer Service
"""

from invox.repositories.customer_repository import CustomerRepository


class CustomerService:

    def __init__(self):

        self.customer_repository = CustomerRepository()

    # --------------------------------
    # Create Customer
    # --------------------------------

    def create_customer(
        self,
        name: str,
        phone: str,
        address: str = "",
    ):

        return self.customer_repository.create_customer(
            name=name,
            phone=phone,
            address=address,
        )

    # --------------------------------
    # Get Customer
    # --------------------------------

    def get_customer(
        self,
        customer_id: int,
    ):

        return self.customer_repository.get_by_id(
            customer_id
        )

    # --------------------------------
    # Get All Customers
    # --------------------------------

    def get_all_customers(self):

        return self.customer_repository.get_all()

    # --------------------------------
    # Search
    # --------------------------------

    def search_customers(
        self,
        keyword: str,
    ):

        return self.customer_repository.search(
            keyword
        )

    # --------------------------------
    # Phone Search
    # --------------------------------

    def get_customer_by_phone(
        self,
        phone: str,
    ):

        return self.customer_repository.get_by_phone(
            phone
        )

    # --------------------------------
    # Update
    # --------------------------------

    def update_customer(
        self,
        customer_id: int,
        data: dict,
    ):

        return self.customer_repository.update_customer(
            customer_id,
            data,
        )

    # --------------------------------
    # Delete
    # --------------------------------

    def delete_customer(
        self,
        customer_id: int,
    ):

        return self.customer_repository.delete_customer(
            customer_id
        )