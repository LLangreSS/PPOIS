import pytest
from people.Dean import Dean
from academia.Faculty import Faculty

def test_dean_init():
    fac = Faculty("Eng")
    d = Dean(1, "Dean", "d@example.com", fac)
    assert d.faculty == fac
    assert fac.dean == d

def test_approve_study_plan():
    from academia.StudyPlan import StudyPlan
    from academia.Curriculum import Curriculum
    fac = Faculty("Eng")
    d = Dean(1, "Dean", "d@example.com", fac)
    plan = StudyPlan(Curriculum("CS-2020"))
    d.approve_study_plan(plan)
    assert plan.approved