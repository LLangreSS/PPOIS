import pytest
from academia.Credit import Credit, AcademicException
from academia.Course import Course
from people.Student import Student
from academia.Group import Group

def test_credit_init():
    course = Course("Math", 5)
    credit = Credit(course)
    assert credit.course == course
    assert credit.passed_students == set()

def test_award_credit():
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    course = Course("Math", 5)
    course.enroll_student(student)
    credit = Credit(course)
    credit.award_credit(student)
    assert student in credit.passed_students

def test_award_not_enrolled():
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    course = Course("Math", 5)
    credit = Credit(course)
    with pytest.raises(AcademicException):
        credit.award_credit(student)