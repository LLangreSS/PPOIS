from __future__ import annotations
from typing import List, Tuple
from products.Product import Product

class Container:
    """
    Представляет физический контейнер (коробку, ящик) для хранения нескольких единиц товара.
    Используется при сборке, возвратах или внутренней транспортировке.
    """
    def __init__(self, id: str, max_capacity_items: int = 50):
        if max_capacity_items <= 0:
            raise ValueError("Max capacity must be positive")
        self.id = id
        self.max_capacity_items = max_capacity_items
        self.contents: List[Tuple[Product, int]] = []

    def add_product(self, product: Product, quantity: int) -> None:
        """
        Добавляет указанное количество товара в контейнер.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.current_items() + quantity > self.max_capacity_items:
            raise ValueError("Container capacity exceeded")
        self.contents.append((product, quantity))

    def current_items(self) -> int:
        """
        Возвращает общее количество товаров в контейнере.
        """
        return sum(qty for _, qty in self.contents)

    def is_empty(self) -> bool:
        """
        Проверяет, пуст ли контейнер.
        """
        return len(self.contents) == 0