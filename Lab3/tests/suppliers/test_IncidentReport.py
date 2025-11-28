import unittest
from suppliers.IncidentReport import IncidentReport
from suppliers.Supplier import Supplier
from deliveries.Delivery import Delivery
from deliveries.DeliveryItem import DeliveryItem
from staff.Employee import Employee
from staff.Role import Role
from staff.Permission import Permission
from staff.Shift import Shift
from products.Product import Product
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from products.UnitOfMeasure import UnitOfMeasure
from datetime import datetime

class TestIncidentReport(unittest.TestCase):
    def setUp(self):
        cat = ProductCategory("CAT", "Goods")
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0)
        barcode = Barcode("1234567890123")
        self.supplier = Supplier("S", "Co", "e@mail.com")
        unit = UnitOfMeasure("pc", "piece")
        product = Product("P", "Item", cat, spec, barcode, self.supplier, unit)
        item = DeliveryItem(product, 10)
        self.delivery = Delivery("D1", self.supplier, [item])
        perm = Permission("report", "Incident")
        role = Role("Inspector", [perm])
        shift = Shift(datetime(2025, 1, 1), datetime(2025, 12, 31), "WH")
        self.reporter = Employee("E1", "Alice", role, shift)

    def test_valid_creation(self):
        report = IncidentReport(
            "IR-01", self.delivery, self.supplier, self.reporter,
            "Shortage of 3 units", "medium"
        )
        self.assertEqual(report.severity, "medium")

    def test_empty_description_raises(self):
        with self.assertRaises(ValueError):
            IncidentReport("IR", self.delivery, self.supplier, self.reporter, "", "low")

    def test_is_critical(self):
        report = IncidentReport("IR", self.delivery, self.supplier, self.reporter, "Defect", "high")
        self.assertTrue(report.is_critical())