import pytest
from people.Teacher import Teacher
from academia.Department import Department
from academia.Course import Course

def test_teacher_init():
    dept = Department("CS")
    t = Teacher(1, "Dr. Smith", "s@example.com", dept)
    assert t.name == "Dr. Smith"
    assert t in dept.teachers

def test_assign_course():
    dept = Department("CS")
    t = Teacher(1, "Dr. Smith", "s@example.com", dept)
    course = Course("Algo", 6)
    t.assign_course(course)
    assert course in t.courses
    assert course.teacher == t