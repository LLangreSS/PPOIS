from __future__ import annotations

class Budget:
    def __init__(self, fiscal_year: int):
        self.fiscal_year = fiscal_year
        self.allocations: dict[str, float] = {}

    def allocate(self, category: str, amount: float) -> None:
        self.allocations[category] = self.allocations.get(category, 0) + amount

    def get_total(self) -> float:
        return sum(self.allocations.values())

    def is_over_budget(self, category: str, amount: float) -> bool:
        return self.allocations.get(category, 0) + amount > 1_000_000

    def export_csv(self) -> str:
        return "\n".join(f"{k},{v}" for k, v in self.allocations.items())
