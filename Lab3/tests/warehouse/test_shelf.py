import unittest
from warehouse.Location import Location
from warehouse.Shelf import Shelf
from warehouse.Pallet import Pallet
from exceptions.SlotAllocationError import SlotAllocationError

class TestShelf(unittest.TestCase):
    def setUp(self):
        self.location = Location("A", "1", "S1", "ZONE1")
        self.pallet1 = Pallet("P1", self.location)
        self.pallet2 = Pallet("P2", self.location)

    def test_init(self):
        shelf = Shelf("S1", "ZONE1", max_pallets=3)
        self.assertEqual(shelf.id, "S1")
        self.assertEqual(shelf.zone_id, "ZONE1")
        self.assertEqual(shelf.max_pallets, 3)
        self.assertEqual(shelf.pallets, [])

    def test_has_space_true(self):
        shelf = Shelf("S1", "ZONE1", max_pallets=2)
        shelf.pallets = [self.pallet1]
        self.assertTrue(shelf.has_space())

    def test_has_space_false(self):
        shelf = Shelf("S1", "ZONE1", max_pallets=1)
        shelf.pallets = [self.pallet1]
        self.assertFalse(shelf.has_space())

    def test_add_pallet_success(self):
        shelf = Shelf("S1", "ZONE1", max_pallets=2)
        shelf.add_pallet(self.pallet1)
        self.assertIn(self.pallet1, shelf.pallets)

    def test_add_pallet_no_space(self):
        shelf = Shelf("S1", "ZONE1", max_pallets=1)
        shelf.add_pallet(self.pallet1)
        with self.assertRaises(SlotAllocationError) as cm:
            shelf.add_pallet(self.pallet2)
        self.assertIn("has no space for additional pallets", str(cm.exception))

    def test_remove_pallet_found(self):
        shelf = Shelf("S1", "ZONE1")
        shelf.add_pallet(self.pallet1)
        result = shelf.remove_pallet("P1")
        self.assertTrue(result)
        self.assertEqual(shelf.pallets, [])

    def test_remove_pallet_not_found(self):
        shelf = Shelf("S1", "ZONE1")
        shelf.add_pallet(self.pallet1)
        result = shelf.remove_pallet("P999")
        self.assertFalse(result)

    def test_get_pallet_locations(self):
        shelf = Shelf("S1", "ZONE1")
        pallet_a = Pallet("PA", Location("R1", "10", "S1", "Z1"))
        pallet_b = Pallet("PB", Location("R1", "11", "S1", "Z1"))
        shelf.add_pallet(pallet_a)
        shelf.add_pallet(pallet_b)
        locations = shelf.get_pallet_locations()
        self.assertIn("R1-10-S1", locations)
        self.assertIn("R1-11-S1", locations)
        self.assertEqual(len(locations), 2)