import pytest
from infrastructure.Building import Building
from infrastructure.Classroom import Classroom
from infrastructure.Room import Room

def test_building_init():
    b = Building("Main", "Street 1")
    assert b.name == "Main"
    assert b.address == "Street 1"

def test_add_classroom():
    b = Building("Main", "Street 1")
    room = Classroom("101", 30)
    b.add_classroom(room)
    assert room in b.classrooms
    assert room.building == b