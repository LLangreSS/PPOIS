import pytest
from academia.Faculty import Faculty
from academia.Department import Department

def test_faculty_init():
    f = Faculty("Engineering")
    assert f.name == "Engineering"
    assert f.dean is None
    assert f.departments == []

def test_add_department():
    f = Faculty("Eng")
    d = Department("CS")
    f.add_department(d)
    assert d in f.departments
    assert d.faculty == f