import pytest
from infrastructure.Classroom import Classroom

def test_classroom_init():
    c = Classroom("101", 30)
    assert c.room_number == "101"
    assert c.capacity == 30

def test_book():
    c = Classroom("101", 30)
    c.book("Mon 10:00")
    assert not c.is_available("Mon 10:00")