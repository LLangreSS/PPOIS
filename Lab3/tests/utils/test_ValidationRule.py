import unittest
from unittest.mock import Mock
from utils.ValidationRule import ValidationRule
from products.Product import Product

class TestValidationRule(unittest.TestCase):

    def setUp(self):
        self.mock_product = Mock(spec=Product)

    def test_apply_true(self):
        rule = ValidationRule("test", lambda p: True)
        self.assertTrue(rule.apply(self.mock_product))

    def test_apply_false(self):
        rule = ValidationRule("test", lambda p: False)
        self.assertFalse(rule.apply(self.mock_product))

    def test_str_representation(self):
        rule = ValidationRule("barcode_valid", lambda p: True)
        self.assertEqual(str(rule), "ValidationRule: barcode_valid")

    def test_and_rule_both_true(self):
        rule1 = ValidationRule("A", lambda p: True)
        rule2 = ValidationRule("B", lambda p: True)
        combined = rule1.and_rule(rule2)
        self.assertTrue(combined.apply(self.mock_product))

    def test_and_rule_first_false(self):
        rule1 = ValidationRule("A", lambda p: False)
        rule2 = ValidationRule("B", lambda p: True)
        combined = rule1.and_rule(rule2)
        self.assertFalse(combined.apply(self.mock_product))

    def test_and_rule_second_false(self):
        rule1 = ValidationRule("A", lambda p: True)
        rule2 = ValidationRule("B", lambda p: False)
        combined = rule1.and_rule(rule2)
        self.assertFalse(combined.apply(self.mock_product))

    def test_and_rule_name(self):
        rule1 = ValidationRule("weight", lambda p: True)
        rule2 = ValidationRule("fragile", lambda p: True)
        combined = rule1.and_rule(rule2)
        self.assertEqual(str(combined), "ValidationRule: weight_AND_fragile")