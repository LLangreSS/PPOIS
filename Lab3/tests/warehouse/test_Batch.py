import unittest
from datetime import datetime, timedelta
from products.Product import Product
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from suppliers.Supplier import Supplier
from products.UnitOfMeasure import UnitOfMeasure
from warehouse.StorageCondition import StorageCondition
from warehouse.Batch import Batch


class TestBatch(unittest.TestCase):
    def setUp(self):
        category = ProductCategory("cat1", "Test")
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0)
        barcode = Barcode("1234567890123")
        supplier = Supplier("sup1", "Test", "test@example.com")
        unit = UnitOfMeasure("pc", "piece")
        self.product = Product("p1", "Test", category, spec, barcode, supplier, unit)

    def test_init_valid(self):
        batch = Batch("B1", self.product, 100, datetime(2025, 1, 1))
        self.assertEqual(batch.id, "B1")
        self.assertIs(batch.product, self.product)
        self.assertEqual(batch.quantity, 100)
        self.assertEqual(batch.manufacture_date, datetime(2025, 1, 1))
        self.assertIsNone(batch.expiry_date)
        self.assertIsNone(batch.storage_condition)

    def test_init_with_expiry_and_condition(self):
        expiry = datetime(2026, 1, 1)
        cond = StorageCondition(temp_max=8.0)
        batch = Batch("B1", self.product, 50, datetime(2025, 1, 1), expiry, cond)
        self.assertEqual(batch.expiry_date, expiry)
        self.assertIs(batch.storage_condition, cond)

    def test_init_invalid_quantity(self):
        with self.assertRaises(ValueError) as cm:
            Batch("B1", self.product, 0, datetime.now())
        self.assertIn("Batch quantity must be positive", str(cm.exception))

    def test_is_expired_false_no_expiry(self):
        batch = Batch("B1", self.product, 10, datetime.now())
        self.assertFalse(batch.is_expired())

    def test_is_expired_false_future(self):
        batch = Batch("B1", self.product, 10, datetime.now(), datetime.now() + timedelta(days=10))
        self.assertFalse(batch.is_expired())

    def test_is_expired_true(self):
        batch = Batch("B1", self.product, 10, datetime.now(), datetime.now() - timedelta(days=1))
        self.assertTrue(batch.is_expired())

    def test_get_remaining_shelf_life_none(self):
        batch = Batch("B1", self.product, 10, datetime.now())
        self.assertIsNone(batch.get_remaining_shelf_life())

    def test_get_remaining_shelf_life_positive(self):
        expiry_date = datetime.now() + timedelta(days=15)
        batch = Batch("B1", self.product, 10, datetime.now(), expiry_date)
        remaining_days = batch.get_remaining_shelf_life()
        self.assertIsNotNone(remaining_days)
        self.assertGreaterEqual(remaining_days, 14)  # Может быть 14 или 15 в зависимости от времени выполнения

    def test_get_remaining_shelf_life_negative(self):
        expiry_date = datetime.now() - timedelta(days=5)
        batch = Batch("B1", self.product, 10, datetime.now(), expiry_date)
        remaining_days = batch.get_remaining_shelf_life()
        self.assertIsNotNone(remaining_days)
        self.assertLessEqual(remaining_days, -4)  # Может быть -4 или -5 в зависимости от времени выполнения

    def test_split_success(self):
        batch = Batch("B1", self.product, 100, datetime(2025, 1, 1))
        new_batch = batch.split(30)

        self.assertEqual(batch.quantity, 70)
        self.assertEqual(new_batch.quantity, 30)
        self.assertEqual(new_batch.product, self.product)
        self.assertEqual(new_batch.manufacture_date, datetime(2025, 1, 1))
        self.assertNotEqual(new_batch.id, "B1")  # Новый ID

    def test_split_invalid_quantity_equal(self):
        batch = Batch("B1", self.product, 100, datetime(2025, 1, 1))
        with self.assertRaises(ValueError) as cm:
            batch.split(100)
        self.assertIn("New quantity must be less than current quantity", str(cm.exception))

    def test_split_invalid_quantity_greater(self):
        batch = Batch("B1", self.product, 100, datetime(2025, 1, 1))
        with self.assertRaises(ValueError) as cm:
            batch.split(150)
        self.assertIn("New quantity must be less than current quantity", str(cm.exception))

    def test_split_with_storage_condition(self):
        cond = StorageCondition(temp_min=2.0, temp_max=8.0)
        expiry = datetime(2026, 1, 1)
        batch = Batch("B1", self.product, 100, datetime(2025, 1, 1), expiry, cond)

        new_batch = batch.split(40)

        self.assertEqual(new_batch.storage_condition, cond)
        self.assertEqual(new_batch.expiry_date, expiry)

    def test_is_expired_with_custom_time(self):
        expiry_date = datetime(2025, 1, 1)
        batch = Batch("B1", self.product, 10, datetime(2024, 1, 1), expiry_date)

        self.assertFalse(batch.is_expired(datetime(2024, 12, 31)))
        self.assertTrue(batch.is_expired(datetime(2025, 1, 2)))