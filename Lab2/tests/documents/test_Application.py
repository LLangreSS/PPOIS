import pytest
from documents.Application import Application
from people.Person import Person

def test_application_init():
    applicant = Person(1, "Alex", "a@example.com")
    app = Application(applicant, "Computer Science")
    assert app.program == "Computer Science"
    assert app.owner == applicant
    assert app.submitted == False

def test_is_complete():
    applicant = Person(1, "Alex", "a@example.com")
    app = Application(applicant, "CS")
    assert app.is_complete() == True