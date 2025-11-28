import unittest
from staff.Permission import Permission

class TestPermission(unittest.TestCase):

    def test_init(self):
        perm = Permission("receive_delivery", "Delivery")
        self.assertEqual(perm.action, "receive_delivery")
        self.assertEqual(perm.resource, "Delivery")

    def test_str_representation(self):
        perm = Permission("ship_order", "CustomerOrder")
        self.assertEqual(str(perm), "ship_order_CustomerOrder")

    def test_matches_true(self):
        perm = Permission("execute_transfer", "InternalTransfer")
        self.assertTrue(perm.matches("execute_transfer", "InternalTransfer"))

    def test_matches_false_action(self):
        perm = Permission("approve_return", "ReturnRequest")
        self.assertFalse(perm.matches("reject_return", "ReturnRequest"))

    def test_matches_false_resource(self):
        perm = Permission("approve_return", "ReturnRequest")
        self.assertFalse(perm.matches("approve_return", "RefundNote"))