from unittest import TestCase

from examine_stock_data import (
    build_notification_message,
    examine_stock_data,
)
from tests.test_data.stock_data import new_stock_data, recent_stock_data

# TODO: look at mocking pg connection & add test for get_recent_mens_medium_synchilla_stock_data


class TestBuildNotificationMessage(TestCase):
    def setUp(self):
        self.new_stock_data = new_stock_data

    def test_build_notification_message(self):
        notification_message = build_notification_message(self.new_stock_data)
        self.assertTrue(notification_message.startswith("New stock data found:"))
        self.assertIs(str, type(notification_message))


class TestExamineStockData(TestCase):
    def setUp(self):
        self.recent_stock_data = recent_stock_data
        self.new_stock_data = new_stock_data

    def test_examine_stock_data(self):
        new_stock_data = examine_stock_data(self.recent_stock_data)
        self.assertEqual(new_stock_data, self.new_stock_data)
