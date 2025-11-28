import unittest
from products.ProductCategory import ProductCategory

class TestProductCategory(unittest.TestCase):
    def test_init(self):
        cat = ProductCategory("1", "Electronics")
        self.assertEqual(cat.id, "1")
        self.assertEqual(cat.name, "Electronics")
        self.assertIsNone(cat.parent)
        self.assertEqual(cat.children, [])

    def test_full_path_root(self):
        cat = ProductCategory("1", "Electronics")
        self.assertEqual(cat.full_path(), "Electronics")

    def test_full_path_nested(self):
        root = ProductCategory("1", "Electronics")
        child = ProductCategory("2", "Phones")
        root.add_child(child)
        self.assertEqual(child.full_path(), "Electronics/Phones")

    def test_add_child_sets_parent_and_appends(self):
        root = ProductCategory("1", "Root")
        child = ProductCategory("2", "Child")
        root.add_child(child)
        self.assertIn(child, root.children)
        self.assertIs(child.parent, root)

    def test_is_ancestor_of_true(self):
        root = ProductCategory("1", "Root")
        level1 = ProductCategory("2", "L1")
        level2 = ProductCategory("3", "L2")
        root.add_child(level1)
        level1.add_child(level2)
        self.assertTrue(root._is_ancestor_of(level2))

    def test_is_ancestor_of_false(self):
        cat1 = ProductCategory("1", "Cat1")
        cat2 = ProductCategory("2", "Cat2")
        self.assertFalse(cat1._is_ancestor_of(cat2))

    def test_get_all_products_count(self):
        cat = ProductCategory("1", "Root")
        child = ProductCategory("2", "Child")
        cat.add_child(child)

        class MockProduct:
            def __init__(self, category):
                self.category = category

        p1 = MockProduct(cat)
        p2 = MockProduct(child)
        p3 = MockProduct(ProductCategory("3", "Other"))

        registry = [p1, p2, p3]
        self.assertEqual(cat.get_all_products_count(registry), 2)