import unittest
from datetime import datetime
from unittest.mock import patch
from staff.Employee import Employee
from staff.Role import Role
from staff.Permission import Permission
from staff.Shift import Shift
from orders.RefundNote import RefundNote


class TestRefundNote(unittest.TestCase):

    def setUp(self):
        permissions = [Permission("process_refund", "RefundNote")]
        role = Role("RefundSpecialist", permissions)
        shift = Shift(
            start_time=datetime(2025, 1, 1, 8, 0),
            end_time=datetime(2025, 1, 1, 17, 0),
            warehouse_id="WH-01"
        )
        self.employee = Employee("EMP-101", "Иван Петров", role, shift)

    def test_valid_creation(self):
        refund = RefundNote("RETURN-2025-001", 150.75, self.employee)
        self.assertEqual(refund.return_id, "RETURN-2025-001")
        self.assertEqual(refund.amount, 150.75)
        self.assertEqual(refund.processed_by, self.employee)
        self.assertEqual(refund.status, "created")
        self.assertIsInstance(refund.processed_date, datetime)

    def test_invalid_amount_raises(self):
        with self.assertRaises(ValueError) as cm:
            RefundNote("RETURN-2025-001", -10.0, self.employee)
        self.assertEqual(str(cm.exception), "Refund amount must be positive")

        with self.assertRaises(ValueError) as cm:
            RefundNote("RETURN-2025-001", 0.0, self.employee)
        self.assertEqual(str(cm.exception), "Refund amount must be positive")

    def test_issue_updates_status(self):
        refund = RefundNote("RETURN-2025-001", 100.0, self.employee)
        self.assertEqual(refund.status, "created")
        result = refund.issue()
        self.assertTrue(result)
        self.assertEqual(refund.status, "issued")

    def test_get_refund_details_after_issue(self):
        refund = RefundNote("RETURN-2025-001", 50.0, self.employee)
        refund.issue()
        details = refund.get_refund_details()
        self.assertEqual(details["status"], "issued")