import unittest
from src.invox.services.pdf_service import PDFService

class TestPDFService(unittest.TestCase):

    def setUp(self):
        self.pdf_service = PDFService()

    def test_generate_invoice_pdf(self):
        invoice_data = {
            'invoice_number': 'INV-001',
            'date': '2023-10-01',
            'customer_name': 'John Doe',
            'items': [
                {'description': 'Product 1', 'quantity': 2, 'price': 50.00},
                {'description': 'Product 2', 'quantity': 1, 'price': 100.00}
            ],
            'total': 200.00
        }
        pdf_path = self.pdf_service.generate_invoice_pdf(invoice_data)
        self.assertTrue(pdf_path.endswith('.pdf'))

    def test_generate_quotation_pdf(self):
        quotation_data = {
            'quotation_number': 'QT-001',
            'date': '2023-10-01',
            'customer_name': 'Jane Smith',
            'items': [
                {'description': 'Service 1', 'quantity': 1, 'price': 150.00},
                {'description': 'Service 2', 'quantity': 3, 'price': 75.00}
            ],
            'total': 375.00
        }
        pdf_path = self.pdf_service.generate_quotation_pdf(quotation_data)
        self.assertTrue(pdf_path.endswith('.pdf'))

if __name__ == '__main__':
    unittest.main()