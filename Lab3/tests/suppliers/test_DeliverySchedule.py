import unittest
from suppliers.DeliverySchedule import DeliverySchedule
from suppliers.Supplier import Supplier
from datetime import time

class TestDeliverySchedule(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S", "Co", "e@mail.com")
        self.schedule = DeliverySchedule(
            supplier=self.supplier,
            delivery_days=[0, 2, 4],  # Пн, Ср, Пт
            time_window_start=time(9, 0),
            time_window_end=time(17, 0)
        )

    def test_valid_day(self):
        self.assertTrue(self.schedule.is_valid_delivery_day(0))
        self.assertFalse(self.schedule.is_valid_delivery_day(1))

    def test_time_window(self):
        self.assertTrue(self.schedule.is_within_time_window(time(12, 0)))
        self.assertFalse(self.schedule.is_within_time_window(time(18, 0)))

    def test_invalid_input_raises(self):
        with self.assertRaises(ValueError):
            DeliverySchedule(self.supplier, [], time(9,0), time(17,0))
        with self.assertRaises(ValueError):
            DeliverySchedule(self.supplier, [0], time(17,0), time(9,0))