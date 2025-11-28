from __future__ import annotations
from typing import List
from warehouse.Pallet import Pallet
from exceptions.SlotAllocationError import SlotAllocationError

class Shelf:
    """
    Представляет стеллаж для хранения в пределах зоны хранения.
    Содержит ограниченное количество паллетов и отслеживает доступное пространство.
    """

    def __init__(self, id: str, zone_id: str, max_pallets: int = 4):
        self.id = id
        self.zone_id = zone_id
        self.pallets: List[Pallet] = []
        self.max_pallets = max_pallets

    def has_space(self) -> bool:
        """
        Проверяет, есть ли свободное место на стеллаже.
        """
        return len(self.pallets) < self.max_pallets

    def add_pallet(self, pallet: Pallet) -> None:
        """
        Добавляет паллет на стеллаж при наличии свободного места.
        """
        if not self.has_space():
            raise SlotAllocationError(f"Shelf {self.id} has no space for additional pallets")
        self.pallets.append(pallet)

    def remove_pallet(self, pallet_id: str) -> bool:
        """
        Удаляет паллет со стеллажа.
        """
        for i, pallet in enumerate(self.pallets):
            if pallet.id == pallet_id:
                self.pallets.pop(i)
                return True
        return False

    def get_pallet_locations(self) -> List[str]:
        """
        Возвращает список местоположений всех паллетов на стеллаже.
        """
        return [pallet.location.to_string() for pallet in self.pallets]