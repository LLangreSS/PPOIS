import unittest
from warehouse.StorageCondition import StorageCondition

class TestStorageCondition(unittest.TestCase):
    def test_init_defaults(self):
        sc = StorageCondition()
        self.assertEqual(sc.temp_min, -float('inf'))
        self.assertEqual(sc.temp_max, float('inf'))
        self.assertEqual(sc.humidity_max, 100.0)
        self.assertFalse(sc.requires_ventilation)
        self.assertFalse(sc.light_sensitive)

    def test_init_custom(self):
        sc = StorageCondition(
            temp_min=2.0,
            temp_max=8.0,
            humidity_max=60.0,
            requires_ventilation=True,
            light_sensitive=True
        )
        self.assertEqual(sc.temp_min, 2.0)
        self.assertEqual(sc.temp_max, 8.0)
        self.assertEqual(sc.humidity_max, 60.0)
        self.assertTrue(sc.requires_ventilation)
        self.assertTrue(sc.light_sensitive)

    def test_satisfied_by_true(self):
        sc = StorageCondition(temp_min=0, temp_max=25, humidity_max=70)
        self.assertTrue(sc.satisfied_by(20.0, 60.0))

    def test_satisfied_by_false_temp_low(self):
        sc = StorageCondition(temp_min=5, temp_max=25)
        self.assertFalse(sc.satisfied_by(3.0, 50.0))

    def test_satisfied_by_false_temp_high(self):
        sc = StorageCondition(temp_min=5, temp_max=25)
        self.assertFalse(sc.satisfied_by(30.0, 50.0))

    def test_satisfied_by_false_humidity(self):
        sc = StorageCondition(humidity_max=60)
        self.assertFalse(sc.satisfied_by(20.0, 70.0))

    def test_get_condition_description_standard(self):
        sc = StorageCondition()
        self.assertEqual(sc.get_condition_description(), "Standard conditions")

    def test_get_condition_description_all(self):
        sc = StorageCondition(
            temp_min=2.0,
            temp_max=8.0,
            humidity_max=60.0,
            requires_ventilation=True,
            light_sensitive=True
        )
        desc = sc.get_condition_description()
        self.assertIn("Temperature: 2.0°C - 8.0°C", desc)
        self.assertIn("Humidity: up to 60.0%", desc)
        self.assertIn("Ventilation required", desc)
        self.assertIn("Light sensitive", desc)