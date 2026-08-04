from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.customer import Customer
from .base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, db_session: Session):
        super().__init__(db_session)

    def add_customer(self, customer: Customer) -> Customer:
        return self.add(customer)

    def edit_customer(self, customer: Customer) -> Customer | None:
        existing_customer = self.get_customer(customer.customer_id)
        if existing_customer is None:
            return None
        existing_customer.name = customer.name
        existing_customer.company_name = customer.company_name
        existing_customer.address = customer.address
        existing_customer.phone = customer.phone
        existing_customer.email = customer.email
        existing_customer.gst_number = customer.gst_number
        self.db_session.commit()
        self.db_session.refresh(existing_customer)
        return existing_customer

    def delete_customer(self, customer_id: int) -> bool:
        customer = self.get_customer(customer_id)
        if customer is None:
            return False
        self.db_session.delete(customer)
        self.db_session.commit()
        return True

    def get_customer(self, customer_id: int) -> Customer | None:
        return self.db_session.query(Customer).filter(Customer.customer_id == customer_id).first()

    def get_all_customers(self) -> list[Customer]:
        return list(self.db_session.query(Customer).order_by(Customer.name.asc()).all())

    def search(self, query: str) -> list[Customer]:
        term = f"%{query.lower()}%"
        return list(
            self.db_session.query(Customer)
            .filter(
                Customer.name.ilike(term)
                | Customer.company_name.ilike(term)
                | Customer.phone.ilike(term)
                | Customer.email.ilike(term)
            )
            .order_by(Customer.name.asc())
            .all()
        )