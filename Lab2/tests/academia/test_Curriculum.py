import pytest
from academia.Curriculum import Curriculum

def test_curriculum_init():
    c = Curriculum("CS-2020", "Algorithms, Math")
    assert c.program == "CS-2020"
    assert c.content == "Algorithms, Math"

def test_is_outdated():
    c = Curriculum("CS-2010")
    assert c.is_outdated(2025) == True
    c2 = Curriculum("CS-2022")
    assert c2.is_outdated(2025) == False