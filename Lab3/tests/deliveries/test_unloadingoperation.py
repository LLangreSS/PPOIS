import unittest
from unittest.mock import Mock, patch
from deliveries.UnloadingOperation import UnloadingOperation
from warehouse.Warehouse import Warehouse

class TestUnloadingOperation(unittest.TestCase):

    def setUp(self):
        self.mock_delivery = Mock()
        self.mock_delivery.received_at = Mock()  # уже получена
        self.mock_operator = Mock()
        self.mock_warehouse = Mock(spec=Warehouse)
        self.operation = UnloadingOperation(self.mock_delivery, self.mock_operator, self.mock_warehouse)

    def test_init_delivery_not_received(self):
        with self.assertRaises(ValueError) as cm:
            UnloadingOperation(Mock(received_at=None), self.mock_operator, self.mock_warehouse)
        self.assertEqual(str(cm.exception), "Delivery must be received before unloading")

    def test_init_valid(self):
        self.assertIs(self.operation.delivery, self.mock_delivery)
        self.assertIs(self.operation.operator, self.mock_operator)
        self.assertIs(self.operation.warehouse, self.mock_warehouse)
        self.assertEqual(self.operation.status, "in_progress")
        self.assertIsNotNone(self.operation.timestamp)

    @patch('deliveries.UnloadingOperation.datetime')
    def test_process_success(self, mock_datetime):
        mock_item = Mock()
        mock_item.received_quantity = 10
        mock_item.product = Mock()
        self.mock_delivery.items = [mock_item]
        mock_slot = Mock()
        self.mock_warehouse.allocate_slot.return_value = mock_slot

        slots = self.operation.process()

        self.assertEqual(slots, [mock_slot])
        self.assertEqual(self.operation.status, "completed")
        self.mock_warehouse.allocate_slot.assert_called_once_with(
            product=mock_item.product,
            quantity=10
        )

    def test_process_skip_zero_quantity(self):
        mock_item = Mock()
        mock_item.received_quantity = 0
        self.mock_delivery.items = [mock_item]

        slots = self.operation.process()

        self.assertEqual(slots, [])
        self.mock_warehouse.allocate_slot.assert_not_called()

