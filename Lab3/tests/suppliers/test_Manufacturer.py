import unittest
from suppliers.Manufacturer import Manufacturer

class TestManufacturer(unittest.TestCase):
    def test_init(self):
        m = Manufacturer("m1", "Pharma Inc", "Germany", 7.5)
        self.assertEqual(m.id, "m1")
        self.assertEqual(m.name, "Pharma Inc")
        self.assertEqual(m.country, "Germany")
        self.assertEqual(m.quality_rating, 7.5)

    def test_is_european_true(self):
        eu_countries = ["Germany", "France", "Italy", "Spain", "Poland"]
        for country in eu_countries:
            with self.subTest(country=country):
                m = Manufacturer("m1", "X", country)
                self.assertTrue(m.is_european())

    def test_is_european_false(self):
        non_eu = ["China", "USA", "Japan", "Brazil"]
        for country in non_eu:
            with self.subTest(country=country):
                m = Manufacturer("m1", "X", country)
                self.assertFalse(m.is_european())

    def test_update_quality_rating_valid_range(self):
        m = Manufacturer("m1", "X", "USA", 5.0)
        test_ratings = [0.0, 1.0, 5.0, 9.9, 10.0]
        for rating in test_ratings:
            with self.subTest(rating=rating):
                m.update_quality_rating(rating)
                self.assertEqual(m.quality_rating, rating)

    def test_update_quality_rating_invalid_low(self):
        m = Manufacturer("m1", "X", "USA", 5.0)
        with self.assertRaises(ValueError) as cm:
            m.update_quality_rating(-0.1)
        self.assertEqual(str(cm.exception), "Rating must be between 0 and 10")

    def test_update_quality_rating_invalid_high(self):
        m = Manufacturer("m1", "X", "USA", 5.0)
        with self.assertRaises(ValueError) as cm:
            m.update_quality_rating(10.1)
        self.assertEqual(str(cm.exception), "Rating must be between 0 and 10")

    def test_update_quality_rating_edge_zero(self):
        m = Manufacturer("m1", "X", "USA", 5.0)
        m.update_quality_rating(0.0)
        self.assertEqual(m.quality_rating, 0.0)

    def test_update_quality_rating_edge_ten(self):
        m = Manufacturer("m1", "X", "USA", 5.0)
        m.update_quality_rating(10.0)
        self.assertEqual(m.quality_rating, 10.0)