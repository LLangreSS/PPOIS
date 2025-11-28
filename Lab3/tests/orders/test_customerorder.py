import unittest
from unittest.mock import Mock
from orders.CustomerOrder import CustomerOrder
from orders.OrderLine import OrderLine
from products.Product import Product

class TestCustomerOrder(unittest.TestCase):

    def setUp(self):
        self.mock_product1 = Mock(spec=Product)
        self.mock_product1.id = "P1"
        self.mock_product2 = Mock(spec=Product)
        self.mock_product2.id = "P2"
        line1 = OrderLine(self.mock_product1, 5)
        line2 = OrderLine(self.mock_product2, 3)
        self.order = CustomerOrder("ORD-001", "CUST-100", [line1, line2])

    def test_init_valid(self):
        self.assertEqual(self.order.id, "ORD-001")
        self.assertEqual(self.order.customer_id, "CUST-100")
        self.assertEqual(len(self.order.lines), 2)
        self.assertEqual(self.order.status, "created")

    def test_init_empty_lines(self):
        with self.assertRaises(ValueError) as cm:
            CustomerOrder("O1", "C1", [])
        self.assertEqual(str(cm.exception), "Order must contain at least one line")

    def test_get_total_quantity(self):
        self.assertEqual(self.order.get_total_quantity(), 8)

    def test_get_fulfillment_status_not_fulfilled(self):
        self.assertEqual(self.order.get_fulfillment_status(), "not_fulfilled")

    def test_get_fulfillment_status_partially_fulfilled(self):
        self.order.lines[0].fulfill(2)
        self.assertEqual(self.order.get_fulfillment_status(), "partially_fulfilled")

    def test_get_fulfillment_status_fully_fulfilled(self):
        self.order.lines[0].fulfill(5)
        self.order.lines[1].fulfill(3)
        self.assertEqual(self.order.get_fulfillment_status(), "fully_fulfilled")

    def test_can_fulfill_true(self):
        inventory = {self.mock_product1: 10, self.mock_product2: 5}
        self.assertTrue(self.order.can_fulfill(inventory))

    def test_can_fulfill_false_missing_product(self):
        inventory = {self.mock_product1: 10}
        self.assertFalse(self.order.can_fulfill(inventory))

    def test_can_fulfill_false_insufficient_stock(self):
        inventory = {self.mock_product1: 5, self.mock_product2: 2}
        self.assertFalse(self.order.can_fulfill(inventory))

    def test_get_total_value(self):
        price_list = {"P1": 100.0, "P2": 200.0}
        expected = 5 * 100.0 + 3 * 200.0
        self.assertEqual(self.order.get_total_value(price_list), expected)

    def test_get_total_value_missing_price(self):
        price_list = {"P1": 100.0}
        expected = 5 * 100.0 + 3 * 0.0
        self.assertEqual(self.order.get_total_value(price_list), expected)