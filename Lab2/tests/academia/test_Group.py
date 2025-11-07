import pytest
from academia.Group import Group

def test_group_init():
    g = Group("G1", 2)
    assert g.group_id == "G1"
    assert g.course_year == 2
    assert g.students == []

def test_promote_to_next_year():
    g = Group("G1", 2)
    g.promote_to_next_year()
    assert g.course_year == 3