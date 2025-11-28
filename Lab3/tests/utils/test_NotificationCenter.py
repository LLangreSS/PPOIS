import unittest
from utils.NotificationCenter import NotificationCenter

class TestNotificationCenter(unittest.TestCase):

    def setUp(self):
        self.center = NotificationCenter()
        self.received_events = []

    def callback(self, event: str, payload: dict):
        self.received_events.append((event, payload))

    def test_subscribe_and_notify(self):
        self.center.subscribe("order_created", self.callback)
        payload = {"type": "order_created", "order_id": "O1"}
        self.center.notify("order", payload)

        self.assertEqual(len(self.received_events), 1)
        event, data = self.received_events[0]
        self.assertEqual(event, "order")
        self.assertEqual(data, payload)

    def test_notify_unrelated_event_type_no_call(self):
        self.center.subscribe("stock_alert", self.callback)
        payload = {"type": "order_created", "order_id": "O1"}
        self.center.notify("event", payload)
        self.assertEqual(len(self.received_events), 0)

    def test_multiple_subscribers(self):
        events1, events2 = [], []

        def cb1(e, p): events1.append(p)
        def cb2(e, p): events2.append(p)

        self.center.subscribe("alert", cb1)
        self.center.subscribe("alert", cb2)

        payload = {"type": "alert", "msg": "Low stock"}
        self.center.notify("sys", payload)

        self.assertEqual(len(events1), 1)
        self.assertEqual(len(events2), 1)
        self.assertEqual(events1[0], payload)
        self.assertEqual(events2[0], payload)

    def test_unsubscribe(self):
        self.center.subscribe("test", self.callback)
        self.center.unsubscribe("test", self.callback)
        self.center.notify("event", {"type": "test"})
        self.assertEqual(len(self.received_events), 0)

    def test_notify_without_subscribers(self):
        self.center.notify("unknown", {"type": "unknown"})
        self.assertEqual(len(self.received_events), 0)