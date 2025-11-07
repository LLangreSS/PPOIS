import pytest
from academia.Attendance import Attendance, AcademicException
from academia.Course import Course
from people.Student import Student
from academia.Group import Group

def test_attendance_init():
    course = Course("Math", 5)
    att = Attendance(course, "2025-11-07")
    assert att.course == course
    assert att.date == "2025-11-07"

def test_mark_present():
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    course = Course("Math", 5)
    course.enroll_student(student)
    att = Attendance(course, "2025-11-07")
    att.mark_present(student)
    assert student in att.present_students

def test_mark_not_enrolled():
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    course = Course("Math", 5)
    att = Attendance(course, "2025-11-07")
    with pytest.raises(AcademicException):
        att.mark_present(student)