import unittest
from warehouse.ReservedSlot import ReservedSlot
from datetime import datetime, timedelta

class TestReservedSlot(unittest.TestCase):

    def test_init(self):
        rs = ReservedSlot("SLOT1", 10, "ORDER123")
        self.assertEqual(rs.slot_id, "SLOT1")
        self.assertEqual(rs.reserved_quantity, 10)
        self.assertEqual(rs.reserved_for, "ORDER123")
        self.assertIsInstance(rs.reserved_at, datetime)

    def test_release(self):
        rs = ReservedSlot("SLOT1", 5, "ORD1")
        payload = rs.release()
        self.assertEqual(payload["slot_id"], "SLOT1")
        self.assertEqual(payload["quantity_to_restore"], 5)
        self.assertEqual(payload["reserved_for"], "ORD1")

    def test_is_expired_false(self):
        rs = ReservedSlot("S1", 1, "O1")
        self.assertFalse(rs.is_expired(expiry_minutes=30))

    def test_is_expired_true(self):
        rs = ReservedSlot("S1", 1, "O1")
        rs.reserved_at = datetime.now() - timedelta(minutes=35)
        self.assertTrue(rs.is_expired(expiry_minutes=30))

    def test_is_expired_zero_minutes(self):
        rs = ReservedSlot("S1", 1, "O1")
        rs.reserved_at = datetime.now() - timedelta(seconds=1)
        self.assertTrue(rs.is_expired(expiry_minutes=0))