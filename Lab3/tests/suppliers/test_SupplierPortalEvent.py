import unittest
from suppliers.SupplierPortalEvent import SupplierPortalEvent
from suppliers.Supplier import Supplier

class TestSupplierPortalEvent(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "Alpha", "a@b.com")

    def test_valid_creation(self):
        event = SupplierPortalEvent("delivery_confirmation", self.supplier, {"delivery_id": "D1"})
        self.assertEqual(event.event_type, "delivery_confirmation")

    def test_empty_type_raises(self):
        with self.assertRaises(ValueError):
            SupplierPortalEvent("", self.supplier, {})

    def test_is_confirmation(self):
        event = SupplierPortalEvent("delivery_confirmation", self.supplier, {})
        self.assertTrue(event.is_confirmation())
        event2 = SupplierPortalEvent("invoice_sent", self.supplier, {})
        self.assertFalse(event2.is_confirmation())

    def test_to_log_entry(self):
        event = SupplierPortalEvent("test", self.supplier, {})
        log = event.to_log_entry()
        self.assertIn("S1", log)
        self.assertIn("test", log)