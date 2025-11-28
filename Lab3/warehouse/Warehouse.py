from __future__ import annotations
from typing import List, Optional
from warehouse.Location import Location
from warehouse.StorageZone import StorageZone
from warehouse.Pallet import Pallet
from products.Product import Product
from warehouse.InventorySlot import InventorySlot
from warehouse.WarehouseConfig import WarehouseConfig
from exceptions.SlotAllocationError import SlotAllocationError
from warehouse.Batch import Batch
from utils.IdGenerator import IdGenerator
from datetime import datetime

class Warehouse:
    """
    Верхнеуровневый контейнер для всех складских операций.
    Управляет зонами хранения, распределяет слоты инвентаря и маршрутизирует товары.
    """

    def __init__(self, id: str, name: str, config: WarehouseConfig):
        self.id = id
        self.name = name
        self.config = config
        self.zones: List[StorageZone] = []

    def find_available_zone(self, product: Product) -> Optional[StorageZone]:
        """
        Находит доступную зону хранения, совместимую с товаром.
        """
        for zone in self.zones:
            if zone.is_compatible(product):
                if zone.find_available_shelf() is not None:
                    return zone
        return None

    def allocate_slot(self, product: Product, quantity: int) -> InventorySlot:
        """
        Распределяет слот инвентаря для товара в подходящей зоне хранения.
        """
        zone = self.find_available_zone(product)
        if zone is None:
            raise SlotAllocationError(f"No suitable zone for product {product.id}")

        shelf = zone.find_available_shelf()
        if shelf is None:
            raise SlotAllocationError(f"No available shelves in zone {zone.id}")

        batch_id = IdGenerator("BATCH").generate()
        batch = Batch(
            id=batch_id,
            product=product,
            quantity=quantity,
            manufacture_date=datetime.now()
        )

        pallet_id = IdGenerator("PALLET").generate()
        pallet = Pallet(id=pallet_id, location=Location("R1", "RK1", shelf.id, zone.id))

        try:
            pallet.add_batch(batch)
        except Exception as e:
            raise SlotAllocationError(f"Cannot place batch on pallet: {e}")

        shelf.add_pallet(pallet)
        slot_id = IdGenerator("SLOT").generate()
        return InventorySlot(id=slot_id, location=pallet.location, batch=batch, quantity=quantity)

    def add_zone(self, zone: StorageZone) -> None:
        """
        Добавляет зону хранения на склад.
        """
        self.zones.append(zone)

    def get_total_capacity(self) -> float:
        """
        Возвращает общую вместимость склада.
        """
        return sum(zone.max_load_kg for zone in self.zones)

    def get_current_utilization(self) -> float:
        """
        Возвращает текущую загрузку склада.
        """
        total_load = sum(zone.current_load() for zone in self.zones)
        total_capacity = self.get_total_capacity()
        return (total_load / total_capacity) * 100 if total_capacity > 0 else 0