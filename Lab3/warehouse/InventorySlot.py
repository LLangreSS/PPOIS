from __future__ import annotations
from warehouse.Location import Location
from warehouse.Batch import Batch
from warehouse.ReservedSlot import ReservedSlot

class InventorySlot:
    """
    Представляет физический или логический слот на складе, содержащий определенную партию товара.
    Отслеживает количество и местоположение, поддерживает резервирование для исходящих операций.
    """

    def __init__(self, id: str, location: Location, batch: Batch, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.id = id
        self.location = location
        self.batch = batch
        self.quantity = quantity
        self.reserved_quantity = 0

    def is_empty(self) -> bool:
        """
        Возвращает True, если слот не содержит товаров.
        """
        return self.quantity <= 0

    def reserve(self, quantity: int, reserved_for: str) -> "ReservedSlot":
        """
        Резервирует заданное количество из этого слота для определенной цели (например, ID заказа).
        Вызывает исключение при недостаточном количестве товара.
        """
        if quantity > self.available_quantity():
            from exceptions.InsufficientStockError import InsufficientStockError
            raise InsufficientStockError(f"Requested {quantity}, available {self.available_quantity()}")
        self.reserved_quantity += quantity
        return ReservedSlot(slot_id=self.id, reserved_quantity=quantity, reserved_for=reserved_for)

    def available_quantity(self) -> int:
        """
        Возвращает количество доступное для резервирования.
        """
        return self.quantity - self.reserved_quantity

    def release_reservation(self, quantity: int) -> None:
        """
        Освобождает зарезервированное количество.
        """
        if quantity > self.reserved_quantity:
            raise ValueError("Cannot release more than reserved")
        self.reserved_quantity -= quantity

    def get_utilization_percentage(self) -> float:
        """
        Возвращает процент использования слота.
        """
        max_capacity = 100
        return (self.quantity / max_capacity) * 100