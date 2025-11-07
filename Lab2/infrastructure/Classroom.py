from __future__ import annotations

class Classroom:
    def __init__(self, room_number: str, capacity: int):
        self.room_number = room_number
        self.capacity = capacity
        self.building = None
        self.booked_slots: set[str] = set()

    def is_available(self, time_slot: str) -> bool:
        return time_slot not in self.booked_slots

    def book(self, time_slot: str) -> None:
        self.booked_slots.add(time_slot)
