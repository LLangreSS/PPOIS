import pytest
from people.Secretary import Secretary
from people.Student import Student
from academia.Group import Group
from academia.Credit import Credit
from academia.Exam import Exam
from academia.Course import Course

def test_secretary_init():
    s = Secretary(1, "Sec", "s@example.com")
    assert s.name == "Sec"

def test_notify_exam_schedule():
    s = Secretary(1, "Sec", "s@example.com")
    course = Course("Math", 5)
    exam = Exam(course, "2025-12-01")
    msg = s.notify_exam_schedule(exam)
    assert "Math" in msg
    assert "2025-12-01" in msg