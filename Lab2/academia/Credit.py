from __future__ import annotations
from exceptions.AcademicException import AcademicException

class Credit:
    def __init__(self, course: "Course"):
        self.course = course
        self.passed_students: set["Student"] = set()

    def register_student(self, student: "Student") -> None:
        if student not in getattr(self.course, 'students', []):
            raise AcademicException(f"{student.name} not enrolled in {self.course.name}.")
        self.passed_students.add(student)

    def award_credit(self, student: "Student") -> None:
        self.register_student(student)

    def is_passed(self, student: "Student") -> bool:
        return student in self.passed_students

    def get_pass_count(self) -> int:
        return len(self.passed_students)
