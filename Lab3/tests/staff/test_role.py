import unittest
from staff.Permission import Permission
from staff.Role import Role

class TestRole(unittest.TestCase):

    def setUp(self):
        self.perm1 = Permission("receive_delivery", "Delivery")
        self.perm2 = Permission("ship_order", "CustomerOrder")
        self.role = Role("Receiver", [self.perm1])

    def test_init(self):
        self.assertEqual(self.role.name, "Receiver")
        self.assertEqual(self.role.permissions, [self.perm1])

    def test_has_permission_exact_match(self):
        self.assertTrue(self.role.has_permission("receive_delivery", "Delivery"))
        self.assertFalse(self.role.has_permission("ship_order", "CustomerOrder"))

    def test_has_permission_action_only(self):
        self.assertTrue(self.role.has_permission("receive_delivery"))

    def test_add_permission(self):
        self.role.add_permission(self.perm2)
        self.assertIn(self.perm2, self.role.permissions)
        self.assertTrue(self.role.has_permission("ship_order", "CustomerOrder"))

    def test_remove_permission_found(self):
        self.role.add_permission(self.perm2)
        result = self.role.remove_permission("ship_order", "CustomerOrder")
        self.assertTrue(result)
        self.assertFalse(self.role.has_permission("ship_order", "CustomerOrder"))

    def test_remove_permission_not_found(self):
        result = self.role.remove_permission("ship_order", "CustomerOrder")
        self.assertFalse(result)