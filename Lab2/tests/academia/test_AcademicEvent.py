import pytest
from academia.AcademicEvent import AcademicEvent

def test_academic_event_init():
    event = AcademicEvent("Graduation", "2025-06-15", "Ceremony")
    assert event.name == "Graduation"
    assert event.date == "2025-06-15"
    assert event.description == "Ceremony"

def test_is_upcoming():
    past = AcademicEvent("Past", "2020-01-01")
    future = AcademicEvent("Future", "2030-01-01")
    assert not past.is_upcoming()
    assert future.is_upcoming()