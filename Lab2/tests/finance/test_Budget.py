import pytest
from finance.Budget import Budget

def test_budget_init():
    b = Budget(2025)
    assert b.fiscal_year == 2025
    assert b.allocations == {}

def test_allocate():
    b = Budget(2025)
    b.allocate("Salaries", 500000.0)
    assert b.allocations["Salaries"] == 500000.0