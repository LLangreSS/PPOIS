import unittest
from utils.IdGenerator import IdGenerator

class TestIdGenerator(unittest.TestCase):

    def setUp(self):
        IdGenerator._counters.clear()

    def test_generate_increments_correctly(self):
        gen = IdGenerator("TEST")
        self.assertEqual(gen.generate(), "TEST-0001")
        self.assertEqual(gen.generate(), "TEST-0002")
        self.assertEqual(gen.generate(), "TEST-0003")

    def test_different_prefixes_independent(self):
        gen1 = IdGenerator("A")
        gen2 = IdGenerator("B")
        self.assertEqual(gen1.generate(), "A-0001")
        self.assertEqual(gen2.generate(), "B-0001")
        self.assertEqual(gen1.generate(), "A-0002")

    def test_reset_counter_specific_prefix(self):
        gen = IdGenerator("TASK")
        gen.generate()
        IdGenerator.reset_counter("TASK")
        self.assertEqual(gen.generate(), "TASK-0001")

    def test_prefix_case_sensitive(self):
        gen1 = IdGenerator("Order")
        gen2 = IdGenerator("order")
        self.assertEqual(gen1.generate(), "Order-0001")
        self.assertEqual(gen2.generate(), "order-0001")