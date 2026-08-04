import unittest
from src.invox.services.customer_service import CustomerService
from src.invox.models.customer import Customer

class TestCustomerService(unittest.TestCase):

    def setUp(self):
        self.customer_service = CustomerService()
        self.test_customer = Customer(customer_id=1, name="John Doe", address="123 Elm St")

    def test_add_customer(self):
        result = self.customer_service.add_customer(self.test_customer)
        self.assertTrue(result)
        self.assertIn(self.test_customer, self.customer_service.get_all_customers())

    def test_edit_customer(self):
        self.customer_service.add_customer(self.test_customer)
        self.test_customer.name = "Jane Doe"
        result = self.customer_service.edit_customer(self.test_customer)
        self.assertTrue(result)
        self.assertEqual(self.customer_service.get_customer_by_id(1).name, "Jane Doe")

    def test_delete_customer(self):
        self.customer_service.add_customer(self.test_customer)
        result = self.customer_service.delete_customer(self.test_customer.customer_id)
        self.assertTrue(result)
        self.assertNotIn(self.test_customer, self.customer_service.get_all_customers())

    def test_get_customer_by_id(self):
        self.customer_service.add_customer(self.test_customer)
        customer = self.customer_service.get_customer_by_id(1)
        self.assertEqual(customer.name, "John Doe")

    def test_get_all_customers(self):
        self.customer_service.add_customer(self.test_customer)
        customers = self.customer_service.get_all_customers()
        self.assertGreater(len(customers), 0)

if __name__ == '__main__':
    unittest.main()