import unittest
from warehouse.StorageCondition import StorageCondition
from warehouse.StorageZone import StorageZone
from warehouse.Shelf import Shelf
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from suppliers.Supplier import Supplier
from products.UnitOfMeasure import UnitOfMeasure
from products.Product import Product

class TestStorageZone(unittest.TestCase):
    def setUp(self):
        self.condition = StorageCondition(temp_max=8.0, humidity_max=60.0)
        self.zone = StorageZone("Z1", "Refrigerated", self.condition, max_load_kg=5000.0)

    def test_init(self):
        self.assertEqual(self.zone.id, "Z1")
        self.assertEqual(self.zone.name, "Refrigerated")
        self.assertIs(self.zone.condition, self.condition)
        self.assertEqual(self.zone.max_load_kg, 5000.0)
        self.assertEqual(self.zone.shelves, [])

    def test_current_load_empty(self):
        self.assertEqual(self.zone.current_load(), 0.0)

    def test_current_load_with_pallets(self):
        shelf = Shelf("S1", "Z1")
        from warehouse.Location import Location
        from warehouse.Pallet import Pallet
        from warehouse.Batch import Batch
        from datetime import datetime
        category = ProductCategory("cat1", "Test")
        spec = ProductSpecification((0.1, 0.1, 0.1), 10.0)
        barcode = Barcode("1234567890123")
        supplier = Supplier("sup1", "Test", "test@example.com")
        unit = UnitOfMeasure("pc", "piece")
        product = Product("p1", "Test", category, spec, barcode, supplier, unit)
        batch = Batch("B1", product, 5, datetime.now())
        pallet = Pallet("P1", Location("R1", "1", "S1", "Z1"))
        pallet.add_batch(batch)
        shelf.add_pallet(pallet)
        self.zone.add_shelf(shelf)
        self.assertAlmostEqual(self.zone.current_load(), 50.0)

    def test_is_compatible_cold(self):
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0, storage_notes="cold storage")
        product = Product("p1", "Vaccine", ProductCategory("c", "C"), spec, Barcode("1234567890123"), Supplier("s", "S", "e@e.com"), UnitOfMeasure("pc", "p"))
        self.assertTrue(self.zone.is_compatible(product))

    def test_is_compatible_dry(self):
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0, storage_notes="dry")
        product = Product("p1", "Flour", ProductCategory("c", "C"), spec, Barcode("1234567890123"), Supplier("s", "S", "e@e.com"), UnitOfMeasure("pc", "p"))
        dry_condition = StorageCondition(humidity_max=50.0)
        dry_zone = StorageZone("Z2", "Dry", dry_condition)
        self.assertTrue(dry_zone.is_compatible(product))

    def test_is_compatible_standard(self):
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0)
        product = Product("p1", "Book", ProductCategory("c", "C"), spec, Barcode("1234567890123"), Supplier("s", "S", "e@e.com"), UnitOfMeasure("pc", "p"))
        self.assertTrue(self.zone.is_compatible(product))

    def test_find_available_shelf_found(self):
        shelf = Shelf("S1", "Z1", max_pallets=1)
        self.zone.add_shelf(shelf)
        self.assertIs(self.zone.find_available_shelf(), shelf)

    def test_find_available_shelf_none(self):
        shelf = Shelf("S1", "Z1", max_pallets=1)
        from warehouse.Location import Location
        from warehouse.Pallet import Pallet
        shelf.add_pallet(Pallet("P1", Location("R1", "1", "S1", "Z1")))
        self.zone.add_shelf(shelf)
        self.assertIsNone(self.zone.find_available_shelf())

    def test_add_shelf(self):
        shelf = Shelf("S1", "Z1")
        self.zone.add_shelf(shelf)
        self.assertIn(shelf, self.zone.shelves)

    def test_get_utilization_percentage(self):
        self.zone.shelves = []
        self.assertEqual(self.zone.get_utilization_percentage(), 0.0)