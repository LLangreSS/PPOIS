import unittest
from warehouse.WarehouseConfig import WarehouseConfig
from warehouse.Warehouse import Warehouse
from warehouse.StorageZone import StorageZone
from warehouse.StorageCondition import StorageCondition
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from suppliers.Supplier import Supplier
from products.UnitOfMeasure import UnitOfMeasure
from products.Product import Product

class TestWarehouse(unittest.TestCase):
    def setUp(self):
        self.config = WarehouseConfig()
        self.warehouse = Warehouse("WH1", "Main", self.config)

    def test_init(self):
        self.assertEqual(self.warehouse.id, "WH1")
        self.assertEqual(self.warehouse.name, "Main")
        self.assertIs(self.warehouse.config, self.config)
        self.assertEqual(self.warehouse.zones, [])

    def test_add_zone(self):
        zone = StorageZone("Z1", "Test", StorageCondition())
        self.warehouse.add_zone(zone)
        self.assertIn(zone, self.warehouse.zones)

    def test_get_total_capacity(self):
        zone1 = StorageZone("Z1", "A", StorageCondition(), max_load_kg=1000.0)
        zone2 = StorageZone("Z2", "B", StorageCondition(), max_load_kg=2000.0)
        self.warehouse.add_zone(zone1)
        self.warehouse.add_zone(zone2)
        self.assertEqual(self.warehouse.get_total_capacity(), 3000.0)

    def test_get_current_utilization_empty(self):
        self.assertEqual(self.warehouse.get_current_utilization(), 0.0)

    def test_find_available_zone_no_zones(self):
        category = ProductCategory("c", "C")
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0)
        product = Product("p", "P", category, spec, Barcode("1234567890123"), Supplier("s", "S", "e@e.com"), UnitOfMeasure("pc", "p"))
        self.assertIsNone(self.warehouse.find_available_zone(product))

    def test_allocate_slot_success(self):
        zone = StorageZone("Z1", "Standard", StorageCondition())
        from warehouse.Shelf import Shelf
        shelf = Shelf("S1", "Z1", max_pallets=1)
        zone.add_shelf(shelf)
        self.warehouse.add_zone(zone)

        category = ProductCategory("c", "C")
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0)
        product = Product("p", "P", category, spec, Barcode("1234567890123"), Supplier("s", "S", "e@e.com"), UnitOfMeasure("pc", "p"))

        slot = self.warehouse.allocate_slot(product, 10)
        self.assertIsNotNone(slot)
        self.assertEqual(slot.quantity, 10)

    def test_allocate_slot_no_zone(self):
        category = ProductCategory("c", "C")
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0)
        product = Product("p", "P", category, spec, Barcode("1234567890123"), Supplier("s", "S", "e@e.com"), UnitOfMeasure("pc", "p"))
        from exceptions.SlotAllocationError import SlotAllocationError
        with self.assertRaises(SlotAllocationError) as cm:
            self.warehouse.allocate_slot(product, 10)
        self.assertIn("No suitable zone", str(cm.exception))