import pytest
from academia.Grade import Grade, InvalidGradeException
from people.Student import Student
from academia.Course import Course
from academia.Group import Group

def test_grade_valid():
    g = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", g)
    c = Course("Math", 5)
    grade = Grade(s, c, 90.0)
    assert grade.value == 90.0
    assert grade in s.academic_record.grades

def test_grade_invalid():
    g = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", g)
    c = Course("Math", 5)
    with pytest.raises(InvalidGradeException):
        Grade(s, c, 150.0)