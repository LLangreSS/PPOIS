from __future__ import annotations
from typing import List, Dict
from datetime import datetime
from orders.OrderLine import OrderLine
from orders.PickingList import PickingList
from products.Product import Product


class CustomerOrder:
    """
    Представляет запрос клиента на один или несколько товаров.
    Управляет статусом выполнения и генерирует инструкции по сборке.
    """

    def __init__(self, id: str, customer_id: str, lines: List[OrderLine]):
        if not lines:
            raise ValueError("Order must contain at least one line")
        self.id = id
        self.customer_id = customer_id
        self.lines = lines
        self.status = "created"
        self.created_date = datetime.now()

    def can_fulfill(self, inventory: Dict[Product, int]) -> bool:
        """
        Проверяет, может ли заказ быть полностью выполнен на основе текущих запасов.
        """
        for line in self.lines:
            available = inventory.get(line.product, 0)
            if available < line.quantity:
                return False
        return True

    def generate_picking_list(self) -> PickingList:
        """
        Создаёт список сборки на основе позиций заказа.
        """
        if not all(line.quantity > 0 for line in self.lines):
            raise ValueError("Order contains invalid lines")
        return PickingList(order_id=self.id, slots=[])

    def get_total_quantity(self) -> int:
        """
        Возвращает общее количество всех товаров в заказе.
        """
        return sum(line.quantity for line in self.lines)

    def get_fulfillment_status(self) -> str:
        """
        Возвращает общий статус выполнения заказа на английском языке:
        'fully_fulfilled', 'partially_fulfilled' или 'not_fulfilled'.
        """
        if all(line.is_fulfilled() for line in self.lines):
            return "fully_fulfilled"
        elif any(line.fulfilled > 0 for line in self.lines):
            return "partially_fulfilled"
        else:
            return "not_fulfilled"

    def get_total_value(self, price_list: Dict[str, float]) -> float:
        """
        Вычисляет общую стоимость заказа на основе прайс-листа.
        """
        total = 0.0
        for line in self.lines:
            price = price_list.get(line.product.id, 0.0)
            total += price * line.quantity
        return total