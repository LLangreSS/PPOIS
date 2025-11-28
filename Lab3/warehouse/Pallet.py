from __future__ import annotations
from typing import List
from warehouse.Location import Location
from warehouse.Batch import Batch
from exceptions.OverloadedPalletError import OverloadedPalletError

class Pallet:
    """
    Представляет стандартный носитель груза (например, деревянный или пластиковый паллет).
    Содержит несколько партий и обеспечивает соблюдение ограничений по весу и пространству.
    """

    def __init__(self, id: str, location: Location, max_weight: float = 1000.0):
        self.id = id
        self.location = location
        self.batches: List[Batch] = []
        self.max_weight = max_weight

    @property
    def total_weight(self) -> float:
        """
        Возвращает общий вес всех партий на паллете.
        """
        return sum(batch.quantity * batch.product.spec.weight_kg for batch in self.batches)

    @property
    def remaining_capacity_kg(self) -> float:
        """
        Возвращает оставшуюся грузоподъемность паллета в килограммах.
        """
        return self.max_weight - self.total_weight

    @property
    def max_dimensions(self) -> tuple[float, float, float]:
        """
        Возвращает максимальные размеры паллета (длина, ширина, высота).
        """
        max_height = 150
        max_width = 100
        max_length = 120
        return (max_length, max_width, max_height)
    def add_batch(self, batch: Batch) -> None:
        """
        Добавляет партию на паллет с проверкой весовых ограничений.
        """
        new_weight = self.total_weight + batch.quantity * batch.product.spec.weight_kg
        if new_weight > self.max_weight:
            raise OverloadedPalletError(
                f"Pallet {self.id} would exceed maximum weight ({self.max_weight} kg)"
            )
        self.batches.append(batch)

    def is_overloaded(self) -> bool:
        """
        Проверяет, превышает ли паллет максимальную грузоподъемность.
        """
        return self.total_weight > self.max_weight

    def get_batch_by_product(self, product_id: str) -> Batch:
        """
        Находит партию по ID товара.
        """
        for batch in self.batches:
            if batch.product.id == product_id:
                return batch
        return None

    def remove_batch(self, batch_id: str) -> bool:
        """
        Удаляет партию с паллета.
        """
        for i, batch in enumerate(self.batches):
            if batch.id == batch_id:
                self.batches.pop(i)
                return True
        return False