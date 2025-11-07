import pytest
from academia.StudyPlan import StudyPlan
from academia.Curriculum import Curriculum

def test_study_plan_init():
    curr = Curriculum("CS-2020")
    plan = StudyPlan(curr)
    assert plan.curriculum == curr
    assert plan.approved == False

def test_is_valid():
    curr = Curriculum("CS-2020", "Content")
    plan = StudyPlan(curr)
    assert plan.is_valid() == False
    plan.approved = True
    assert plan.is_valid() == True