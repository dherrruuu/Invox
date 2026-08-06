"""
Quotation Service
"""

from invox.repositories.quotation_repository import QuotationRepository
from invox.services.pdf_service import PDFService


class QuotationService:

    def __init__(self):

        self.quotation_repository = QuotationRepository()

        self.pdf_service = PDFService()

    # --------------------------------
    # Create Quotation
    # --------------------------------

    def create_quotation(
        self,
        quotation_data: dict,
        items: list,
    ):

        return self.quotation_repository.create_quotation(
            quotation_data,
            items,
        )

    # --------------------------------
    # Get Quotation
    # --------------------------------

    def get_quotation(
        self,
        quotation_id: int,
    ):

        return self.quotation_repository.get_quotation_details(
            quotation_id
        )

    # --------------------------------
    # Customer Quotations
    # --------------------------------

    def get_customer_quotations(
        self,
        customer_id: int,
    ):

        return self.quotation_repository.get_customer_quotations(
            customer_id
        )

    # --------------------------------
    # Delete
    # --------------------------------

    def delete_quotation(
        self,
        quotation_id: int,
    ):

        return self.quotation_repository.delete_quotation(
            quotation_id
        )

    # --------------------------------
    # Generate PDF
    # --------------------------------

    def generate_quotation_pdf(
        self,
        quotation_data: dict,
    ):

        return self.pdf_service.generate_quotation_pdf(
            quotation_data
        )