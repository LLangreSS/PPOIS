from __future__ import annotations

class FinancialReport:
    def __init__(self, budget: "Budget"):
        self.budget = budget
        self.generated_on = "2025-11-06"

    def summarize(self) -> str:
        return f"Total budget: {self.budget.get_total():.2f} for year {self.budget.fiscal_year}"

    def is_balanced(self) -> bool:
        return self.budget.get_total() > 0
