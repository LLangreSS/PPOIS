import unittest
from unittest.mock import patch, Mock
from staff.Permission import Permission
from staff.Role import Role
from staff.Shift import Shift
from staff.Employee import Employee

class TestEmployee(unittest.TestCase):
    def setUp(self):
        perm = Permission("receive_delivery", "Delivery")
        self.role = Role("Receiver", [perm])
        self.shift = Mock(spec=Shift)
        self.shift.is_active.return_value = True
        self.employee = Employee("E1", "Alice", self.role, self.shift)

    def test_init(self):
        self.assertEqual(self.employee.id, "E1")
        self.assertEqual(self.employee.name, "Alice")
        self.assertIs(self.employee.role, self.role)
        self.assertIs(self.employee.shift, self.shift)
        self.assertTrue(self.employee.is_active)

    @patch('staff.Shift.datetime')
    def test_can_perform_true(self, mock_datetime):
        from datetime import datetime
        mock_datetime.now.return_value = datetime(2025, 1, 1, 10, 0)
        self.assertTrue(self.employee.can_perform("receive_delivery", "Delivery"))

    @patch('staff.Shift.datetime')
    def test_can_perform_false_wrong_permission(self, mock_datetime):
        from datetime import datetime
        mock_datetime.now.return_value = datetime(2025, 1, 1, 10, 0)
        self.assertFalse(self.employee.can_perform("ship_order", "CustomerOrder"))

    def test_get_employee_info_active_shift(self):
        with patch('staff.Shift.datetime') as mock_dt:
            from datetime import datetime
            mock_dt.now.return_value = datetime(2025, 1, 1, 12, 0)
            info = self.employee.get_employee_info()
        self.assertEqual(info["id"], "E1")
        self.assertEqual(info["name"], "Alice")
        self.assertEqual(info["role"], "Receiver")
        self.assertTrue(info["shift_active"])
        self.assertEqual(info["status"], "active")

    def test_transfer_to_role(self):
        new_role = Role("Shipper", [])
        self.employee.transfer_to_role(new_role)
        self.assertIs(self.employee.role, new_role)