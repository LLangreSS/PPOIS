from __future__ import annotations
from typing import List, Tuple
from products.Product import Product


class PackingSlip:
    """
    Документ, перечисляющий все товары, включенные в отгрузку.
    Используется для проверки сотрудниками склада и клиентами.
    """

    def __init__(self, shipment_id: str, items: List[Tuple[Product, int]]):
        if not items:
            raise ValueError("Packing slip must contain items")
        self.shipment_id = shipment_id
        self.items = items

    def to_pdf(self) -> bytes:
        """
        Генерирует текстовое представление упаковочного листа на русском языке (для печати/человека).
        """
        content = f"Упаковочный лист для {self.shipment_id}\n"
        content += "=" * 50 + "\n"
        for product, qty in self.items:
            content += f"- {product.name}: {qty} {product.unit.symbol}\n"
        return content.encode("utf-8")

    def get_total_quantity(self) -> int:
        """
        Возвращает общее количество всех товаров в упаковочном листе.
        """
        return sum(quantity for _, quantity in self.items)

    def validate_against_order(self, order_lines: List) -> bool:
        """
        Проверяет, что содержимое упаковочного листа точно соответствует строкам заказа.
        """
        slip_products = {product.id: quantity for product, quantity in self.items}
        order_products = {line.product.id: line.quantity for line in order_lines}
        return slip_products == order_products