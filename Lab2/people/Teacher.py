from __future__ import annotations
from people.Person import Person
from academia.Department import Department
from academia.Course import Course
from academia.Exam import Exam
from academia.Grade import Grade
from academia.Attendance import Attendance
from academia.Research import Research

class Teacher(Person):
    def __init__(self, person_id: int, name: str, email: str, department: Department):
        super().__init__(person_id, name, email)
        self.department = department
        self.courses: list[Course] = []
        department.assign_teacher(self)

    def assign_course(self, course: Course) -> None:
        if course not in self.courses:
            self.courses.append(course)
            course.teacher = self

    def create_exam(self, course: Course, date: str) -> Exam:
        return Exam(course, date)

    def grade_student(self, student, course, grade_value: float) -> None:
        Grade(student, course, grade_value)

    def submit_attendance(self, course: Course, date: str, present_students) -> None:
        att = Attendance(course, date)
        for student in present_students:
            att.mark_present(student)

    def publish_research(self, title: str) -> Research:
        return Research(title, self)
