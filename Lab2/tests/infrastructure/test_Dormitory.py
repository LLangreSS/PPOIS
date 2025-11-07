import pytest
from infrastructure.Dormitory import Dormitory
from infrastructure.Room import Room
from people.Student import Student
from academia.Group import Group

def test_dormitory_init():
    d = Dormitory("Dorm1", "Street 2")
    assert d.name == "Dorm1"

def test_assign_room_to_student():
    d = Dormitory("Dorm1", "Street 2")
    room = Room("201", 1)
    d.add_room(room)
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    d.assign_room_to_student(student, "201")
    assert student in room.occupants