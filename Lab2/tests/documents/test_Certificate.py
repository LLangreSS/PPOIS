import pytest
from documents.Certificate import Certificate
from people.Person import Person

def test_certificate_init():
    p = Person(1, "Alex", "a@example.com")
    cert = Certificate(p, "Language Proficiency")
    assert cert.title == "Language Proficiency"
    assert cert.owner == p

def test_is_valid_for_visa():
    p = Person(1, "Alex", "a@example.com")
    cert = Certificate(p, "Language Certificate")
    cert.approved = True
    assert cert.is_valid_for_visa() == True