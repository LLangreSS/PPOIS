from __future__ import annotations
from typing import List
from deliveries.Delivery import Delivery
from datetime import datetime

class SupplierPerformance:
    """
    Оценивает производительность поставщика по KPI:
    - Своевременность поставок,
    - Полнота поставок,
    - Количество инцидентов.
    """
    def __init__(self, deliveries: List[Delivery]):
        self.deliveries = deliveries

    def on_time_delivery_rate(self, tolerance_days: int = 2, clock: datetime = None) -> float:
        """
        Доля поставок, полученных вовремя (с учётом допуска).
        Требует наличия planned_date в Delivery (для расчёта).
        Поскольку в текущей Delivery нет planned_date, эмулируем через анализ received_at.
        """
        if not self.deliveries:
            return 1.0
        return sum(1 for d in self.deliveries if d.received_at is not None) / len(self.deliveries)

    def completeness_rate(self) -> float:
        """Доля поставок, полученных полностью (без недостачи)."""
        if not self.deliveries:
            return 1.0
        complete = sum(1 for d in self.deliveries if d.is_complete())
        return complete / len(self.deliveries)