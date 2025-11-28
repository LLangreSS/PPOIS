import unittest
from warehouse.Container import Container
from products.Product import Product
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from suppliers.Supplier import Supplier
from products.UnitOfMeasure import UnitOfMeasure

class TestContainer(unittest.TestCase):
    def setUp(self):
        cat = ProductCategory("CAT", "Items")
        spec = ProductSpecification((0.1, 0.1, 0.1), 0.1)
        barcode = Barcode("1234567890123")
        supplier = Supplier("S", "Co", "e@mail.com")
        unit = UnitOfMeasure("pc", "piece")
        self.product = Product("P", "Item", cat, spec, barcode, supplier, unit)

    def test_valid_creation(self):
        c = Container("C-01", 10)
        self.assertEqual(c.max_capacity_items, 10)

    def test_add_product(self):
        c = Container("C-01", 5)
        c.add_product(self.product, 3)
        self.assertEqual(c.current_items(), 3)

    def test_add_zero_raises(self):
        c = Container("C-01", 5)
        with self.assertRaises(ValueError):
            c.add_product(self.product, 0)

    def test_exceed_capacity_raises(self):
        c = Container("C-01", 2)
        c.add_product(self.product, 2)
        with self.assertRaises(ValueError):
            c.add_product(self.product, 1)

    def test_is_empty(self):
        c = Container("C-01", 5)
        self.assertTrue(c.is_empty())
        c.add_product(self.product, 1)
        self.assertFalse(c.is_empty())