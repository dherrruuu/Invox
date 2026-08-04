import unittest
from src.invox.services.invoice_service import InvoiceService
from src.invox.models.invoice import Invoice
from src.invox.models.customer import Customer

class TestInvoiceService(unittest.TestCase):

    def setUp(self):
        self.invoice_service = InvoiceService()
        self.customer = Customer(customer_id=1, name="John Doe", address="123 Elm St")
        self.invoice = Invoice(invoice_number=1001, customer=self.customer, date="2023-10-01")

    def test_create_invoice(self):
        result = self.invoice_service.create_invoice(self.invoice)
        self.assertTrue(result)
        self.assertEqual(result.invoice_number, 1001)

    def test_calculate_total(self):
        self.invoice.add_item("Product A", 2, 50)  # 2 items at $50 each
        self.invoice.add_item("Product B", 1, 100)  # 1 item at $100
        total = self.invoice_service.calculate_total(self.invoice)
        self.assertEqual(total, 200)

    def test_generate_invoice_pdf(self):
        self.invoice_service.create_invoice(self.invoice)
        pdf_result = self.invoice_service.generate_invoice_pdf(self.invoice)
        self.assertTrue(pdf_result)

    def tearDown(self):
        self.invoice_service = None
        self.invoice = None
        self.customer = None

if __name__ == '__main__':
    unittest.main()