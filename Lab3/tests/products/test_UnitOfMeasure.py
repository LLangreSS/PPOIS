import unittest
from products.UnitOfMeasure import UnitOfMeasure

class TestUnitOfMeasure(unittest.TestCase):

    def test_init(self):
        unit = UnitOfMeasure("kg", "kilogram", is_discrete=False)
        self.assertEqual(unit.symbol, "kg")
        self.assertEqual(unit.name, "kilogram")
        self.assertFalse(unit.is_discrete)

    def test_eq_true(self):
        u1 = UnitOfMeasure("kg", "kilogram")
        u2 = UnitOfMeasure("kg", "kilogram")
        self.assertEqual(u1, u2)

    def test_eq_false_symbol(self):
        u1 = UnitOfMeasure("kg", "kilogram")
        u2 = UnitOfMeasure("g", "kilogram")
        self.assertNotEqual(u1, u2)

    def test_eq_false_name(self):
        u1 = UnitOfMeasure("kg", "kilogram")
        u2 = UnitOfMeasure("kg", "gram")
        self.assertNotEqual(u1, u2)

    def test_convert_same_unit(self):
        unit = UnitOfMeasure("kg", "kilogram")
        self.assertEqual(unit.convert(5.0, unit), 5.0)

    def test_convert_kg_to_g(self):
        kg = UnitOfMeasure("kg", "kilogram")
        g = UnitOfMeasure("g", "gram")
        self.assertEqual(kg.convert(2.5, g), 2500.0)

    def test_convert_g_to_kg(self):
        g = UnitOfMeasure("g", "gram")
        kg = UnitOfMeasure("kg", "kilogram")
        self.assertEqual(g.convert(1500, kg), 1.5)

    def test_convert_unsupported_raises(self):
        kg = UnitOfMeasure("kg", "kilogram")
        l = UnitOfMeasure("l", "liter")
        with self.assertRaises(ValueError) as cm:
            kg.convert(1.0, l)
        self.assertIn("Conversion from kg to l is not supported", str(cm.exception))