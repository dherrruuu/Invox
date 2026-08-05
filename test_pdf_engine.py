from pathlib import Path
import sys

sys.path.insert(
    0,
    str(Path(__file__).parent / "src")
)

from invox.services.pdf_service import PDFService


invoice = {

    "company_name":"BALAJI WOOD DECOR",

    "company_address":"Bangalore, Karnataka",

    "company_phone":"9876543210",

    "company_gst":"29ABCDE1234F1Z5",

    "customer_name":"ABC Interiors",

    "customer_address":"JP Nagar\nBangalore",

    "customer_phone":"9988776655",

    "customer_gst":"29AAAAA0000A1Z5",

    "invoice_code":"INV-0001",

    "date":"05-08-2026",

    "items":[

        {
            "section":True,
            "description":"Living Area"
        },

        {
            "description":"TV Unit",
            "unit":"SFT",
            "nos":1,
            "length":8,
            "height":7,
            "quantity":56,
            "rate":1450,
            "amount":81200,
            "remarks":""
        },

        {
            "description":"Wall Panel",
            "unit":"SFT",
            "nos":1,
            "length":12,
            "height":7,
            "quantity":84,
            "rate":1250,
            "amount":105000,
            "remarks":""
        },

        {
            "section":True,
            "description":"Kitchen"
        },

        {
            "description":"Base Unit",
            "unit":"SFT",
            "nos":1,
            "length":15,
            "height":3,
            "quantity":45,
            "rate":1600,
            "amount":72000,
            "remarks":""
        }

    ],

    "subtotal":258200,

    "gst_amount":46476,

    "discount_amount":5000,

    "grand_total":299676,

    "bank_details":
"""Canara Bank
A/C No : 123456789
IFSC : CNRB0001234""",

    "terms_and_conditions":
"""Goods once sold will not be taken back.
Payment within 7 days.
Subject to Bangalore Jurisdiction."""
}


service = PDFService()

pdf = service.generate_invoice_pdf(invoice)

print()

print("PDF Generated Successfully")

print(pdf)