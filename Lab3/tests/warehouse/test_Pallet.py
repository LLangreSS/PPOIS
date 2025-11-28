import unittest
from datetime import datetime
from warehouse.Location import Location
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from suppliers.Supplier import Supplier
from products.UnitOfMeasure import UnitOfMeasure
from products.Product import Product
from warehouse.Batch import Batch
from warehouse.Pallet import Pallet
from exceptions.OverloadedPalletError import OverloadedPalletError

class TestPallet(unittest.TestCase):

    def setUp(self):
        category = ProductCategory("cat1", "Test")
        spec = ProductSpecification((0.5, 0.4, 0.3), 10.0)  # 10 кг
        barcode = Barcode("1234567890123")
        supplier = Supplier("sup1", "Test", "test@example.com")
        unit = UnitOfMeasure("pc", "piece")
        self.product = Product("p1", "Heavy Item", category, spec, barcode, supplier, unit)
        self.location = Location("A", "1", "S1", "ZONE1")

    def test_init(self):
        pallet = Pallet("P1", self.location, max_weight=100.0)
        self.assertEqual(pallet.id, "P1")
        self.assertIs(pallet.location, self.location)
        self.assertEqual(pallet.max_weight, 100.0)
        self.assertEqual(pallet.batches, [])

    def test_total_weight_empty(self):
        pallet = Pallet("P1", self.location)
        self.assertEqual(pallet.total_weight, 0.0)

    def test_total_weight_with_batches(self):
        pallet = Pallet("P1", self.location, max_weight=200.0)
        batch1 = Batch("B1", self.product, 5, datetime.now())  # 5 * 10 = 50 кг
        batch2 = Batch("B2", self.product, 10, datetime.now()) # 10 * 10 = 100 кг
        pallet.add_batch(batch1)
        pallet.add_batch(batch2)
        self.assertEqual(pallet.total_weight, 150.0)

    def test_remaining_capacity_kg(self):
        pallet = Pallet("P1", self.location, max_weight=100.0)
        batch = Batch("B1", self.product, 8, datetime.now())  # 80 кг
        pallet.add_batch(batch)
        self.assertEqual(pallet.remaining_capacity_kg, 20.0)

    def test_max_dimensions(self):
        pallet = Pallet("P1", self.location)
        self.assertEqual(pallet.max_dimensions, (120.0, 100.0, 150.0))

    def test_add_batch_success(self):
        pallet = Pallet("P1", self.location, max_weight=100.0)
        batch = Batch("B1", self.product, 5, datetime.now())  # 50 кг
        pallet.add_batch(batch)
        self.assertIn(batch, pallet.batches)

    def test_add_batch_overload(self):
        pallet = Pallet("P1", self.location, max_weight=30.0)
        batch = Batch("B1", self.product, 5, datetime.now())  # 50 кг > 30
        with self.assertRaises(OverloadedPalletError) as cm:
            pallet.add_batch(batch)
        self.assertIn("would exceed maximum weight", str(cm.exception))

    def test_is_overloaded_false(self):
        pallet = Pallet("P1", self.location, max_weight=100.0)
        batch = Batch("B1", self.product, 5, datetime.now())
        pallet.add_batch(batch)
        self.assertFalse(pallet.is_overloaded())

    def test_is_overloaded_true(self):
        pallet = Pallet("P1", self.location, max_weight=30.0)
        batch = Batch("B1", self.product, 5, datetime.now())
        pallet.batches.append(batch)
        self.assertTrue(pallet.is_overloaded())

    def test_get_batch_by_product_found(self):
        pallet = Pallet("P1", self.location)
        batch = Batch("B1", self.product, 5, datetime.now())
        pallet.add_batch(batch)
        found = pallet.get_batch_by_product("p1")
        self.assertIs(found, batch)

    def test_get_batch_by_product_not_found(self):
        pallet = Pallet("P1", self.location)
        batch = Batch("B1", self.product, 5, datetime.now())
        pallet.add_batch(batch)
        found = pallet.get_batch_by_product("unknown")
        self.assertIsNone(found)

    def test_remove_batch_found(self):
        pallet = Pallet("P1", self.location)
        batch = Batch("B1", self.product, 5, datetime.now())
        pallet.add_batch(batch)
        result = pallet.remove_batch("B1")
        self.assertTrue(result)
        self.assertNotIn(batch, pallet.batches)

    def test_remove_batch_not_found(self):
        pallet = Pallet("P1", self.location)
        result = pallet.remove_batch("B999")
        self.assertFalse(result)