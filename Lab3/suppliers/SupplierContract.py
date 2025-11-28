from __future__ import annotations
from datetime import datetime, timedelta
from suppliers.Supplier import Supplier

class SupplierContract:
    """
    Представляет договор с поставщиком, включая срок действия и условия поставки.
    Используется для контроля законности операций и автоматического продления.
    """
    def __init__(
        self,
        id: str,
        supplier: Supplier,
        start_date: datetime,
        duration_days: int,
        auto_renew: bool = False
    ):
        if duration_days <= 0:
            raise ValueError("Contract cannot be empty")
        self.id = id
        self.supplier = supplier
        self.start_date = start_date
        self.end_date = start_date + timedelta(days=duration_days)
        self.auto_renew = auto_renew

    def is_active(self, now: datetime) -> bool:
        """Проверяет, действует ли договор на указанную дату."""
        return self.start_date <= now <= self.end_date

    def should_renew(self, now: datetime) -> bool:
        """Определяет, пора ли продлевать договор (за 7 дней до окончания)."""
        return (
            self.auto_renew
            and (self.end_date - now).days <= 7
            and now <= self.end_date
        )