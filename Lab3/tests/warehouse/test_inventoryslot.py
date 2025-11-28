import unittest
from unittest.mock import Mock
from warehouse.InventorySlot import InventorySlot
from warehouse.ReservedSlot import ReservedSlot
from exceptions.InsufficientStockError import InsufficientStockError

class TestInventorySlot(unittest.TestCase):
    def setUp(self):
        self.mock_location = Mock()
        self.mock_batch = Mock()
        self.mock_batch.product.spec.weight_kg = 1.0
        self.slot = InventorySlot("SLOT-0001", self.mock_location, self.mock_batch, 100)

    def test_init_valid(self):
        self.assertEqual(self.slot.id, "SLOT-0001")
        self.assertIs(self.slot.location, self.mock_location)
        self.assertIs(self.slot.batch, self.mock_batch)
        self.assertEqual(self.slot.quantity, 100)
        self.assertEqual(self.slot.reserved_quantity, 0)

    def test_init_invalid_quantity_zero(self):
        with self.assertRaises(ValueError) as cm:
            InventorySlot("S1", self.mock_location, self.mock_batch, 0)
        self.assertEqual(str(cm.exception), "Quantity must be positive")

    def test_init_invalid_quantity_negative(self):
        with self.assertRaises(ValueError) as cm:
            InventorySlot("S1", self.mock_location, self.mock_batch, -5)
        self.assertEqual(str(cm.exception), "Quantity must be positive")

    def test_is_empty_false(self):
        self.assertFalse(self.slot.is_empty())

    def test_available_quantity_initial(self):
        self.assertEqual(self.slot.available_quantity(), 100)

    def test_available_quantity_after_reservation(self):
        self.slot.reserve(30, "ORDER-1")
        self.assertEqual(self.slot.available_quantity(), 70)

    def test_reserve_success(self):
        reserved = self.slot.reserve(25, "ORDER-1")
        self.assertIsInstance(reserved, ReservedSlot)
        self.assertEqual(self.slot.reserved_quantity, 25)
        self.assertEqual(reserved.reserved_quantity, 25)
        self.assertEqual(reserved.reserved_for, "ORDER-1")
        self.assertEqual(reserved.slot_id, "SLOT-0001")

    def test_reserve_insufficient_stock(self):
        with self.assertRaises(InsufficientStockError) as cm:
            self.slot.reserve(150, "ORDER-1")
        self.assertIn("Requested 150, available 100", str(cm.exception))

    def test_release_reservation_success(self):
        self.slot.reserve(40, "ORDER-1")
        self.slot.release_reservation(10)
        self.assertEqual(self.slot.reserved_quantity, 30)

    def test_release_reservation_too_much(self):
        self.slot.reserve(20, "ORDER-1")
        with self.assertRaises(ValueError) as cm:
            self.slot.release_reservation(25)
        self.assertEqual(str(cm.exception), "Cannot release more than reserved")

    def test_get_utilization_percentage(self):
        slot = InventorySlot("S3", self.mock_location, self.mock_batch, 75)
        self.assertEqual(slot.get_utilization_percentage(), 75.0)