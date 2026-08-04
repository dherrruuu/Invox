from __future__ import annotations

from sqlalchemy.orm import Session

from ..db.connection import get_session
from ..models.customer import Customer
from ..repositories.customer_repository import CustomerRepository
from ..utils.validators import validate_customer_data


class CustomerService:
    def __init__(self, db_session: Session | None = None):
        self.db_session = db_session or get_session()
        self.customer_repository = CustomerRepository(self.db_session)

    def add_customer(self, customer_data):
        customer = customer_data if isinstance(customer_data, Customer) else Customer(**customer_data)
        if not validate_customer_data(customer):
            raise ValueError("Invalid customer data")
        return self.customer_repository.add_customer(customer)

    def edit_customer(self, customer_or_id, updated_data=None):
        if isinstance(customer_or_id, Customer):
            customer = customer_or_id
        else:
            existing = self.customer_repository.get_customer(customer_or_id)
            if existing is None:
                raise ValueError("Customer not found")
            if updated_data is None:
                raise ValueError("Invalid customer data")
            customer = existing
            for key, value in updated_data.items():
                setattr(customer, key, value)
        if not validate_customer_data(customer):
            raise ValueError("Invalid customer data")
        return self.customer_repository.edit_customer(customer)

    def delete_customer(self, customer_id):
        if not self.customer_repository.delete_customer(customer_id):
            raise ValueError("Customer not found")
        return True

    def get_all_customers(self):
        return self.customer_repository.get_all_customers()

    def get_customer_by_id(self, customer_id):
        customer = self.customer_repository.get_customer(customer_id)
        if customer is None:
            raise ValueError("Customer not found")
        return customer

    def search_customers(self, query: str):
        return self.customer_repository.search(query)