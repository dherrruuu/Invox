"""
Report Service
"""

from invox.repositories.invoice_repository import InvoiceRepository
from invox.repositories.customer_repository import CustomerRepository
from invox.repositories.product_repository import ProductRepository
from invox.repositories.quotation_repository import QuotationRepository


class ReportService:

    def __init__(self):

        self.invoice_repo = InvoiceRepository()
        self.customer_repo = CustomerRepository()
        self.product_repo = ProductRepository()
        self.quotation_repo = QuotationRepository()

    # -------------------------------------------------
    # Sales Report
    # -------------------------------------------------

    def generate_sales_report(
        self,
        start_date=None,
        end_date=None,
    ):

        invoices = self.invoice_repo.get_all()

        filtered = []

        total_sales = 0.0

        for invoice in invoices:

            invoice_date = invoice.get("date")

            if start_date and invoice_date:

                if str(invoice_date) < str(start_date):
                    continue

            if end_date and invoice_date:

                if str(invoice_date) > str(end_date):
                    continue

            filtered.append(invoice)

            total_sales += float(
                invoice.get(
                    "grand_total",
                    0,
                )
            )

        return {

            "total_sales": total_sales,

            "invoices": filtered,

        }

    # -------------------------------------------------
    # Customer Report
    # -------------------------------------------------

    def generate_customer_report(self):

        customers = self.customer_repo.get_all()

        return {

            "total_customers": len(customers),

            "customers": customers,

        }

    # -------------------------------------------------
    # Product Report
    # -------------------------------------------------

    def generate_product_report(self):

        products = self.product_repo.get_all()

        return {

            "total_products": len(products),

            "products": products,

        }

    # -------------------------------------------------
    # Quotation Report
    # -------------------------------------------------

    def generate_quotation_report(
        self,
        start_date=None,
        end_date=None,
    ):

        quotations = self.quotation_repo.get_all()

        filtered = []

        total_value = 0.0

        for quotation in quotations:

            quotation_date = quotation.get("date")

            if start_date and quotation_date:

                if str(quotation_date) < str(start_date):
                    continue

            if end_date and quotation_date:

                if str(quotation_date) > str(end_date):
                    continue

            filtered.append(quotation)

            total_value += float(

                quotation.get(

                    "grand_total",

                    0,

                )

            )

        return {

            "total_quotations": len(filtered),

            "total_value": total_value,

            "quotations": filtered,

        }