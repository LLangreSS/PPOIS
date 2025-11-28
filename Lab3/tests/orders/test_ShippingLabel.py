# test_ShippingLabel.py
import unittest
from unittest.mock import patch
from datetime import datetime
from orders.ShippingLabel import ShippingLabel


class TestShippingLabel(unittest.TestCase):

    def test_init_with_valid_data(self):
        label = ShippingLabel("TRACK-001", "Moscow", 2.5)
        self.assertEqual(label.tracking_number, "TRACK-001")
        self.assertEqual(label.destination, "Moscow")
        self.assertEqual(label.weight_kg, 2.5)
        self.assertIsInstance(label.created_date, datetime)

    def test_init_with_zero_weight_raises(self):
        with self.assertRaises(ValueError) as cm:
            ShippingLabel("T1", "Berlin", 0.0)
        self.assertEqual(str(cm.exception), "Weight must be positive")

    def test_init_with_negative_weight_raises(self):
        with self.assertRaises(ValueError) as cm:
            ShippingLabel("T1", "Paris", -1.5)
        self.assertEqual(str(cm.exception), "Weight must be positive")

    def test_print_outputs_correct_format(self):
        label = ShippingLabel("T1", "Saint Petersburg", 10.0)
        with patch('builtins.print') as mock_print:
            label.print()
            mock_print.assert_called_once_with(
                "[LABEL] TO: Saint Petersburg | TRACK: T1 | WT: 10.0kg"
            )

    def test_get_shipping_cost_uses_default_rate(self):
        label = ShippingLabel("T1", "Kazan", 3.0)
        self.assertAlmostEqual(label.get_shipping_cost(), 15.0)

    def test_get_shipping_cost_uses_custom_rate(self):
        label = ShippingLabel("T1", "Yekaterinburg", 4.0)
        self.assertAlmostEqual(label.get_shipping_cost(rate_per_kg=12.5), 50.0)

    def test_is_international_returns_false_for_domestic_cities(self):
        russian_cities = ["Moscow", "Saint Petersburg", "Novosibirsk", "Kazan", "Yekaterinburg"]
        for city in russian_cities:
            with self.subTest(city=city):
                label = ShippingLabel("T1", city, 1.0)
                self.assertFalse(label.is_international())

    def test_is_international_returns_true_for_foreign_cities(self):
        foreign_cities = ["Berlin", "Paris", "New York", "Tokyo"]
        for city in foreign_cities:
            with self.subTest(city=city):
                label = ShippingLabel("T1", city, 1.0)
                self.assertTrue(label.is_international())

    def test_is_international_is_case_sensitive(self):
        label = ShippingLabel("T1", "moscow", 1.0)
        self.assertTrue(label.is_international())