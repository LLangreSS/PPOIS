import pytest
from academia.Department import Department
from people.Teacher import Teacher

def test_department_init():
    d = Department("CS")
    assert d.name == "CS"
    assert d.teachers == []
    assert d.head is None

def test_get_head_name():
    d = Department("CS")
    assert d.get_head_name() == "None"
    # Head устанавливается в HeadOfDepartment