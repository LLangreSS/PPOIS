from datetime import datetime

class ReservedSlot:
    """
    Представляет количество товара, зарезервированное из слота инвентаря,
    обычно для выполнения заказа или передачи.
    Может быть освобождено обратно при отмене операции.
    """

    def __init__(self, slot_id: str, reserved_quantity: int, reserved_for: str):
        self.slot_id = slot_id
        self.reserved_quantity = reserved_quantity
        self.reserved_for = reserved_for
        self.reserved_at = datetime.now()

    def release(self) -> dict:
        """
        Освобождает зарезервированное количество обратно в исходный слот.
        Возвращает полезную нагрузку для обработки системой инвентаря.
        """
        return {
            "slot_id": self.slot_id,
            "quantity_to_restore": self.reserved_quantity,
            "reserved_for": self.reserved_for
        }

    def is_expired(self, expiry_minutes: int = 30) -> bool:
        """Проверяет, истекло ли время резервирования."""
        from datetime import timedelta
        if self.reserved_at is None:
            return False
        return datetime.now() > self.reserved_at + timedelta(minutes=expiry_minutes)

