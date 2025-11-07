import pytest
from people.ForeignStudent import ForeignStudent
from academia.Group import Group
from documents.Visa import Visa
from people.Person import Person
from exceptions.VisaExpiredException import VisaExpiredException

def test_foreign_student_init():
    group = Group("G1", 1)
    person = Person(1, "Ali", "ali@example.com")
    visa = Visa(person, "2026-01-01")
    fs = ForeignStudent(2, "Ali", "ali@example.com", group, visa)
    assert fs.visa == visa

def test_renew_visa_ok():
    group = Group("G1", 1)
    person = Person(1, "Ali", "ali@example.com")
    visa = Visa(person, "2026-01-01")  # not expired
    fs = ForeignStudent(2, "Ali", "ali@example.com", group, visa)
    fs.renew_visa()  # should not raise

def test_renew_visa_expired():
    group = Group("G1", 1)
    person = Person(1, "Ali", "ali@example.com")
    visa = Visa(person, "2020-01-01")  # expired
    fs = ForeignStudent(2, "Ali", "ali@example.com", group, visa)
    with pytest.raises(VisaExpiredException):
        fs.renew_visa()