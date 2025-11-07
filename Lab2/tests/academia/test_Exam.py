import pytest
from academia.Exam import Exam, AcademicException
from academia.Course import Course
from people.Student import Student
from academia.Group import Group

def test_exam_init():
    course = Course("Math", 5)
    exam = Exam(course, "2025-12-01")
    assert exam.course == course
    assert exam.date == "2025-12-01"
    assert exam.attendees == []

def test_register_student():
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    course = Course("Math", 5)
    course.enroll_student(student)
    exam = Exam(course, "2025-12-01")
    exam.register_student(student)
    assert student in exam.attendees

def test_register_not_enrolled():
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    course = Course("Math", 5)
    exam = Exam(course, "2025-12-01")
    with pytest.raises(AcademicException):
        exam.register_student(student)