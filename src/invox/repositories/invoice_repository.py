from typing import Dict, Any, List

from invox.repositories.base_repository import BaseRepository
from invox.repositories.customer_repository import CustomerRepository
from invox.db.manager import db


class InvoiceRepository(BaseRepository):

    def __init__(self):
        super().__init__("invoices")
        self.customer_repository = CustomerRepository()

    # -------------------------------------------------
    # Create complete invoice
    # -------------------------------------------------

    def create_invoice(
        self,
        invoice_data: Dict[str, Any],
        items: List[Dict[str, Any]]
    ):

        invoice_response = self.create(invoice_data)

        if not invoice_response:
            return None

        invoice_id = invoice_response[0]["id"]

        for item in items:
            item["invoice_id"] = invoice_id
            db.insert(
                "invoice_items",
                item
            )

        return self.get_invoice_details(invoice_id)

    # -------------------------------------------------
    # Get complete invoice
    # -------------------------------------------------

    def get_invoice_details(
        self,
        invoice_id: int
    ):

        invoice = self.get_by_id(invoice_id)

        if not invoice:
            return None

        # ---------------------------------------
        # Customer Details
        # ---------------------------------------

        customer = {}

        customer_id = invoice.get("customer_id")

        if customer_id:

            customer = (
                self.customer_repository.get_by_id(
                    customer_id
                )
                or {}
            )

        invoice["customer_name"] = customer.get(
            "name",
            ""
        )

        invoice["customer_phone"] = customer.get(
            "phone",
            ""
        )

        invoice["customer_address"] = customer.get(
            "address",
            ""
        )

        # ---------------------------------------
        # Invoice Items
        # ---------------------------------------

        items = db.find(
            "invoice_items",
            "invoice_id",
            invoice_id
        )

        invoice["items"] = items

        return invoice

    # -------------------------------------------------
    # Get invoices by customer
    # -------------------------------------------------

    def get_customer_invoices(
        self,
        customer_id: int
    ):

        return db.find(
            "invoices",
            "customer_id",
            customer_id
        )

    # -------------------------------------------------
    # Delete invoice
    # -------------------------------------------------

    def delete_invoice(
        self,
        invoice_id: int
    ):

        # invoice_items will be deleted automatically
        # because of CASCADE

        return self.delete(
            invoice_id
        )