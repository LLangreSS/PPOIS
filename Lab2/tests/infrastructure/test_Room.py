import pytest
from infrastructure.Room import Room, RoomCapacityException
from people.Student import Student
from academia.Group import Group

def test_room_init():
    r = Room("201", 2)
    assert r.number == "201"
    assert r.capacity == 2

def test_assign_student():
    r = Room("201", 1)
    group = Group("G1", 1)
    s1 = Student(1, "A", "a@example.com", group)
    r.assign_student(s1)
    assert s1 in r.occupants

def test_assign_over_capacity():
    r = Room("201", 1)
    group = Group("G1", 1)
    s1 = Student(1, "A", "a@example.com", group)
    s2 = Student(2, "B", "b@example.com", group)
    r.assign_student(s1)
    with pytest.raises(RoomCapacityException):
        r.assign_student(s2)