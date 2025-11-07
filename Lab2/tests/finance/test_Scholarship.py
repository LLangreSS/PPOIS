import pytest
from finance.Scholarship import Scholarship, ScholarshipCriteriaException
from people.Student import Student
from academia.Group import Group

def test_scholarship_eligible():
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    # Добавим высокую оценку
    from academia.Grade import Grade
    from academia.Course import Course
    c = Course("Math", 5)
    Grade(student, c, 90.0)
    scholarship = Scholarship(student, 10000)
    assert scholarship.evaluate_eligibility() == True

def test_scholarship_not_eligible():
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    scholarship = Scholarship(student, 10000)
    with pytest.raises(ScholarshipCriteriaException):
        scholarship.evaluate_eligibility()