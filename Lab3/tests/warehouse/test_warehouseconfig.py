import unittest
from warehouse.WarehouseConfig import WarehouseConfig
from warehouse.StorageCondition import StorageCondition

class TestWarehouseConfig(unittest.TestCase):

    def test_init_defaults(self):
        config = WarehouseConfig()
        self.assertEqual(config.timezone, "UTC")
        self.assertIsInstance(config.default_condition, StorageCondition)
        self.assertFalse(config.auto_consolidate)
        self.assertEqual(config.max_pallet_weight, 1000.0)
        self.assertTrue(config.enable_expiry_tracking)

    def test_init_custom(self):
        cond = StorageCondition(temp_max=10)
        config = WarehouseConfig(
            timezone="Europe/Moscow",
            default_condition=cond,
            auto_consolidate=True,
            max_pallet_weight=1500.0,
            enable_expiry_tracking=False
        )
        self.assertEqual(config.timezone, "Europe/Moscow")
        self.assertIs(config.default_condition, cond)
        self.assertTrue(config.auto_consolidate)
        self.assertEqual(config.max_pallet_weight, 1500.0)
        self.assertFalse(config.enable_expiry_tracking)

    def test_validate_config_true(self):
        config = WarehouseConfig(max_pallet_weight=500.0, timezone="UTC")
        self.assertTrue(config.validate_config())

    def test_validate_config_false_weight(self):
        config = WarehouseConfig(max_pallet_weight=-10.0)
        self.assertFalse(config.validate_config())

    def test_validate_config_false_timezone(self):
        config = WarehouseConfig(timezone="")
        self.assertFalse(config.validate_config())

    def test_get_config_summary(self):
        config = WarehouseConfig(auto_consolidate=True, max_pallet_weight=2000.0)
        summary = config.get_config_summary()
        self.assertEqual(summary["timezone"], "UTC")
        self.assertTrue(summary["auto_consolidate"])
        self.assertEqual(summary["max_pallet_weight"], 2000.0)
        self.assertTrue(summary["enable_expiry_tracking"])