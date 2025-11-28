import unittest
from unittest.mock import Mock
from orders.PackingSlip import PackingSlip
from products.Product import Product


class TestPackingSlip(unittest.TestCase):

    def setUp(self):
        mock_unit1 = Mock()
        mock_unit1.symbol = "шт"

        mock_unit2 = Mock()
        mock_unit2.symbol = "кг"

        self.mock_product1 = Mock(spec=Product)
        self.mock_product1.id = "P1"
        self.mock_product1.name = "Товар 1"
        self.mock_product1.unit = mock_unit1

        self.mock_product2 = Mock(spec=Product)
        self.mock_product2.id = "P2"
        self.mock_product2.name = "Товар 2"
        self.mock_product2.unit = mock_unit2

        self.items = [(self.mock_product1, 5), (self.mock_product2, 3)]
        self.slip = PackingSlip("SHIP-001", self.items)

    def test_init_valid(self):
        self.assertEqual(self.slip.shipment_id, "SHIP-001")
        self.assertEqual(self.slip.items, self.items)

    def test_init_empty_items(self):
        with self.assertRaises(ValueError) as cm:
            PackingSlip("S1", [])
        self.assertEqual(str(cm.exception), "Packing slip must contain items")

    def test_get_total_quantity(self):
        self.assertEqual(self.slip.get_total_quantity(), 8)

    def test_to_pdf(self):
        pdf_bytes = self.slip.to_pdf()
        content = pdf_bytes.decode("utf-8")
        self.assertIn("Товар 1: 5 шт", content)
        self.assertIn("Товар 2: 3 кг", content)
        self.assertIn("Упаковочный лист для SHIP-001", content)

    def test_validate_against_order_true(self):
        order_lines = [
            Mock(product=self.mock_product1, quantity=5),
            Mock(product=self.mock_product2, quantity=3)
        ]
        self.assertTrue(self.slip.validate_against_order(order_lines))

    def test_validate_against_order_false_quantity_mismatch(self):
        order_lines = [
            Mock(product=self.mock_product1, quantity=5),
            Mock(product=self.mock_product2, quantity=4)
        ]
        self.assertFalse(self.slip.validate_against_order(order_lines))

    def test_validate_against_order_false_product_mismatch(self):
        mock_unit3 = Mock()
        mock_unit3.symbol = "л"

        mock_product3 = Mock(spec=Product)
        mock_product3.id = "P3"
        mock_product3.name = "Товар 3"
        mock_product3.unit = mock_unit3

        order_lines = [
            Mock(product=self.mock_product1, quantity=5),
            Mock(product=mock_product3, quantity=3)
        ]
        self.assertFalse(self.slip.validate_against_order(order_lines))