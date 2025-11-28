# DeliverySchedule.py
from __future__ import annotations
from typing import List
from suppliers.Supplier import Supplier
from datetime import time

class DeliverySchedule:
    """
    Определяет график поставок от поставщика: дни недели и временные окна приёма.
    Используется для планирования разгрузки и выделения ресурсов.
    """
    def __init__(
        self,
        supplier: Supplier,
        delivery_days: List[int],
        time_window_start: time,
        time_window_end: time
    ):
        if not delivery_days:
            raise ValueError("Schedule must include at least one day")
        if time_window_start >= time_window_end:
            raise ValueError("Start time must be earlier than end time")
        self.supplier = supplier
        self.delivery_days = delivery_days
        self.time_window_start = time_window_start
        self.time_window_end = time_window_end

    def is_valid_delivery_day(self, weekday: int) -> bool:
        """
        Проверяет, разрешена ли поставка в указанный день недели (0-6).
        """
        return weekday in self.delivery_days

    def is_within_time_window(self, t: time) -> bool:
        """
        Проверяет, попадает ли время в разрешённое окно.
        """
        return self.time_window_start <= t <= self.time_window_end