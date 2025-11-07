from __future__ import annotations

class Semester:
    def __init__(self, year: int, term: str):
        self.year = year
        self.term = term
        self.courses: list["Course"] = []

    def add_course(self, course: "Course") -> None:
        self.courses.append(course)

    def close_semester(self) -> None:
        for course in self.courses:
            course.students.clear()
