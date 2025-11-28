from __future__ import annotations
from datetime import datetime, time

class Shift:
    """
    Представляет запланированный рабочий период для сотрудника.
    Используется для определения, находится ли сотрудник в настоящее время на дежурстве.
    """

    def __init__(self, start_time: time, end_time: time, warehouse_id: str):
        if start_time >= end_time:
            raise ValueError("End time must be after start time")
        self.start_time = start_time
        self.end_time = end_time
        self.warehouse_id = warehouse_id

    def is_active(self, now: datetime = None) -> bool:
        """
        Проверяет, активна ли смена в указанное время.
        """
        if now is None:
            now = datetime.now()
        current_time = now.time()
        return self.start_time <= current_time <= self.end_time

    def get_duration_hours(self) -> float:
        """
        Возвращает продолжительность смены в часах.
        """
        start_dt = datetime.combine(datetime.today(), self.start_time)
        end_dt = datetime.combine(datetime.today(), self.end_time)
        duration = end_dt - start_dt
        return duration.total_seconds() / 3600

    def get_shift_type(self) -> str:
        """
        Определяет тип смены (утренняя, дневная, ночная).
        """
        if self.start_time.hour < 6:
            return "night"
        elif self.start_time.hour < 14:
            return "morning"
        else:
            return "day"