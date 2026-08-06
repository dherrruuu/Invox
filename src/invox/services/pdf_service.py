"""
PDF Service
"""

from pathlib import Path

from invox.config import APP_CONFIG
from invox.pdf.builder import InvoiceBuilder
from invox.utils.amount_to_words import amount_to_words


class PDFService:

    def __init__(
        self,
        invoice_dir=None,
        quotation_dir=None,
    ):

        self.invoice_dir = Path(
            invoice_dir or APP_CONFIG.bills_dir
        )

        self.quotation_dir = Path(
            quotation_dir or APP_CONFIG.quotations_dir
        )

        self.invoice_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.quotation_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -------------------------------------------------
    # Invoice
    # -------------------------------------------------

    def generate_invoice_pdf(
        self,
        invoice_data: dict,
    ):

        invoice_code = (
            invoice_data.get("invoice_code")
            or f"INV-{invoice_data.get('invoice_number', '0001')}"
        )

        file_path = (
            self.invoice_dir
            / f"{invoice_code}.pdf"
        )

        grand_total = float(
            invoice_data.get(
                "grand_total",
                0,
            )
        )

        company = {

            "company_name":
                invoice_data.get(
                    "company_name",
                    "BALAJI WOOD DECOR",
                ),

            "company_tagline":
                invoice_data.get(
                    "company_tagline",
                    "Interior | Furniture | Turnkey Works",
                ),

            "company_address":
                invoice_data.get(
                    "company_address",
                    "",
                ),

            "company_phone":
                invoice_data.get(
                    "company_phone",
                    "",
                ),

            "company_gstin":
                invoice_data.get(
                    "company_gstin",
                    "",
                ),

        }

        customer = {

            "name":
                invoice_data.get(
                    "customer_name",
                    "",
                ),

            "address":
                invoice_data.get(
                    "customer_address",
                    "",
                ),

            "phone":
                invoice_data.get(
                    "customer_phone",
                    "",
                ),

            "gstin":
                invoice_data.get(
                    "customer_gstin",
                    "",
                ),

        }

        invoice = {

            "invoice_no":
                invoice_code,

            "date":
                invoice_data.get(
                    "date",
                    "",
                ),

            "gstin":
                invoice_data.get(
                    "customer_gstin",
                    "",
                ),

            "place":
                invoice_data.get(
                    "place",
                    "",
                ),

            "payment":
                invoice_data.get(
                    "payment_mode",
                    "",
                ),

            "subject":
                invoice_data.get(
                    "subject",
                    "",
                ),

            "subtotal":
                float(
                    invoice_data.get(
                        "subtotal",
                        0,
                    )
                ),

            "gst":
                float(
                    invoice_data.get(
                        "gst_amount",
                        0,
                    )
                ),

            "discount":
                float(
                    invoice_data.get(
                        "discount_amount",
                        0,
                    )
                ),

            "roundoff":
                float(
                    invoice_data.get(
                        "roundoff",
                        0,
                    )
                ),

            "grand_total":
                grand_total,

            "amount_in_words":
                amount_to_words(
                    grand_total
                ),

            "bank_details":
                invoice_data.get(
                    "bank_details",
                    "",
                ),

        }

        items = invoice_data.get(
            "items",
            [],
        )

        builder = InvoiceBuilder()

        return builder.build(
            file_path=file_path,
            company=company,
            customer=customer,
            invoice=invoice,
            items=items,
        )

    # -------------------------------------------------
    # Quotation
    # -------------------------------------------------

    def generate_quotation_pdf(
        self,
        quotation_data: dict,
    ):

        raise NotImplementedError(
            "Quotation PDF is under development."
        )