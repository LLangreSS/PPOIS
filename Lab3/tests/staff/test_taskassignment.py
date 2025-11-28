import unittest
from unittest.mock import Mock
from staff.TaskAssignment import TaskAssignment
from staff.Employee import Employee

class TestTaskAssignment(unittest.TestCase):
    def setUp(self):
        self.assignment = TaskAssignment("E1", "TASK-001", "Picking")

    def test_init_valid(self):
        self.assertEqual(self.assignment.employee_id, "E1")
        self.assertEqual(self.assignment.task_id, "TASK-001")
        self.assertEqual(self.assignment.task_type, "Picking")
        self.assertEqual(self.assignment.status, "assigned")

    def test_init_empty_task_type(self):
        with self.assertRaises(ValueError) as cm:
            TaskAssignment("E1", "T1", "")
        self.assertIn("Task type cannot be empty", str(cm.exception))

    def test_assign_to_correct_employee(self):
        mock_employee = Mock(spec=Employee)
        mock_employee.id = "E1"
        self.assignment.assign_to(mock_employee)
        self.assertEqual(self.assignment.status, "active")

    def test_assign_to_wrong_employee(self):
        mock_employee = Mock(spec=Employee)
        mock_employee.id = "E2"
        with self.assertRaises(ValueError) as cm:
            self.assignment.assign_to(mock_employee)
        self.assertIn("Employee ID mismatch", str(cm.exception))

    def test_complete(self):
        self.assignment.complete()
        self.assertEqual(self.assignment.status, "completed")

    def test_get_assignment_info(self):
        info = self.assignment.get_assignment_info()
        self.assertEqual(info["employee_id"], "E1")
        self.assertEqual(info["task_id"], "TASK-001")
        self.assertEqual(info["task_type"], "Picking")
        self.assertEqual(info["status"], "assigned")