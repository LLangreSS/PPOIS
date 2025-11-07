import pytest
from people.Student import Student
from academia.Group import Group
from academia.Course import Course
from finance.Payment import Payment

def test_student_init():
    group = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", group, 1000.0)
    assert s.name == "Alex"
    assert s.group == group
    assert s.balance == 1000.0
    assert s in group.students

def test_enroll_in_course():
    group = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", group)
    course = Course("Math", 5)
    s.enroll_in_course(course)
    assert s in course.students

def test_pay_tuition():
    group = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", group, 1000.0)
    payment = s.pay_tuition(200.0)
    assert isinstance(payment, Payment)
    assert s.balance == 800.0
    assert payment.processed

def test_transfer_to_group():
    g1 = Group("G1", 1)
    g2 = Group("G2", 1)
    s = Student(1, "Alex", "a@example.com", g1)
    s.transfer_to_group(g2)
    assert s.group == g2
    assert s not in g1.students
    assert s in g2.students