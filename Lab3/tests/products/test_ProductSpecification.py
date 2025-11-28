import unittest
from products.ProductSpecification import ProductSpecification
from unittest.mock import Mock

class TestProductSpecification(unittest.TestCase):
    def test_init(self):
        spec = ProductSpecification((0.5, 0.3, 0.2), 2.5, is_fragile=True, storage_notes="Keep dry")
        self.assertEqual(spec.dimensions, (0.5, 0.3, 0.2))
        self.assertEqual(spec.weight_kg, 2.5)
        self.assertTrue(spec.is_fragile)
        self.assertEqual(spec.storage_notes, "Keep dry")

    def test_volume(self):
        spec = ProductSpecification((2.0, 3.0, 4.0), 1.0)
        self.assertEqual(spec.volume(), 24.0)

    def test_requires_temperature_control_true(self):
        spec = ProductSpecification((1,1,1), 1.0, min_temperature=2.0)
        self.assertTrue(spec.requires_temperature_control())

        spec = ProductSpecification((1,1,1), 1.0, max_temperature=8.0)
        self.assertTrue(spec.requires_temperature_control())

        spec = ProductSpecification((1,1,1), 1.0, min_temperature=2.0, max_temperature=8.0)
        self.assertTrue(spec.requires_temperature_control())

    def test_requires_temperature_control_false(self):
        spec = ProductSpecification((1,1,1), 1.0)
        self.assertFalse(spec.requires_temperature_control())

    def test_get_temperature_range(self):
        spec = ProductSpecification((1,1,1), 1.0, min_temperature=2.0, max_temperature=8.0)
        self.assertEqual(spec.get_temperature_range(), (2.0, 8.0))

        spec = ProductSpecification((1,1,1), 1.0, min_temperature=2.0)
        self.assertEqual(spec.get_temperature_range(), (2.0, float('inf')))

        spec = ProductSpecification((1,1,1), 1.0, max_temperature=8.0)
        self.assertEqual(spec.get_temperature_range(), (-float('inf'), 8.0))

        spec = ProductSpecification((1,1,1), 1.0)
        self.assertEqual(spec.get_temperature_range(), (-float('inf'), float('inf')))

    def test_fits_in_true(self):
        spec = ProductSpecification((100.0, 80.0, 50.0), 200.0)
        pallet = Mock()
        pallet.max_dimensions = (120.0, 100.0, 150.0)
        pallet.remaining_capacity_kg = 300.0
        self.assertTrue(spec.fits_in(pallet))

    def test_fits_in_false_length(self):
        spec = ProductSpecification((130.0, 80.0, 50.0), 200.0)
        pallet = Mock()
        pallet.max_dimensions = (120.0, 100.0, 150.0)
        pallet.remaining_capacity_kg = 300.0
        self.assertFalse(spec.fits_in(pallet))

    def test_fits_in_false_width(self):
        spec = ProductSpecification((100.0, 110.0, 50.0), 200.0)
        pallet = Mock()
        pallet.max_dimensions = (120.0, 100.0, 150.0)
        pallet.remaining_capacity_kg = 300.0
        self.assertFalse(spec.fits_in(pallet))

    def test_fits_in_false_weight(self):
        spec = ProductSpecification((100.0, 80.0, 50.0), 200.0)
        pallet = Mock()
        pallet.max_dimensions = (120.0, 100.0, 150.0)
        pallet.remaining_capacity_kg = 150.0
        self.assertFalse(spec.fits_in(pallet))