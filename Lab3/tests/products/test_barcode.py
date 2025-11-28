import unittest
from products.Barcode import Barcode

class TestBarcode(unittest.TestCase):
    def test_validate_valid_ean13(self):
        b = Barcode("1234567890123")
        self.assertTrue(b.validate())

    def test_validate_invalid_length(self):
        b = Barcode("123")
        self.assertFalse(b.validate())

    def test_validate_non_digits(self):
        b = Barcode("123456789012a")
        self.assertFalse(b.validate())

    def test_get_barcode_type_ean13(self):
        b = Barcode("1234567890123")
        self.assertEqual(b.get_barcode_type(), "EAN-13")

    def test_get_barcode_type_ean8(self):
        b = Barcode("12345678")
        self.assertEqual(b.get_barcode_type(), "EAN-8")

    def test_get_barcode_type_upc_a(self):
        b = Barcode("123456789012")
        self.assertEqual(b.get_barcode_type(), "UPC-A")

    def test_get_barcode_type_unknown(self):
        b = Barcode("12345")
        self.assertEqual(b.get_barcode_type(), "Unknown format")

    def test_generate_image_data(self):
        b = Barcode("1234567890123")
        self.assertEqual(b.generate_image_data(), "|| 1234567890123 ||")