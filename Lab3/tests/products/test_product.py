import unittest
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from suppliers.Supplier import Supplier
from products.UnitOfMeasure import UnitOfMeasure
from products.ProductTag import ProductTag
from products.Product import Product

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.category = ProductCategory("cat1", "Electronics")
        self.spec = ProductSpecification((0.2, 0.1, 0.1), 1.5, is_fragile=True)
        self.barcode = Barcode("1234567890123")
        self.supplier = Supplier("sup1", "ABC Inc", "contact@abc.com")
        self.unit = UnitOfMeasure("pc", "piece")

    def test_init(self):
        tags = [ProductTag("hazardous")]
        product = Product("p1", "Phone", self.category, self.spec, self.barcode, self.supplier, self.unit, tags)
        self.assertEqual(product.id, "p1")
        self.assertEqual(product.name, "Phone")
        self.assertIs(product.category, self.category)
        self.assertIs(product.spec, self.spec)
        self.assertIs(product.barcode, self.barcode)
        self.assertIs(product.supplier, self.supplier)
        self.assertIs(product.unit, self.unit)
        self.assertEqual(product.tags, tags)
        self.assertTrue(product.is_active)

    def test_is_hazardous_true(self):
        tag = ProductTag("hazardous")
        product = Product("p1", "Chem", self.category, self.spec, self.barcode, self.supplier, self.unit, [tag])
        self.assertTrue(product.is_hazardous())

    def test_is_hazardous_hazardous_uppercase(self):
        tag = ProductTag("HAZARDOUS")
        product = Product("p1", "Chem", self.category, self.spec, self.barcode, self.supplier, self.unit, [tag])
        self.assertTrue(product.is_hazardous())

    def test_is_hazardous_false(self):
        tag = ProductTag("regular")
        product = Product("p1", "Book", self.category, self.spec, self.barcode, self.supplier, self.unit, [tag])
        self.assertFalse(product.is_hazardous())

    def test_requires_special_storage_hazardous(self):
        tag = ProductTag("hazardous")
        product = Product("p1", "Chem", self.category, self.spec, self.barcode, self.supplier, self.unit, [tag])
        self.assertTrue(product.requires_special_storage())

    def test_requires_special_storage_fragile(self):
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0, is_fragile=True)
        product = Product("p1", "Glass", self.category, spec, self.barcode, self.supplier, self.unit)
        self.assertTrue(product.requires_special_storage())

    def test_requires_special_storage_temperature(self):
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0, min_temperature=2.0, max_temperature=8.0)
        product = Product("p1", "Vaccine", self.category, spec, self.barcode, self.supplier, self.unit)
        self.assertTrue(product.requires_special_storage())

    def test_requires_special_storage_none(self):
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0)
        product = Product("p1", "Book", self.category, spec, self.barcode, self.supplier, self.unit)
        self.assertFalse(product.requires_special_storage())

    def test_get_storage_requirements_all(self):
        tag = ProductTag("hazardous")
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0, is_fragile=True, min_temperature=2.0)
        product = Product("p1", "Vial", self.category, spec, self.barcode, self.supplier, self.unit, [tag])
        reqs = product.get_storage_requirements()
        self.assertIn("Hazardous materials", reqs)
        self.assertIn("Fragile goods", reqs)
        self.assertIn("Temperature control", reqs)
        self.assertEqual(len(reqs), 3)

    def test_validate_for_storage_valid(self):
        product = Product("p1", "Valid", self.category, self.spec, self.barcode, self.supplier, self.unit)
        self.assertTrue(product.validate_for_storage())

    def test_validate_for_storage_invalid_barcode(self):
        bad_barcode = Barcode("123")
        product = Product("p1", "Invalid", self.category, self.spec, bad_barcode, self.supplier, self.unit)
        self.assertFalse(product.validate_for_storage())

    def test_validate_for_storage_invalid_weight(self):
        bad_spec = ProductSpecification((0.1, 0.1, 0.1), 0.0)
        product = Product("p1", "Invalid", self.category, bad_spec, self.barcode, self.supplier, self.unit)
        self.assertFalse(product.validate_for_storage())

    def test_validate_for_storage_invalid_dimensions(self):
        bad_spec = ProductSpecification((0.0, 0.1, 0.1), 1.0)
        product = Product("p1", "Invalid", self.category, bad_spec, self.barcode, self.supplier, self.unit)
        self.assertFalse(product.validate_for_storage())