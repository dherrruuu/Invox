import unittest
from invox.services.product_service import ProductService
from invox.models.product import Product

class TestProductService(unittest.TestCase):

    def setUp(self):
        self.product_service = ProductService()
        self.test_product = Product(product_id=1, name="Test Product", category="Test Category", rate=100.0)

    def test_add_product(self):
        result = self.product_service.add_product(self.test_product)
        self.assertTrue(result)
        self.assertIn(self.test_product, self.product_service.get_all_products())

    def test_edit_product(self):
        self.product_service.add_product(self.test_product)
        self.test_product.name = "Updated Product"
        result = self.product_service.edit_product(self.test_product)
        self.assertTrue(result)
        self.assertEqual(self.product_service.get_product_by_id(1).name, "Updated Product")

    def test_delete_product(self):
        self.product_service.add_product(self.test_product)
        result = self.product_service.delete_product(self.test_product.product_id)
        self.assertTrue(result)
        self.assertNotIn(self.test_product, self.product_service.get_all_products())

    def test_get_all_products(self):
        self.product_service.add_product(self.test_product)
        products = self.product_service.get_all_products()
        self.assertGreater(len(products), 0)

    def test_get_product_by_id(self):
        self.product_service.add_product(self.test_product)
        product = self.product_service.get_product_by_id(1)
        self.assertEqual(product.name, "Test Product")

if __name__ == '__main__':
    unittest.main()