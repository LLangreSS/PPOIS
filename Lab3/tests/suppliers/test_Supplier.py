import unittest
from suppliers.Supplier import Supplier

class TestSupplier(unittest.TestCase):

    def test_init(self):
        s = Supplier("s1", "ABC Corp", "contact@abc.com", "+123456")
        self.assertEqual(s.id, "s1")
        self.assertEqual(s.name, "ABC Corp")
        self.assertEqual(s.contact_email, "contact@abc.com")
        self.assertEqual(s.phone, "+123456")
        self.assertTrue(s.is_active)

    def test_init_without_phone(self):
        s = Supplier("s2", "XYZ Ltd", "hello@xyz.com")
        self.assertEqual(s.phone, "")
        self.assertEqual(s.get_contact_summary(), "hello@xyz.com")

    def test_validate_contact_info_valid_emails(self):
        valid_emails = [
            "test@example.com",
            "user.name+tag@domain.co.uk",
            "123456789@gmail.com",
            "user@sub.example.org"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                s = Supplier("s1", "X", email)
                self.assertTrue(s.validate_contact_info(), f"Email {email} should be valid")

    def test_validate_contact_info_invalid_emails(self):
        invalid_emails = [
            "plainaddress",
            "@missingdomain.com",
            "missing@.com",
            "spaces @domain.com",
            "user@",
            "",
            "user@domain",
            "user@domain.",
            "user@.com",
            "user@domain..ю...com"
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                s = Supplier("s1", "X", email)
                self.assertFalse(s.validate_contact_info(), f"Email {email} should be invalid")

    def test_get_contact_summary_with_phone(self):
        s = Supplier("s1", "Test", "a@b.com", "+79991234567")
        self.assertEqual(s.get_contact_summary(), "a@b.com, +79991234567")

    def test_get_contact_summary_empty_phone(self):
        s = Supplier("s1", "Test", "a@b.com", "")
        self.assertEqual(s.get_contact_summary(), "a@b.com")

    def test_get_contact_summary_none_phone_not_possible(self):
        s = Supplier("s1", "Test", "a@b.com")
        self.assertEqual(s.phone, "")
        self.assertEqual(s.get_contact_summary(), "a@b.com")

    def test_validate_contact_info_edge_cases(self):
        s = Supplier("s1", "X", "a@b.co")
        self.assertTrue(s.validate_contact_info())

        s = Supplier("s1", "X", "user@domain.international")
        self.assertTrue(s.validate_contact_info())

        s = Supplier("s1", "X", "user@domain_name.com")
        self.assertFalse(s.validate_contact_info())