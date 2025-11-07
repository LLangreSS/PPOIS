from __future__ import annotations
from exceptions.InvalidScheduleException import InvalidScheduleException

class Schedule:
    def __init__(self):
        self.entries: list[tuple["Course", "Classroom", str]] = []

    def add_entry(self, course: "Course", classroom: "Classroom", time_slot: str) -> None:
        if not classroom.is_available(time_slot):
            raise InvalidScheduleException("Classroom not available at this time.")
        self.entries.append((course, classroom, time_slot))
        classroom.book(time_slot)

    def has_conflict(self, teacher, time_slot: str) -> bool:
        for course, _, ts in self.entries:
            if ts == time_slot and getattr(course, 'teacher', None) == teacher:
                return True
        return False

    def get_student_schedule(self, student) -> list[tuple[str, str, str]]:
        return [
            (course.name, classroom.room_number, ts)
            for course, classroom, ts in self.entries
            if student in getattr(course, 'students', [])
        ]

    def export_as_text(self) -> str:
        return "\n".join(
            f"{ts}: {course.name} in {classroom.room_number}"
            for course, classroom, ts in self.entries
        )
