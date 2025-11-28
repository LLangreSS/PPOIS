import unittest
from datetime import datetime
from unittest.mock import Mock
from warehouse.InternalTransfer import InternalTransfer
from products.Product import Product
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from suppliers.Supplier import Supplier
from products.UnitOfMeasure import UnitOfMeasure

class TestInternalTransfer(unittest.TestCase):
    def setUp(self):
        category = ProductCategory("cat1", "Test")
        spec = ProductSpecification((0.1, 0.1, 0.1), 1.0)
        barcode = Barcode("1234567890123")
        supplier = Supplier("sup1", "Test", "test@example.com")
        unit = UnitOfMeasure("pc", "piece")
        self.product = Product("P1", "Test", category, spec, barcode, supplier, unit)

    def test_init_valid(self):
        transfer = InternalTransfer(
            id="TR-001",
            product=self.product,
            quantity=50,
            source_location="ZONE-A/S1",
            destination_location="ZONE-B/S2"
        )
        self.assertEqual(transfer.id, "TR-001")
        self.assertIs(transfer.product, self.product)
        self.assertEqual(transfer.quantity, 50)
        self.assertEqual(transfer.source_location, "ZONE-A/S1")
        self.assertEqual(transfer.destination_location, "ZONE-B/S2")
        self.assertEqual(transfer.status, "pending")
        self.assertIsInstance(transfer.created_at, datetime)
        self.assertIsNone(transfer.completed_at)

    def test_init_invalid_quantity_zero(self):
        with self.assertRaises(ValueError) as cm:
            InternalTransfer("T1", self.product, 0, "A", "B")
        self.assertEqual(str(cm.exception), "Transfer quantity must be positive")

    def test_init_invalid_quantity_negative(self):
        with self.assertRaises(ValueError) as cm:
            InternalTransfer("T1", self.product, -5, "A", "B")
        self.assertEqual(str(cm.exception), "Transfer quantity must be positive")

    def test_init_same_source_and_destination(self):
        with self.assertRaises(ValueError) as cm:
            InternalTransfer("T1", self.product, 10, "LOC-1", "LOC-1")
        self.assertEqual(str(cm.exception), "Source and destination must be different")

    def test_execute_success(self):
        transfer = InternalTransfer("T1", self.product, 10, "A", "B")
        self.assertEqual(transfer.status, "pending")
        transfer.execute("OP-001")
        self.assertEqual(transfer.status, "executed_by_operator")
        self.assertIsInstance(transfer.completed_at, datetime)

    def test_execute_already_completed(self):
        transfer = InternalTransfer("T1", self.product, 10, "A", "B")
        transfer.execute("OP-001")
        with self.assertRaises(ValueError) as cm:
            transfer.execute("OP-002")
        self.assertEqual(str(cm.exception), "Transfer already processed")

    def test_is_completed_false_initially(self):
        transfer = InternalTransfer("T1", self.product, 10, "A", "B")
        self.assertFalse(transfer.is_completed())

    def test_is_completed_true_after_execute(self):
        transfer = InternalTransfer("T1", self.product, 10, "A", "B")
        transfer.execute("OP-001")
        self.assertTrue(transfer.is_completed())

    def test_get_transfer_summary(self):
        transfer = InternalTransfer("TR-100", self.product, 25, "WH1-Z1", "WH1-Z2")
        summary = transfer.get_transfer_summary()
        self.assertEqual(summary["id"], "TR-100")
        self.assertEqual(summary["product_id"], "P1")
        self.assertEqual(summary["quantity"], 25)
        self.assertEqual(summary["from"], "WH1-Z1")
        self.assertEqual(summary["to"], "WH1-Z2")
        self.assertEqual(summary["status"], "pending")
        self.assertIsInstance(summary["created_at"], datetime)