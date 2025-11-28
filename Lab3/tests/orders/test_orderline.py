import unittest
from unittest.mock import Mock
from orders.OrderLine import OrderLine
from products.Product import Product

class TestOrderLine(unittest.TestCase):

    def setUp(self):
        self.mock_product = Mock(spec=Product)
        self.mock_product.id = "P1"
        self.line = OrderLine(self.mock_product, 10)

    def test_init_valid(self):
        self.assertIs(self.line.product, self.mock_product)
        self.assertEqual(self.line.quantity, 10)
        self.assertEqual(self.line.fulfilled, 0)

    def test_init_invalid_quantity_zero(self):
        with self.assertRaises(ValueError) as cm:
            OrderLine(self.mock_product, 0)
        self.assertEqual(str(cm.exception), "Order quantity must be positive")

    def test_init_invalid_quantity_negative(self):
        with self.assertRaises(ValueError) as cm:
            OrderLine(self.mock_product, -3)
        self.assertEqual(str(cm.exception), "Order quantity must be positive")

    def test_is_fulfilled_false_initially(self):
        self.assertFalse(self.line.is_fulfilled())

    def test_is_fulfilled_true_when_equal(self):
        self.line.fulfill(10)
        self.assertTrue(self.line.is_fulfilled())

    def test_is_fulfilled_true_when_exceeded(self):
        self.line.fulfill(10)
        # fulfilled == quantity → True
        self.assertTrue(self.line.is_fulfilled())

    def test_fulfill_success(self):
        self.line.fulfill(4)
        self.assertEqual(self.line.fulfilled, 4)

    def test_fulfill_zero(self):
        with self.assertRaises(ValueError) as cm:
            self.line.fulfill(0)
        self.assertEqual(str(cm.exception), "Fulfill amount must be positive")

    def test_fulfill_negative(self):
        with self.assertRaises(ValueError) as cm:
            self.line.fulfill(-2)
        self.assertEqual(str(cm.exception), "Fulfill amount must be positive")

    def test_fulfill_exceeds_quantity(self):
        with self.assertRaises(ValueError) as cm:
            self.line.fulfill(11)
        self.assertEqual(
            str(cm.exception),
            "Fulfill amount exceeds order line quantity"
        )

    def test_get_remaining_quantity_initial(self):
        self.assertEqual(self.line.get_remaining_quantity(), 10)

    def test_get_remaining_quantity_partial(self):
        self.line.fulfill(3)
        self.assertEqual(self.line.get_remaining_quantity(), 7)

    def test_get_fulfillment_percentage_initial(self):
        self.assertEqual(self.line.get_fulfillment_percentage(), 0.0)

    def test_get_fulfillment_percentage_partial(self):
        self.line.fulfill(5)
        self.assertEqual(self.line.get_fulfillment_percentage(), 50.0)

    def test_get_fulfillment_percentage_complete(self):
        self.line.fulfill(10)
        self.assertEqual(self.line.get_fulfillment_percentage(), 100.0)