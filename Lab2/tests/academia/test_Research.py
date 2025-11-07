import pytest
from academia.Research import Research
from people.Teacher import Teacher
from academia.Department import Department

def test_research_init():
    dept = Department("CS")
    lead = Teacher(1, "Dr. A", "a@example.com", dept)
    research = Research("AI Paper", lead)
    assert research.title == "AI Paper"
    assert research.lead == lead
    assert research.participants == []

def test_add_participant():
    dept = Department("CS")
    lead = Teacher(1, "Dr. A", "a@example.com", dept)
    t2 = Teacher(2, "Dr. B", "b@example.com", dept)
    research = Research("AI Paper", lead)
    research.add_participant(t2)
    assert t2 in research.participants