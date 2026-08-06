from typing import Dict, Any, List

from invox.repositories.base_repository import BaseRepository
from invox.db.manager import db


class QuotationRepository(BaseRepository):

    def __init__(self):
        super().__init__("quotations")

    # --------------------------------
    # Create quotation
    # --------------------------------

    def create_quotation(
        self,
        quotation_data: Dict[str, Any],
        items: List[Dict[str, Any]],
    ):

        quotation_response = self.create(
            quotation_data
        )

        if not quotation_response:
            return None

        quotation_id = quotation_response[0]["id"]

        for item in items:

            item["quotation_id"] = quotation_id

            db.insert(
                "quotation_items",
                item,
            )

        return self.get_quotation_details(
            quotation_id
        )

    # --------------------------------
    # Get quotation
    # --------------------------------

    def get_quotation_details(
        self,
        quotation_id: int,
    ):

        quotation = self.get_by_id(
            quotation_id
        )

        if not quotation:
            return None

        items = db.find(
            "quotation_items",
            "quotation_id",
            quotation_id,
        )

        quotation["items"] = items

        return quotation

    # --------------------------------
    # Customer quotations
    # --------------------------------

    def get_customer_quotations(
        self,
        customer_id: int,
    ):

        return db.find(
            "quotations",
            "customer_id",
            customer_id,
        )

    # --------------------------------
    # Delete quotation
    # --------------------------------

    def delete_quotation(
        self,
        quotation_id: int,
    ):

        return self.delete(
            quotation_id
        )