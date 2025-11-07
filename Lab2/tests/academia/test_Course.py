import pytest
from academia.Course import Course
from people.Student import Student
from academia.Group import Group
from exceptions.CourseFullException import CourseFullException
from exceptions.DuplicateEnrollmentException import DuplicateEnrollmentException

def test_course_init():
    c = Course("Math", 5)
    assert c.name == "Math"
    assert c.credits == 5

def test_enroll_student():
    c = Course("Math", 5)
    g = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", g)
    c.enroll_student(s)
    assert s in c.students

def test_enroll_duplicate():
    c = Course("Math", 5)
    g = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", g)
    c.enroll_student(s)
    with pytest.raises(DuplicateEnrollmentException):
        c.enroll_student(s)

def test_course_full():
    c = Course("Math", 5)
    c.MAX_STUDENTS = 1
    g = Group("G1", 1)
    s1 = Student(1, "A", "a@example.com", g)
    s2 = Student(2, "B", "b@example.com", g)
    c.enroll_student(s1)
    with pytest.raises(CourseFullException):
        c.enroll_student(s2)