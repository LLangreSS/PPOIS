from __future__ import annotations
from suppliers.Supplier import Supplier
from datetime import datetime

class SupplierPortalEvent:
    """
    Представляет событие в системе взаимодействия с поставщиком (портале).
    Примеры: подтверждение заказа, отправка инвойса, запрос на изменение даты.
    """
    def __init__(self, event_type: str, supplier: Supplier, payload: dict):
        if not event_type.strip():
            raise ValueError("Type of event cannot be empty")
        self.event_type = event_type.strip()
        self.supplier = supplier
        self.payload = payload
        self.timestamp = datetime.now()

    def is_confirmation(self) -> bool:
        return self.event_type == "delivery_confirmation"

    def to_log_entry(self) -> str:
        return f"[{self.timestamp}] {self.supplier.id} :: {self.event_type}"