import unittest
from unittest.mock import Mock, patch
from deliveries.Delivery import Delivery
from datetime import datetime
from deliveries.DeliveryItem import DeliveryItem
from suppliers.Supplier import Supplier
from exceptions.DuplicateDeliveryError import DuplicateDeliveryError

class TestDelivery(unittest.TestCase):

    def setUp(self):
        self.mock_supplier = Mock(spec=Supplier)
        self.mock_item1 = Mock(spec=DeliveryItem)
        self.mock_item1.expected_quantity = 100
        self.mock_item1.received_quantity = 0
        self.mock_item2 = Mock(spec=DeliveryItem)
        self.mock_item2.expected_quantity = 50
        self.mock_item2.received_quantity = 0
        self.delivery = Delivery("DEL-001", self.mock_supplier, [self.mock_item1, self.mock_item2])

    def test_init_valid(self):
        self.assertEqual(self.delivery.id, "DEL-001")
        self.assertIs(self.delivery.supplier, self.mock_supplier)
        self.assertEqual(self.delivery.items, [self.mock_item1, self.mock_item2])
        self.assertIsNone(self.delivery.received_at)

    def test_init_empty_items(self):
        with self.assertRaises(ValueError) as cm:
            Delivery("D1", self.mock_supplier, [])
        self.assertEqual(str(cm.exception), "Delivery must contain at least one item")

    def test_is_complete_false(self):
        self.mock_item1.received_quantity = 90
        self.mock_item2.received_quantity = 50
        self.assertFalse(self.delivery.is_complete())

    def test_is_complete_true(self):
        self.mock_item1.received_quantity = 100
        self.mock_item2.received_quantity = 50
        self.assertTrue(self.delivery.is_complete())

    def test_get_total_expected_quantity(self):
        self.assertEqual(self.delivery.get_total_expected_quantity(), 150)

    def test_get_total_received_quantity(self):
        self.mock_item1.received_quantity = 80
        self.mock_item2.received_quantity = 30
        self.assertEqual(self.delivery.get_total_received_quantity(), 110)

    @patch('deliveries.Delivery.datetime')
    def test_is_overdue_true(self, mock_datetime):
        from datetime import datetime, timedelta
        future = datetime(2025, 1, 1)
        past = future - timedelta(days=1)
        mock_datetime.now.return_value = future
        self.delivery.expected_date = past
        self.delivery.received_at = None
        self.assertTrue(self.delivery.is_overdue())

    @patch('deliveries.Delivery.datetime')
    def test_is_overdue_false_received(self, mock_datetime):
        current_time = datetime(2025, 1, 2)
        expected_date = datetime(2025, 1, 1)
        received_time = datetime(2025, 1, 1)

        mock_datetime.now.return_value = current_time
        self.delivery.expected_date = expected_date
        self.delivery.received_at = received_time

        self.assertFalse(self.delivery.is_overdue())

    def test_receive_items_already_received(self):
        self.delivery.received_at = Mock()
        mock_report = Mock()
        with self.assertRaises(DuplicateDeliveryError):
            self.delivery.receive_items(mock_report)