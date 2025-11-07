import pytest
from people.HeadOfDepartment import HeadOfDepartment
from academia.Department import Department

def test_head_init():
    dept = Department("CS")
    head = HeadOfDepartment(1, "Head", "h@example.com", dept)
    assert dept.head == head
    assert head in dept.teachers

def test_conduct_staff_meeting():
    dept = Department("CS")
    head = HeadOfDepartment(1, "Head", "h@example.com", dept)
    assert head.conduct_staff_meeting() == ["Head"]