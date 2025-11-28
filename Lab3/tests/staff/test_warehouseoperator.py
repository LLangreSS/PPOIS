import unittest
from unittest.mock import Mock
from datetime import time
from staff.Permission import Permission
from staff.Role import Role
from staff.Employee import Employee
from staff.Shift import Shift
from staff.WarehouseOperator import WarehouseOperator
from exceptions.UnauthorizedOperationError import UnauthorizedOperationError
from warehouse.InternalTransfer import InternalTransfer


class TestWarehouseOperator(unittest.TestCase):
    def setUp(self):
        self.shift = Mock(spec=Shift)
        self.shift.is_active.return_value = True
        perm1 = Permission("execute_transfer", "InternalTransfer")
        perm2 = Permission("handle_hazardous", "Product")
        role = Role("ForkliftOperator", [perm1, perm2])
        employee = Employee("OP1", "Bob", role, self.shift)
        self.operator = WarehouseOperator(employee)

    def test_init_valid_role(self):
        self.assertIsInstance(self.operator, WarehouseOperator)

    def test_init_invalid_role_not_operator(self):
        role = Role("Manager", [])
        employee = Employee("M1", "Charlie", role, self.shift)
        with self.assertRaises(UnauthorizedOperationError) as cm:
            WarehouseOperator(employee)
        self.assertIn("Employee is not a warehouse operator", str(cm.exception))

    def test_execute_transfer_success(self):
        transfer = Mock(spec=InternalTransfer)
        transfer.status = "pending"
        self.operator.execute_transfer(transfer)
        self.assertEqual(transfer.status, "executed_by_operator")

    def test_execute_transfer_unauthorized(self):
        role = Role("ForkliftOperator", [Permission("handle_hazardous", "Product")])
        employee = Employee("OP2", "Dave", role, self.shift)
        operator = WarehouseOperator(employee)
        transfer = Mock(spec=InternalTransfer)
        with self.assertRaises(UnauthorizedOperationError) as cm:
            operator.execute_transfer(transfer)
        self.assertIn("does not have permission to execute transfers", str(cm.exception))

    def test_can_handle_hazardous_true(self):
        self.assertTrue(self.operator.can_handle_hazardous())

    def test_can_handle_hazardous_false(self):
        role = Role("ForkliftOperator", [Permission("execute_transfer", "InternalTransfer")])
        employee = Employee("OP3", "Eve", role, self.shift)
        operator = WarehouseOperator(employee)
        self.assertFalse(operator.can_handle_hazardous())

    def test_get_operator_certifications(self):
        certs = self.operator.get_operator_certifications()
        expected = ["basic_training", "hazardous_materials"]
        self.assertEqual(set(certs), set(expected))

    def test_get_operator_certifications_with_forklift(self):
        perm1 = Permission("execute_transfer", "InternalTransfer")
        perm2 = Permission("handle_hazardous", "Product")
        perm3 = Permission("operate_forklift", "Equipment")
        role = Role("ForkliftOperator", [perm1, perm2, perm3])
        employee = Employee("OP4", "Frank", role, self.shift)
        operator = WarehouseOperator(employee)

        certs = operator.get_operator_certifications()
        expected = ["basic_training", "hazardous_materials", "forklift"]
        self.assertEqual(set(certs), set(expected))