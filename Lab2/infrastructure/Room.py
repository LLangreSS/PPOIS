from __future__ import annotations
from exceptions.RoomCapacityException import RoomCapacityException

class Room:
    def __init__(self, number: str, capacity: int):
        self.number = number
        self.capacity = capacity
        self.dormitory = None
        self.building = None
        self.occupants: list["Student"] = []

    def assign_student(self, student: "Student") -> None:
        if len(self.occupants) >= self.capacity:
            raise RoomCapacityException(f"Room {self.number} is at full capacity.")
        self.occupants.append(student)

    def is_occupied(self) -> bool:
        return len(self.occupants) > 0
