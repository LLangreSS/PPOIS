import unittest
from datetime import datetime
from products.Product import Product
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from suppliers.Supplier import Supplier
from products.UnitOfMeasure import UnitOfMeasure
from products.ProductTag import ProductTag
from orders.ReturnRequest import ReturnRequest


class TestReturnRequest(unittest.TestCase):

    def setUp(self):
        self.category = ProductCategory("CAT-001", "Electronics")
        self.spec = ProductSpecification((0.2, 0.1, 0.05), 0.3)
        self.barcode = Barcode("1234567890123")
        self.supplier = Supplier("SUP-01", "Tech Supplier", "contact@tech.com")
        self.unit = UnitOfMeasure("pcs", "pieces")

    def test_valid_creation(self):
        product = Product("PROD-01", "Phone", self.category, self.spec, self.barcode, self.supplier, self.unit)
        items = [product]
        reason = "Changed my mind"
        request = ReturnRequest("ORDER-1001", reason, items)

        self.assertEqual(request.order_id, "ORDER-1001")
        self.assertEqual(request.reason, "Changed my mind")
        self.assertEqual(request.items, items)
        self.assertEqual(request.status, "under_review")
        self.assertIsInstance(request.request_date, datetime)

    def test_empty_items_raises(self):
        with self.assertRaises(ValueError) as cm:
            ReturnRequest("ORDER-1001", "No reason", [])
        self.assertEqual(str(cm.exception), "Return request must include at least one product")

    def test_empty_reason_raises(self):
        product = Product("PROD-01", "Phone", self.category, self.spec, self.barcode, self.supplier, self.unit)
        with self.assertRaises(ValueError) as cm:
            ReturnRequest("ORDER-1001", "", [product])
        self.assertEqual(str(cm.exception), "Return reason cannot be empty")

        with self.assertRaises(ValueError) as cm:
            ReturnRequest("ORDER-1001", "   ", [product])
        self.assertEqual(str(cm.exception), "Return reason cannot be empty")

    def test_validate_allows_normal_product(self):
        product = Product("PROD-01", "Phone", self.category, self.spec, self.barcode, self.supplier, self.unit)
        request = ReturnRequest("ORDER-1001", "No need", [product])
        self.assertTrue(request.validate())

    def test_validate_blocks_hazardous_product(self):
        hazardous_tag = ProductTag("hazardous")
        product = Product(
            "PROD-02", "Battery", self.category, self.spec, self.barcode, self.supplier, self.unit,
            tags=[hazardous_tag]
        )
        request = ReturnRequest("ORDER-1001", "Defective", [product])
        self.assertFalse(request.validate())

    def test_approve_updates_status_correctly(self):
        normal_product = Product("PROD-01", "Phone", self.category, self.spec, self.barcode, self.supplier, self.unit)
        request1 = ReturnRequest("ORDER-1001", "No need", [normal_product])
        request1.approve()
        self.assertEqual(request1.status, "approved")

        hazardous_tag = ProductTag("hazardous")
        hazardous_product = Product(
            "PROD-02", "Battery", self.category, self.spec, self.barcode, self.supplier, self.unit,
            tags=[hazardous_tag]
        )
        request2 = ReturnRequest("ORDER-1001", "No need", [hazardous_product])
        request2.approve()
        self.assertEqual(request2.status, "rejected")

    def test_get_return_summary_returns_correct_dict(self):
        product = Product("PROD-01", "Phone", self.category, self.spec, self.barcode, self.supplier, self.unit)
        request = ReturnRequest("ORDER-1001", "Changed mind", [product])

        summary = request.get_return_summary()

        expected_keys = {"order_id", "reason", "item_count", "status", "request_date"}
        self.assertEqual(set(summary.keys()), expected_keys)
        self.assertEqual(summary["order_id"], "ORDER-1001")
        self.assertEqual(summary["reason"], "Changed mind")
        self.assertEqual(summary["item_count"], 1)
        self.assertEqual(summary["status"], "under_review")
        self.assertIsInstance(summary["request_date"], datetime)


if __name__ == "__main__":
    unittest.main()