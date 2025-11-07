from __future__ import annotations

class Building:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.classrooms: list["Classroom"] = []
        self.rooms: list["Room"] = []

    def add_classroom(self, classroom: "Classroom") -> None:
        self.classrooms.append(classroom)
        classroom.building = self

    def add_room(self, room: "Room") -> None:
        self.rooms.append(room)
        room.building = self

    def get_total_rooms(self) -> int:
        return len(self.classrooms) + len(self.rooms)
