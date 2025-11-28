from __future__ import annotations
from typing import List, Optional
from warehouse.Shelf import Shelf
from warehouse.StorageCondition import StorageCondition
from products.Product import Product

class StorageZone:
    """
    Представляет выделенную область на складе с однородными условиями хранения,
    такую как холодильная секция или зона для сухих товаров.
    Управляет стеллажами и проверяет совместимость товаров.
    """

    def __init__(
        self,
        id: str,
        name: str,
        condition: StorageCondition,
        max_load_kg: float = 10000.0
    ):
        self.id = id
        self.name = name
        self.condition = condition
        self.shelves: List[Shelf] = []
        self.max_load_kg = max_load_kg

    def current_load(self) -> float:
        """
        Возвращает текущую нагрузку зоны в килограммах.
        """
        total = 0.0
        for shelf in self.shelves:
            for pallet in shelf.pallets:
                total += pallet.total_weight
        return total

    def is_compatible(self, product: Product) -> bool:
        """
        Проверяет совместимость товара с условиями зоны хранения.
        """
        notes = product.spec.storage_notes.lower()
        if "cold" in notes or "refrigerated" in notes:
            return self.condition.temp_max <= 10.0
        if "dry" in notes:
            return self.condition.humidity_max <= 60.0
        return True

    def find_available_shelf(self) -> Optional[Shelf]:
        """
        Находит стеллаж со свободным местом в зоне.
        """
        for shelf in self.shelves:
            if shelf.has_space():
                return shelf
        return None

    def add_shelf(self, shelf: Shelf) -> None:
        """
        Добавляет стеллаж в зону.
        """
        self.shelves.append(shelf)

    def get_utilization_percentage(self) -> float:
        """
        Возвращает процент использования зоны.
        """
        return (self.current_load() / self.max_load_kg) * 100