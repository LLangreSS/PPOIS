from __future__ import annotations
from typing import Optional
from datetime import datetime
from products.Product import Product
from warehouse.StorageCondition import StorageCondition

class Batch:
    """
    Представляет однородное количество товара, произведенное в одно и то же время.
    Отслеживает срок годности, происхождение и требования к хранению.
    """

    def __init__(
        self,
        id: str,
        product: Product,
        quantity: int,
        manufacture_date: datetime,
        expiry_date: Optional[datetime] = None,
        storage_condition: Optional[StorageCondition] = None
    ):
        if quantity <= 0:
            raise ValueError("Batch quantity must be positive")
        self.id = id
        self.product = product
        self.quantity = quantity
        self.manufacture_date = manufacture_date
        self.expiry_date = expiry_date
        self.storage_condition = storage_condition

    def is_expired(self, now: datetime = None) -> bool:
        """
        Проверяет, истек ли срок годности партии.
        """
        if now is None:
            now = datetime.now()
        return self.expiry_date is not None and now > self.expiry_date

    def get_remaining_shelf_life(self) -> Optional[int]:
        """
        Возвращает оставшийся срок годности в днях.
        """
        if self.expiry_date is None:
            return None
        now = datetime.now()
        remaining = self.expiry_date - now
        return remaining.days

    def split(self, new_quantity: int) -> "Batch":
        """
        Разделяет партию на две.
        """
        if new_quantity >= self.quantity:
            raise ValueError("New quantity must be less than current quantity")

        from utils.IdGenerator import IdGenerator
        new_batch = Batch(
            id=IdGenerator("BATCH").generate(),
            product=self.product,
            quantity=new_quantity,
            manufacture_date=self.manufacture_date,
            expiry_date=self.expiry_date,
            storage_condition=self.storage_condition
        )
        self.quantity -= new_quantity
        return new_batch