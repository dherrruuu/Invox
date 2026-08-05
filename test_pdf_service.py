"""
Test PDF Generation
"""

import sys
from pathlib import Path

# -------------------------------------------------
# Add src to Python path
# -------------------------------------------------

sys.path.insert(
    0,
    str(Path(__file__).parent / "src")
)

# -------------------------------------------------
# Imports
# -------------------------------------------------

from invox.repositories.invoice_repository import InvoiceRepository
from invox.services.pdf_service import PDFService

# -------------------------------------------------
# Test
# -------------------------------------------------

print("=" * 60)
print("Starting PDF Test...")
print("=" * 60)

repository = InvoiceRepository()

print("Fetching invoice from database...")

# Change this ID if needed
invoice = repository.get_invoice_details(1)

if not invoice:
    print("ERROR: Invoice not found.")
    sys.exit()

print("Invoice Found")
print(f"Invoice Number : {invoice.get('invoice_number')}")
print(f"Customer       : {invoice.get('customer_name')}")
print(f"Items          : {len(invoice.get('items', []))}")

print("\nLoading PDF Service...")

service = PDFService()

print("Generating PDF...")

try:

    pdf_path = service.generate_invoice_pdf(invoice)

    print("\n" + "=" * 60)
    print("PDF GENERATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Saved To : {pdf_path}")

except Exception as e:

    print("\nPDF Generation Failed")
    print(type(e).__name__)
    print(e)