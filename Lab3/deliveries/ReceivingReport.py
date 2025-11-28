from __future__ import annotations
from typing import List, Tuple
from datetime import datetime
from products.Product import Product
from deliveries.Delivery import Delivery
from staff.Employee import Employee


class ReceivingReport:
    """
    Документирует результат операции получения товаров.
    Содержит список пар (товар, фактическое_количество) и привязан к инспектору.
    Используется для проверки и обработки входящих поставок.
    """

    def __init__(
        self,
        delivery_id: str,
        items: List[Tuple[Product, int]],
        inspector: Employee
    ):
        if any(qty <= 0 for _, qty in items):
            raise ValueError("Received quantities must be positive")
        self.delivery_id = delivery_id
        self.items = items
        self.inspector = inspector
        self.report_date = datetime.now()

    def validate_against(self, delivery: Delivery) -> bool:
        """
        Проверяет, что все полученные товары присутствуют в исходной поставке.
        Возвращает True, если отчёт соответствует ожиданиям, иначе False.
        """
        expected_products = {item.product.id for item in delivery.items}
        reported_products = {product.id for product, _ in self.items}
        return reported_products.issubset(expected_products)

    def get_total_received_quantity(self) -> int:
        """
        Возвращает общее количество всех полученных единиц товаров.
        """
        return sum(quantity for _, quantity in self.items)

    def get_discrepancies(self, delivery: Delivery) -> List[dict]:
        """
        Возвращает список расхождений между ожидаемым и фактически полученным количеством.
        Каждый элемент содержит: product_id, expected, received, difference.
        """
        discrepancies = []
        expected_dict = {item.product.id: item.expected_quantity for item in delivery.items}
        received_dict = {product.id: quantity for product, quantity in self.items}

        for product_id, expected_qty in expected_dict.items():
            received_qty = received_dict.get(product_id, 0)
            if received_qty != expected_qty:
                discrepancies.append({
                    "product_id": product_id,
                    "expected": expected_qty,
                    "received": received_qty,
                    "difference": received_qty - expected_qty
                })

        return discrepancies