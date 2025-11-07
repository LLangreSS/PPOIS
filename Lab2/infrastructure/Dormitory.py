from __future__ import annotations

class Dormitory:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.rooms: list["Room"] = []

    def add_room(self, room: "Room") -> None:
        self.rooms.append(room)
        room.dormitory = self

    def assign_room_to_student(self, student, room_number: str) -> None:
        for room in self.rooms:
            if getattr(room, 'number', None) == room_number:
                room.assign_student(student)
                return
