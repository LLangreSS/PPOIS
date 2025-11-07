import pytest
from academia.Schedule import Schedule, InvalidScheduleException
from academia.Course import Course
from infrastructure.Classroom import Classroom

def test_schedule_init():
    s = Schedule()
    assert s.entries == []

def test_add_entry():
    s = Schedule()
    course = Course("Math", 5)
    classroom = Classroom("101", 30)
    s.add_entry(course, classroom, "Mon 10:00")
    assert len(s.entries) == 1
    assert not classroom.is_available("Mon 10:00")

def test_add_entry_conflict():
    s = Schedule()
    course = Course("Math", 5)
    classroom = Classroom("101", 30)
    classroom.book("Mon 10:00")
    with pytest.raises(InvalidScheduleException):
        s.add_entry(course, classroom, "Mon 10:00")