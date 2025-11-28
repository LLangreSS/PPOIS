import unittest
from suppliers.SupplierContract import SupplierContract
from suppliers.Supplier import Supplier
from datetime import datetime, timedelta

class TestSupplierContract(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S-01", "Tech Ltd", "tech@ltd.com")
        self.now = datetime(2025, 11, 27)
        self.contract = SupplierContract(
            id="CT-001",
            supplier=self.supplier,
            start_date=self.now - timedelta(days=30),
            duration_days=60,
            auto_renew=True
        )

    def test_is_active(self):
        self.assertTrue(self.contract.is_active(self.now))
        future = self.now + timedelta(days=100)
        self.assertFalse(self.contract.is_active(future))

    def test_should_renew(self):

        near_end = self.contract.end_date - timedelta(days=5)
        self.assertTrue(self.contract.should_renew(near_end))

        too_early = self.contract.end_date - timedelta(days=10)
        self.assertFalse(self.contract.should_renew(too_early))

        after = self.contract.end_date + timedelta(days=1)
        self.assertFalse(self.contract.should_renew(after))

    def test_invalid_duration_raises(self):
        with self.assertRaises(ValueError):
            SupplierContract("CT", self.supplier, self.now, 0)