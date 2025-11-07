import pytest
from people.Methodologist import Methodologist
from academia.Curriculum import Curriculum

def test_methodologist_init():
    m = Methodologist(1, "Meth", "m@example.com")
    assert m.name == "Meth"

def test_update_curriculum():
    m = Methodologist(1, "Meth", "m@example.com")
    curr = Curriculum("CS-2020")
    m.update_curriculum(curr, "New content")
    assert curr.content == "New content"