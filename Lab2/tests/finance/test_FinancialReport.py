import pytest
from finance.FinancialReport import FinancialReport
from finance.Budget import Budget

def test_financial_report_summarize():
    budget = Budget(2025)
    budget.allocate("Salaries", 500000.0)
    report = FinancialReport(budget)
    summary = report.summarize()
    assert "500000.00" in summary
    assert "2025" in summary