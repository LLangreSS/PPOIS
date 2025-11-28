from __future__ import annotations
from typing import List
from datetime import datetime
from warehouse.InventorySlot import InventorySlot
from warehouse.ReservedSlot import ReservedSlot


class PickingList:
    """
    Список заданий для сборщиков склада, указывающий, из каких слотов собирать.
    Поддерживает резервирование инвентаря для предотвращения двойного сбора.
    """

    def __init__(self, order_id: str, slots: List[InventorySlot]):
        self.order_id = order_id
        self.slots = slots
        self.status = "created"
        self.created_date = datetime.now()

    def reserve_slots(self) -> List[ReservedSlot]:
        """
        Резервирует товары из указанных слотов под текущий заказ.
        Возвращает список созданных резервирований.
        """
        reserved = []
        for slot in self.slots:
            if slot.quantity <= 0:
                continue
            r = slot.reserve(slot.quantity, reserved_for=self.order_id)
            reserved.append(r)
        self.status = "reserved"
        return reserved

    def get_total_items(self) -> int:
        """
        Возвращает общее количество единиц товаров, подлежащих сборке.
        """
        return sum(slot.quantity for slot in self.slots)

    def mark_as_picked(self) -> None:
        """
        Отмечает список сборки как полностью собранный.
        """
        self.status = "picked"

    def get_picking_priority(self) -> str:
        """
        Определяет приоритет сборки на основе характеристик товаров:
        'high' — если есть опасные товары,
        'medium' — если есть хрупкие,
        'low' — в остальных случаях.
        """
        fragile_count = sum(1 for slot in self.slots if slot.batch.product.spec.is_fragile)
        hazardous_count = sum(1 for slot in self.slots if slot.batch.product.is_hazardous())

        if hazardous_count > 0:
            return "high"
        elif fragile_count > 0:
            return "medium"
        else:
            return "low"