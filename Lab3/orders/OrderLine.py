from __future__ import annotations
from products.Product import Product


class OrderLine:
    """
    Представляет одну товарную позицию в заказе клиента.
    Отслеживает запрошенное и выполненное количество.
    """

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Order quantity must be positive")
        self.product = product
        self.quantity = quantity
        self.fulfilled = 0

    def is_fulfilled(self) -> bool:
        """
        Проверяет, полностью ли выполнена строка заказа.
        """
        return self.fulfilled >= self.quantity

    def fulfill(self, amount: int) -> None:
        """
        Выполняет указанное количество товара в рамках строки заказа.
        Увеличивает счётчик выполненного количества.
        """
        if amount <= 0:
            raise ValueError("Fulfill amount must be positive")
        if self.fulfilled + amount > self.quantity:
            raise ValueError("Fulfill amount exceeds order line quantity")
        self.fulfilled += amount

    def get_remaining_quantity(self) -> int:
        """
        Возвращает оставшееся количество товара, которое ещё нужно выполнить.
        """
        return self.quantity - self.fulfilled

    def get_fulfillment_percentage(self) -> float:
        """
        Возвращает процент выполнения строки заказа (от 0.0 до 100.0).
        """
        return (self.fulfilled / self.quantity) * 100