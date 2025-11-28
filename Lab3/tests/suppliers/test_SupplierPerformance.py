import unittest
from suppliers.SupplierPerformance import SupplierPerformance
from deliveries.Delivery import Delivery
from deliveries.DeliveryItem import DeliveryItem
from suppliers.Supplier import Supplier
from products.Product import Product
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from products.UnitOfMeasure import UnitOfMeasure

class TestSupplierPerformance(unittest.TestCase):
    def setUp(self):
        cat = ProductCategory("CAT", "Goods")
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0)
        barcode = Barcode("1234567890123")
        supplier = Supplier("S", "Co", "e@mail.com")
        unit = UnitOfMeasure("шт", "штука")
        product = Product("P", "Item", cat, spec, barcode, supplier, unit)

        item1 = DeliveryItem(product, 10)
        item2 = DeliveryItem(product, 5)
        self.del_full = Delivery("D1", supplier, [item1])
        self.del_partial = Delivery("D2", supplier, [item2])

        from deliveries.ReceivingReport import ReceivingReport
        from staff.Employee import Employee
        from staff.Role import Role
        from staff.Permission import Permission
        from staff.Shift import Shift
        from datetime import datetime
        perm = Permission("receive", "Delivery")
        role = Role("Receiver", [perm])
        shift = Shift(datetime(2025,1,1), datetime(2025,12,31), "WH-01")
        emp = Employee("E1", "John", role, shift)

        report_full = ReceivingReport("D1", [(product, 10)], emp)
        self.del_full.receive_items(report_full)

        report_partial = ReceivingReport("D2", [(product, 3)], emp)
        self.del_partial.receive_items(report_partial)

    def test_completeness_rate(self):
        perf = SupplierPerformance([self.del_full, self.del_partial])
        rate = perf.completeness_rate()
        self.assertEqual(rate, 0.5)

    def test_on_time_delivery_rate(self):
        perf = SupplierPerformance([self.del_full, self.del_partial])
        rate = perf.on_time_delivery_rate()
        self.assertEqual(rate, 1.0)