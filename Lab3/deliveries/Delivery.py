from __future__ import annotations
from typing import List, Optional
from datetime import datetime
from suppliers.Supplier import Supplier
from deliveries.DeliveryItem import DeliveryItem
from exceptions.DuplicateDeliveryError import DuplicateDeliveryError


class Delivery:
    """
    Представляет входящую поставку от поставщика.
    Содержит позиции поставки и отслеживает статус получения.
    """
    def __init__(self, id: str, supplier: Supplier, items: List[DeliveryItem]):
        if not items:
            raise ValueError("Delivery must contain at least one item")
        self.id = id
        self.supplier = supplier
        self.items = items
        self.received_at: Optional[datetime] = None
        self.expected_date = datetime.now()

    def receive_items(self, report) -> None:
        """
        Обрабатывает получение поставки на основе отчёта о приёмке.
        Устанавливает полученные количества для каждой позиции и фиксирует время приёмки.
        """
        if self.received_at is not None:
            raise DuplicateDeliveryError(f"Delivery {self.id} already received")
        if not report.validate_against(self):
            raise ValueError("Receiving report contains unexpected products")

        reported = {product.id: qty for product, qty in report.items}
        for item in self.items:
            if item.product.id in reported:
                item.received_quantity = reported[item.product.id]
        self.received_at = datetime.now()

    def is_complete(self) -> bool:
        """
        Проверяет, полностью ли выполнена поставка (все позиции получены в ожидаемом количестве).
        """
        return all(
            item.received_quantity == item.expected_quantity
            for item in self.items
        )

    def get_total_expected_quantity(self) -> int:
        """
        Возвращает общее ожидаемое количество всех позиций в поставке.
        """
        return sum(item.expected_quantity for item in self.items)

    def get_total_received_quantity(self) -> int:
        """
        Возвращает общее количество фактически полученных товаров по всем позициям.
        """
        return sum(item.received_quantity for item in self.items)

    def is_overdue(self) -> bool:
        """
        Определяет, просрочена ли поставка: текущая дата позже ожидаемой, а поставка ещё не получена.
        """
        return datetime.now() > self.expected_date and self.received_at is None