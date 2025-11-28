from __future__ import annotations
from typing import List
from datetime import datetime
from products.Product import Product


class ReturnRequest:
    """
    Представляет запрос клиента на возврат товаров из выполненного заказа.
    Включает причину и список товаров для возврата.
    """

    def __init__(self, order_id: str, reason: str, items: List[Product]):
        if not items:
            raise ValueError("Return request must include at least one product")
        if not reason.strip():
            raise ValueError("Return reason cannot be empty")
        self.order_id = order_id
        self.reason = reason.strip()
        self.items = items
        self.request_date = datetime.now()
        self.status = "under_review"

    def validate(self) -> bool:
        """
        Проверяет, можно ли принять возврат: запрещено возвращать опасные товары.
        """
        for product in self.items:
            if product.is_hazardous():
                return False
        return True

    def approve(self) -> None:
        """
        Одобряет или отклоняет запрос на возврат на основе валидации.
        Обновляет статус соответствующим образом.
        """
        if self.validate():
            self.status = "approved"
        else:
            self.status = "rejected"

    def get_return_summary(self) -> dict:
        """
        Возвращает сводку по запросу на возврат в виде словаря с ключами на английском языке.
        """
        return {
            "order_id": self.order_id,
            "reason": self.reason,
            "item_count": len(self.items),
            "status": self.status,
            "request_date": self.request_date
        }