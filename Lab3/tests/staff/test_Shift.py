import unittest
from unittest.mock import patch
from datetime import time, datetime
from staff.Shift import Shift

class TestShift(unittest.TestCase):

    def test_init_valid(self):
        shift = Shift(time(8, 0), time(16, 0), "WH1")
        self.assertEqual(shift.start_time, time(8, 0))
        self.assertEqual(shift.end_time, time(16, 0))
        self.assertEqual(shift.warehouse_id, "WH1")

    def test_init_invalid_start_after_end(self):
        with self.assertRaises(ValueError) as cm:
            Shift(time(17, 0), time(9, 0), "WH1")
        self.assertIn("End time must be after start time", str(cm.exception))

    @patch('staff.Shift.datetime')
    def test_is_active_true(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0)
        shift = Shift(time(9, 0), time(17, 0), "WH1")
        self.assertTrue(shift.is_active())

    @patch('staff.Shift.datetime')
    def test_is_active_false_before(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 1, 1, 8, 0)
        shift = Shift(time(9, 0), time(17, 0), "WH1")
        self.assertFalse(shift.is_active())

    @patch('staff.Shift.datetime')
    def test_is_active_false_after(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 1, 1, 18, 0)
        shift = Shift(time(9, 0), time(17, 0), "WH1")
        self.assertFalse(shift.is_active())

    def test_get_duration_hours(self):
        shift = Shift(time(8, 0), time(16, 0), "WH1")
        self.assertEqual(shift.get_duration_hours(), 8.0)

    def test_get_shift_type_night(self):
        shift = Shift(time(0, 0), time(8, 0), "WH1")
        self.assertEqual(shift.get_shift_type(), "night")

    def test_get_shift_type_morning(self):
        shift = Shift(time(6, 0), time(14, 0), "WH1")
        self.assertEqual(shift.get_shift_type(), "morning")

    def test_get_shift_type_day(self):
        shift = Shift(time(14, 0), time(22, 0), "WH1")
        self.assertEqual(shift.get_shift_type(), "day")