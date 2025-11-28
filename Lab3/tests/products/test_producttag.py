import unittest
from products.ProductTag import ProductTag

class TestProductTag(unittest.TestCase):
    def test_init(self):
        tag = ProductTag("fragile", "Requires careful handling")
        self.assertEqual(tag.name, "fragile")
        self.assertEqual(tag.description, "Requires careful handling")

    def test_is_handling_instruction_true(self):
        for name in ["fragile", "hazardous", "temperature", "humidity"]:
            with self.subTest(name=name):
                tag = ProductTag(name)
                self.assertTrue(tag.is_handling_instruction())

    def test_is_handling_instruction_false(self):
        tag = ProductTag("promo")
        self.assertFalse(tag.is_handling_instruction())

    def test_get_color_code_known(self):
        self.assertEqual(ProductTag("hazardous").get_color_code(), "red")
        self.assertEqual(ProductTag("fragile").get_color_code(), "orange")
        self.assertEqual(ProductTag("promo").get_color_code(), "green")
        self.assertEqual(ProductTag("new").get_color_code(), "blue")

    def test_get_color_code_unknown(self):
        self.assertEqual(ProductTag("sale").get_color_code(), "gray")