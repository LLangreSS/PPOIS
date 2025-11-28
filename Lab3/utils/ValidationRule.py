from __future__ import annotations
from typing import Callable
from products.Product import Product

class ValidationRule:
    """
    Инкапсулирует одно бизнес-правило для проверки товара.
    Поддерживает динамическую композицию правил.
    """

    def __init__(self, name: str, predicate: Callable[[Product], bool]):
        self.name = name
        self.predicate = predicate

    def apply(self, product: Product) -> bool:
        """
        Применяет правило проверки к товару.
        """
        return self.predicate(product)

    def __str__(self) -> str:
        return f"ValidationRule: {self.name}"

    def and_rule(self, other: ValidationRule) -> "ValidationRule":
        """
        Создает новое правило, объединяющее текущее с другим через И.
        """
        def combined_predicate(product: Product) -> bool:
            return self.predicate(product) and other.predicate(product)

        return ValidationRule(f"{self.name}_AND_{other.name}", combined_predicate)