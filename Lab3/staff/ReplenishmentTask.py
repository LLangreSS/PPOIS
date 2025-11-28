from __future__ import annotations
from products.Product import Product
from warehouse.Location import Location

class ReplenishmentTask:
    """
    Представляет задачу пополнения пикинг-зоны из резервного хранения.
    Возникает, когда уровень товара в зоне сборки падает ниже порогового значения.
    """
    def __init__(
        self,
        id: str,
        product: Product,
        quantity: int,
        source_location: Location,
        destination_location: Location
    ):
        if quantity <= 0:
            raise ValueError("Replenishment quantity must be positive")
        if source_location.to_string() == destination_location.to_string():
            raise ValueError("Source and destination must be different")
        self.id = id
        self.product = product
        self.quantity = quantity
        self.source_location = source_location
        self.destination_location = destination_location
        self.status = "pending"

    def complete(self) -> None:
        """
        Помечает задачу как выполненную.
        """
        self.status = "completed"

    def is_urgent(self, current_stock: int, threshold: int) -> bool:
        """
        Определяет, является ли задача срочной на основе текущего запаса и порога.
        """
        return current_stock < threshold