from __future__ import annotations
from typing import List
from datetime import datetime
from deliveries.Delivery import Delivery
from staff.Employee import Employee
from warehouse.InventorySlot import InventorySlot
from warehouse.Warehouse import Warehouse


class UnloadingOperation:
    """
    Представляет физический акт разгрузки поставки и размещения товаров на складе.
    Оркестрирует создание слотов инвентаря на основе полученных партий.
    """

    def __init__(self, delivery: Delivery, operator: Employee, warehouse: Warehouse):
        if delivery.received_at is None:
            raise ValueError("Delivery must be received before unloading")
        self.delivery = delivery
        self.operator = operator
        self.warehouse = warehouse
        self.timestamp = datetime.now()
        self.status = "in_progress"

    def process(self) -> List[InventorySlot]:
        """
        Выполняет разгрузку: для каждой полученной позиции создаёт партию и выделяет слот на складе.
        Возвращает список созданных слотов инвентаря.
        """
        slots = []
        for item in self.delivery.items:
            if item.received_quantity <= 0:
                continue
            batch = item.create_batch()
            slot = self.warehouse.allocate_slot(
                product=item.product,
                quantity=item.received_quantity
            )
            slots.append(slot)
        self.status = "completed"
        return slots

    def get_operation_summary(self) -> dict:
        """
        Возвращает сводку по операции разгрузки в виде словаря с ключами и значениями на английском языке.
        """
        return {
            "delivery_id": self.delivery.id,
            "operator": self.operator.name,
            "timestamp": self.timestamp,
            "status": self.status,
            "total_items": len(self.delivery.items)
        }