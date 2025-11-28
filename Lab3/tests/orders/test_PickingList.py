import unittest
from unittest.mock import Mock
from orders.PickingList import PickingList
from warehouse.InventorySlot import InventorySlot
from products.Product import Product
from products.ProductSpecification import ProductSpecification
from warehouse.Batch import Batch

class TestPickingList(unittest.TestCase):

    def setUp(self):
        self.mock_product = Mock(spec=Product)
        self.mock_product.spec = Mock(spec=ProductSpecification)
        self.mock_product.spec.is_fragile = False
        self.mock_product.is_hazardous.return_value = False
        self.mock_batch = Mock(spec=Batch)
        self.mock_batch.product = self.mock_product
        self.mock_slot = Mock(spec=InventorySlot)
        self.mock_slot.batch = self.mock_batch
        self.mock_slot.quantity = 5
        self.picking_list = PickingList("ORD-001", [self.mock_slot])

    def test_init_valid(self):
        self.assertEqual(self.picking_list.order_id, "ORD-001")
        self.assertEqual(self.picking_list.slots, [self.mock_slot])
        self.assertEqual(self.picking_list.status, "created")

    def test_get_total_items(self):
        self.assertEqual(self.picking_list.get_total_items(), 5)

    def test_get_picking_priority_normal(self):
        self.assertEqual(self.picking_list.get_picking_priority(), "low")

    def test_get_picking_priority_fragile(self):
        self.mock_product.spec.is_fragile = True
        self.assertEqual(self.picking_list.get_picking_priority(), "medium")

    def test_get_picking_priority_hazardous(self):
        self.mock_product.is_hazardous.return_value = True
        self.assertEqual(self.picking_list.get_picking_priority(), "high")

    def test_reserve_slots(self):
        # Mock метода reserve
        self.mock_slot.reserve.return_value = Mock()
        reserved = self.picking_list.reserve_slots()
        self.mock_slot.reserve.assert_called_once_with(5, reserved_for="ORD-001")
        self.assertEqual(len(reserved), 1)
        self.assertEqual(self.picking_list.status, "reserved")

    def test_reserve_slots_empty_slot_skipped(self):
        empty_slot = Mock(spec=InventorySlot)
        empty_slot.quantity = 0
        pl = PickingList("ORD-2", [empty_slot])
        empty_slot.reserve.assert_not_called()
        reserved = pl.reserve_slots()
        self.assertEqual(reserved, [])
        self.assertEqual(pl.status, "reserved")