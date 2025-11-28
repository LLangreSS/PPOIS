import unittest
from unittest.mock import Mock, patch
from orders.Shipment import Shipment
from products.Product import Product
from products.ProductSpecification import ProductSpecification
from warehouse.Batch import Batch

class TestShipment(unittest.TestCase):

    def setUp(self):
        self.mock_product = Mock(spec=Product)
        self.mock_product.spec = Mock(spec=ProductSpecification)
        self.mock_product.spec.weight_kg = 2.0
        self.mock_batch = Mock(spec=Batch)
        self.mock_batch.product = self.mock_product
        self.mock_batch.quantity = 10
        self.shipment = Shipment("ORD-001", [self.mock_batch], "DHL", "Москва")

    def test_init_valid(self):
        self.assertEqual(self.shipment.order_id, "ORD-001")
        self.assertEqual(self.shipment.items, [self.mock_batch])
        self.assertEqual(self.shipment.carrier, "DHL")
        self.assertEqual(self.shipment.destination, "Москва")
        self.assertEqual(self.shipment.status, "preparing")

    def test_init_empty_items(self):
        with self.assertRaises(ValueError) as cm:
            Shipment("O1", [], "DHL", "Москва")
        self.assertEqual(str(cm.exception), "Shipment must contain at least one batch")

    def test_get_total_weight(self):
        self.assertEqual(self.shipment.get_total_weight(), 20.0)  # 10 * 2.0

    def test_generate_packing_slip(self):
        slip = self.shipment.generate_packing_slip()
        self.assertEqual(slip.shipment_id, "ORD-001")
        self.assertEqual(len(slip.items), 1)
        self.assertEqual(slip.items[0][0], self.mock_product)
        self.assertEqual(slip.items[0][1], 10)

    @patch('orders.Shipment.IdGenerator')
    def test_create_label(self, mock_id_gen):
        mock_id_gen.return_value.generate.return_value = "TRACK-0001"
        label = self.shipment.create_label()
        self.assertEqual(label.tracking_number, "TRACK-0001")
        self.assertEqual(label.destination, "Москва")
        self.assertEqual(label.weight_kg, 20.0)

    def test_mark_as_shipped(self):
        self.shipment.mark_as_shipped()
        self.assertEqual(self.shipment.status, "shipped")