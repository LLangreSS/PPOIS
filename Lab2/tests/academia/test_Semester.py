import pytest
from academia.Semester import Semester
from academia.Course import Course

def test_semester_init():
    sem = Semester(2025, "Fall")
    assert sem.year == 2025
    assert sem.term == "Fall"
    assert sem.courses == []

def test_close_semester():
    sem = Semester(2025, "Fall")
    course = Course("Math", 5)
    sem.add_course(course)
    student = type('S', (), {})()
    course.students.append(student)
    sem.close_semester()
    assert course.students == []