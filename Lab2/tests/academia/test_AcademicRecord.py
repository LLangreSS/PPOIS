import pytest

from people.Student import Student
from academia.Group import Group
from academia.AcademicRecord import AcademicRecord

def test_academic_record_init():
    g = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", g)
    record = s.academic_record
    assert record.student == s
    assert record.grades == []

def test_get_gpa():
    g = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", g)
    from academia.Grade import Grade
    from academia.Course import Course
    c = Course("Math", 5)
    Grade(s, c, 80.0)
    Grade(s, c, 90.0)
    assert s.academic_record.get_gpa() == 85.0