import unittest
from staff.ReplenishmentTask import ReplenishmentTask
from products.Product import Product
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from suppliers.Supplier import Supplier
from products.UnitOfMeasure import UnitOfMeasure
from warehouse.Location import Location

class TestReplenishmentTask(unittest.TestCase):
    def setUp(self):
        cat = ProductCategory("CAT-01", "Electronics")
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0)
        barcode = Barcode("1234567890123")
        supplier = Supplier("SUP-01", "TechCo", "contact@techco.com")
        unit = UnitOfMeasure("pc", "piece")
        self.product = Product("PROD-01", "Phone", cat, spec, barcode, supplier, unit)
        self.src = Location("A", "1", "S1", "ZONE-RESERVE")
        self.dst = Location("B", "2", "P1", "ZONE-PICKING")

    def test_valid_creation(self):
        task = ReplenishmentTask("TASK-01", self.product, 10, self.src, self.dst)
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.quantity, 10)

    def test_invalid_quantity_raises(self):
        with self.assertRaises(ValueError):
            ReplenishmentTask("TASK-01", self.product, 0, self.src, self.dst)

    def test_same_location_raises(self):
        same_loc = Location("A", "1", "S1", "ZONE-RESERVE")
        with self.assertRaises(ValueError):
            ReplenishmentTask("TASK-01", self.product, 5, self.src, same_loc)

    def test_complete_changes_status(self):
        task = ReplenishmentTask("TASK-01", self.product, 5, self.src, self.dst)
        task.complete()
        self.assertEqual(task.status, "completed")

    def test_is_urgent(self):
        task = ReplenishmentTask("TASK-01", self.product, 5, self.src, self.dst)
        self.assertTrue(task.is_urgent(2, 5))
        self.assertFalse(task.is_urgent(6, 5))