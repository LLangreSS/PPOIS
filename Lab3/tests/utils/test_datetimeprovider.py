import unittest
from unittest.mock import patch
from utils.DateTimeProvider import DateTimeProvider
from datetime import datetime, date

class TestDateTimeProvider(unittest.TestCase):

    def setUp(self):
        self.provider = DateTimeProvider()

    def test_now_returns_datetime(self):
        now = self.provider.now()
        self.assertIsInstance(now, datetime)

    def test_today_returns_datetime(self):
        today = self.provider.today()
        self.assertIsInstance(today, datetime)
        self.assertEqual(today.date(), date.today())

    @patch('utils.DateTimeProvider.datetime')
    def test_is_weekend_saturday(self, mock_datetime):
        mock_datetime.today.return_value = datetime(2025, 11, 29)
        self.assertTrue(self.provider.is_weekend())

    @patch('utils.DateTimeProvider.datetime')
    def test_is_weekend_sunday(self, mock_datetime):
        mock_datetime.today.return_value = datetime(2025, 11, 30)
        self.assertTrue(self.provider.is_weekend())

    @patch('utils.DateTimeProvider.datetime')
    def test_is_weekend_monday(self, mock_datetime):
        mock_datetime.today.return_value = datetime(2025, 12, 1)
        self.assertFalse(self.provider.is_weekend())

    @patch('utils.DateTimeProvider.datetime')
    def test_is_weekend_friday(self, mock_datetime):
        mock_datetime.today.return_value = datetime(2025, 11, 28)
        self.assertFalse(self.provider.is_weekend())