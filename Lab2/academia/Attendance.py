from __future__ import annotations
from exceptions.AcademicException import AcademicException

class Attendance:
    def __init__(self, course: "Course", date: str):
        self.course = course
        self.date = date
        self.present_students: set["Student"] = set()

    def mark_present(self, student: "Student") -> None:
        if student not in getattr(self.course, 'students', []):
            raise AcademicException(f"{student.name} not in course.")
        self.present_students.add(student)
