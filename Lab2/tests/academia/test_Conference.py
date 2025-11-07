import pytest
from academia.Conference import Conference
from academia.Research import Research
from people.Teacher import Teacher
from academia.Department import Department

def test_conference_init():
    conf = Conference("AI Conf", "Moscow")
    assert conf.name == "AI Conf"
    assert conf.location == "Moscow"
    assert conf.researches == []

def test_accept_research():
    dept = Department("CS")
    lead = Teacher(1, "Dr. A", "a@example.com", dept)
    research = Research("AI Paper", lead)
    conf = Conference("AI Conf", "Moscow")
    conf.accept_research(research)
    assert research in conf.researches