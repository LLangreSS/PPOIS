import unittest
from unittest.mock import Mock
from deliveries.DeliveryItem import DeliveryItem

class TestDeliveryItem(unittest.TestCase):

    def setUp(self):
        self.mock_product = Mock()
        self.mock_product.id = "P1"
        self.item = DeliveryItem(self.mock_product, 100)

    def test_init_valid(self):
        self.assertIs(self.item.product, self.mock_product)
        self.assertEqual(self.item.expected_quantity, 100)
        self.assertEqual(self.item.received_quantity, 0)
        self.assertEqual(self.item.batch_id, "")

    def test_init_invalid_quantity_zero(self):
        with self.assertRaises(ValueError) as cm:
            DeliveryItem(self.mock_product, 0)
        self.assertEqual(str(cm.exception), "Expected quantity must be positive")

    def test_init_invalid_quantity_negative(self):
        with self.assertRaises(ValueError) as cm:
            DeliveryItem(self.mock_product, -5)
        self.assertEqual(str(cm.exception), "Expected quantity must be positive")

    def test_get_receipt_status_not_received(self):
        self.assertEqual(self.item.get_receipt_status(), "Not received")

    def test_get_receipt_status_partially_received(self):
        self.item.received_quantity = 70
        self.assertEqual(self.item.get_receipt_status(), "Partially received")

    def test_get_receipt_status_fully_received(self):
        self.item.received_quantity = 100
        self.assertEqual(self.item.get_receipt_status(), "Fully received")

    def test_get_receipt_status_exceeded(self):
        self.item.received_quantity = 110
        self.assertEqual(self.item.get_receipt_status(), "Over-delivered")

    def test_create_batch_before_receipt(self):
        with self.assertRaises(ValueError) as cm:
            self.item.create_batch()
        self.assertEqual(str(cm.exception), "Cannot create batch: no items received")

    def test_create_batch_success(self):
        self.item.received_quantity = 50
        batch = self.item.create_batch()
        self.assertEqual(batch.quantity, 50)
        self.assertIs(batch.product, self.mock_product)
        self.assertEqual(self.item.batch_id, batch.id)
        self.assertIsNotNone(batch.manufacture_date)