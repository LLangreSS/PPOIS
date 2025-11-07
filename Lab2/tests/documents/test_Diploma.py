import pytest
from documents.Diploma import Diploma
from people.Person import Person

def test_diploma_init():
    p = Person(1, "Grad", "g@example.com")
    d = Diploma(p, "Master of Science")
    assert d.degree == "Master of Science"
    assert d.owner == p

def test_is_authentic():
    p = Person(1, "Grad", "g@example.com")
    d = Diploma(p, "Master")
    d.approved = True
    assert d.is_authentic() == True