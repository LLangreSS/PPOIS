from __future__ import annotations
from exceptions.AcademicException import AcademicException

class Exam:
    def __init__(self, course: "Course", date: str):
        self.course = course
        self.date = date
        self.attendees: list["Student"] = []

    def register_student(self, student: "Student") -> None:
        if student not in getattr(self.course, 'students', []):
            raise AcademicException(f"{student.name} not enrolled in {self.course.name}.")
        if student not in self.attendees:
            self.attendees.append(student)

    def grade_all(self, default_grade: float = 60) -> None:
        teacher = getattr(self.course, 'teacher', None)
        if teacher:
            for student in self.attendees:
                teacher.grade_student(student, self.course, default_grade)
