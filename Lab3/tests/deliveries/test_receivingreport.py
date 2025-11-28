import unittest
from unittest.mock import Mock
from deliveries.ReceivingReport import ReceivingReport
from staff.Employee import Employee

class TestReceivingReport(unittest.TestCase):

    def setUp(self):
        self.mock_product1 = Mock()
        self.mock_product1.id = "P1"
        self.mock_product2 = Mock()
        self.mock_product2.id = "P2"
        self.items = [(self.mock_product1, 50), (self.mock_product2, 30)]
        self.mock_inspector = Mock(spec=Employee)
        self.mock_inspector.name = "Inspector"
        self.report = ReceivingReport("DEL-001", self.items, self.mock_inspector)

    def test_init_valid(self):
        self.assertEqual(self.report.delivery_id, "DEL-001")
        self.assertEqual(self.report.items, self.items)
        self.assertIs(self.report.inspector, self.mock_inspector)
        self.assertIsNotNone(self.report.report_date)

    def test_init_invalid_quantity_zero(self):
        with self.assertRaises(ValueError) as cm:
            ReceivingReport("D1", [(self.mock_product1, 0)], self.mock_inspector)
        self.assertEqual(str(cm.exception), "Received quantities must be positive")

    def test_get_total_received_quantity(self):
        self.assertEqual(self.report.get_total_received_quantity(), 80)

    def test_validate_against_delivery_subset(self):
        mock_delivery = Mock()
        mock_delivery.items = [
            Mock(product=Mock(id="P1")),
            Mock(product=Mock(id="P2")),
            Mock(product=Mock(id="P3"))
        ]
        self.assertTrue(self.report.validate_against(mock_delivery))

    def test_validate_against_delivery_extra_product(self):
        mock_delivery = Mock()
        mock_delivery.items = [Mock(product=Mock(id="P1"))]  # нет P2
        self.assertFalse(self.report.validate_against(mock_delivery))

    def test_get_discrepancies(self):
        mock_delivery = Mock()
        mock_delivery.items = [
            Mock(product=Mock(id="P1"), expected_quantity=60),
            Mock(product=Mock(id="P2"), expected_quantity=30)
        ]
        discrepancies = self.report.get_discrepancies(mock_delivery)
        self.assertEqual(len(discrepancies), 1)
        self.assertEqual(discrepancies[0]['product_id'], "P1")
        self.assertEqual(discrepancies[0]['expected'], 60)
        self.assertEqual(discrepancies[0]['received'], 50)
        self.assertEqual(discrepancies[0]['difference'], -10)