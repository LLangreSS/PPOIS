from __future__ import annotations
from products.Product import Product
from warehouse.Batch import Batch
from datetime import datetime
from utils.IdGenerator import IdGenerator


class DeliveryItem:
    """
    Представляет одну товарную позицию в поставке от поставщика.
    Отслеживает ожидаемое и полученное количество, а также связывает позицию с партией при приёмке.
    """

    def __init__(self, product: Product, expected_quantity: int):
        if expected_quantity <= 0:
            raise ValueError("Expected quantity must be positive")
        self.product = product
        self.expected_quantity = expected_quantity
        self.received_quantity = 0
        self.batch_id: str = ""

    def create_batch(self) -> Batch:
        """
        Создаёт партию на основе полученного количества.
        Генерирует уникальный идентификатор партии и привязывает её к товару и дате производства.
        """
        if self.received_quantity <= 0:
            raise ValueError("Cannot create batch: no items received")
        batch_id = IdGenerator("BATCH").generate()
        self.batch_id = batch_id
        return Batch(
            id=batch_id,
            product=self.product,
            quantity=self.received_quantity,
            manufacture_date=datetime.now()
        )

    def get_receipt_status(self) -> str:
        """
        Возвращает текстовый статус получения товара на английском языке:
        'Not received', 'Partially received', 'Fully received' или 'Over-delivered'.
        """
        if self.received_quantity == 0:
            return "Not received"
        elif self.received_quantity < self.expected_quantity:
            return "Partially received"
        elif self.received_quantity == self.expected_quantity:
            return "Fully received"
        else:
            return "Over-delivered"