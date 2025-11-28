import unittest
from warehouse.Location import Location

class TestLocation(unittest.TestCase):

    def test_init(self):
        loc = Location("A", "10", "B2", "ZONE1")
        self.assertEqual(loc.row, "A")
        self.assertEqual(loc.rack, "10")
        self.assertEqual(loc.shelf, "B2")
        self.assertEqual(loc.zone_id, "ZONE1")

    def test_to_string(self):
        loc = Location("A", "10", "B2", "ZONE1")
        self.assertEqual(loc.to_string(), "A-10-B2")

    def test_is_in_zone_true(self):
        loc = Location("A", "10", "B2", "ZONE1")
        self.assertTrue(loc.is_in_zone("ZONE1"))

    def test_is_in_zone_false(self):
        loc = Location("A", "10", "B2", "ZONE1")
        self.assertFalse(loc.is_in_zone("ZONE2"))

    def test_get_adjacent_locations(self):
        loc = Location("R1", "5", "S1", "Z1")
        adj = loc.get_adjacent_locations()
        self.assertEqual(len(adj), 2)
        self.assertEqual(adj[0].rack, "6")
        self.assertEqual(adj[1].rack, "4")
        self.assertEqual(adj[0].row, "R1")
        self.assertEqual(adj[0].shelf, "S1")
        self.assertEqual(adj[0].zone_id, "Z1")