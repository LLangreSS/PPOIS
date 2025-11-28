import unittest
from suppliers.SupplierCategory import SupplierCategory
from suppliers.Supplier import Supplier

class TestSupplierCategory(unittest.TestCase):
    def setUp(self):
        self.cat = SupplierCategory("Стратегические", "Ключевые партнёры")
        self.sup1 = Supplier("S1", "Alpha", "a@b.com")
        self.sup2 = Supplier("S2", "Beta", "b@c.com")

    def test_add_remove(self):
        self.cat.add_supplier(self.sup1)
        self.assertIn(self.sup1, self.cat.suppliers)
        self.cat.remove_supplier(self.sup1)
        self.assertNotIn(self.sup1, self.cat.suppliers)

    def test_get_ids(self):
        self.cat.add_supplier(self.sup1)
        self.cat.add_supplier(self.sup2)
        ids = self.cat.get_supplier_ids()
        self.assertEqual(ids, {"S1", "S2"})

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            SupplierCategory("", "Desc")