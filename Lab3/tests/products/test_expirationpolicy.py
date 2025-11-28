import unittest
from datetime import datetime, timedelta
from products.ExpirationPolicy import ExpirationPolicy


class TestExpirationPolicy(unittest.TestCase):
    def setUp(self):
        self.policy = ExpirationPolicy(shelf_life_days=30, requires_cold_chain=True)

    def test_init(self):
        self.assertEqual(self.policy.shelf_life_days, 30)
        self.assertTrue(self.policy.requires_cold_chain)

    def test_calculate_expiry(self):
        manu_date = datetime(2025, 1, 1)
        expiry = self.policy.calculate_expiry(manu_date)
        self.assertEqual(expiry, datetime(2025, 1, 31))

    def test_is_near_expiry_true(self):
        expiry = datetime.now() + timedelta(days=3)
        self.assertTrue(self.policy.is_near_expiry(expiry))

    def test_is_near_expiry_false(self):
        expiry = datetime.now() + timedelta(days=10)
        self.assertFalse(self.policy.is_near_expiry(expiry, days_threshold=7))

    def test_validate_storage_conditions_cold_chain_ok(self):
        self.assertTrue(self.policy.validate_storage_conditions(5.0))

    def test_validate_storage_conditions_cold_chain_fail(self):
        self.assertFalse(self.policy.validate_storage_conditions(10.0))

    def test_validate_storage_conditions_no_cold_chain(self):
        policy = ExpirationPolicy(10, requires_cold_chain=False)
        self.assertTrue(policy.validate_storage_conditions(25.0))