from __future__ import annotations
from typing import Optional
from datetime import datetime
from products.Product import Product

class InternalTransfer:
    """
    Представляет внутреннюю перемещение товара между зонами или стеллажами склада.
    Используется для перераспределения запасов, консолидации или исправления ошибок размещения.
    """
    def __init__(
        self,
        id: str,
        product: Product,
        quantity: int,
        source_location: str,
        destination_location: str
    ):
        if quantity <= 0:
            raise ValueError("Transfer quantity must be positive")
        if source_location == destination_location:
            raise ValueError("Source and destination must be different")
        self.id = id
        self.product = product
        self.quantity = quantity
        self.source_location = source_location
        self.destination_location = destination_location
        self.status = "pending"
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None

    def execute(self, operator_id: str) -> None:
        """
        Выполняет перемещение (только для внутреннего использования системой).
        """
        if self.status != "pending":
            raise ValueError("Transfer already processed")
        self.status = "executed_by_operator"
        self.completed_at = datetime.now()

    def is_completed(self) -> bool:
        """
        Проверяет, завершено ли перемещение.
        """
        return self.status.startswith("executed")

    def get_transfer_summary(self) -> dict:
        """
        Возвращает сводку по перемещению.
        """
        return {
            "id": self.id,
            "product_id": self.product.id,
            "quantity": self.quantity,
            "from": self.source_location,
            "to": self.destination_location,
            "status": self.status,
            "created_at": self.created_at
        }