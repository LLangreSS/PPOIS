import pytest
from people.Graduate import Graduate
from academia.Group import Group
from documents.Diploma import Diploma
from people.Person import Person

def test_graduate_init():
    group = Group("G1", 1)
    person = Person(1, "Grad", "g@example.com")
    diploma = Diploma(person, "Master")
    g = Graduate(2, "Grad", "g@example.com", group, diploma)
    assert g.diploma == diploma

def test_verify_diploma():
    group = Group("G1", 1)
    person = Person(1, "Grad", "g@example.com")
    diploma = Diploma(person, "Master")
    diploma.approved = True
    g = Graduate(2, "Grad", "g@example.com", group, diploma)
    assert g.verify_diploma() == True