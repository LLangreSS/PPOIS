from __future__ import annotations
from typing import List
from datetime import datetime
from warehouse.Batch import Batch
from orders.PackingSlip import PackingSlip
from orders.ShippingLabel import ShippingLabel
from utils.IdGenerator import IdGenerator


class Shipment:
    """
    Представляет физическую исходящую поставку клиенту.
    Содержит отправляемые партии и генерирует отгрузочную документацию.
    """

    def __init__(
        self,
        order_id: str,
        items: List[Batch],
        carrier: str,
        destination: str
    ):
        if not items:
            raise ValueError("Shipment must contain at least one batch")
        self.order_id = order_id
        self.items = items
        self.carrier = carrier
        self.destination = destination
        self.tracking_number: str = ""
        self.shipment_date = datetime.now()
        self.status = "preparing"

    def generate_packing_slip(self) -> PackingSlip:
        """
        Создаёт упаковочный лист на основе партий в отгрузке.
        """
        slip_items = [
            (batch.product, batch.quantity) for batch in self.items
        ]
        return PackingSlip(shipment_id=self.order_id, items=slip_items)

    def create_label(self) -> ShippingLabel:
        """
        Генерирует транспортную этикетку с трек-номером и весом.
        """
        if not self.tracking_number:
            self.tracking_number = IdGenerator("TRACK").generate()
        total_weight = sum(
            batch.quantity * batch.product.spec.weight_kg for batch in self.items
        )
        return ShippingLabel(
            tracking_number=self.tracking_number,
            destination=self.destination,
            weight_kg=total_weight
        )

    def mark_as_shipped(self) -> None:
        """
        Отмечает отгрузку как отправленную.
        """
        self.status = "shipped"

    def get_total_weight(self) -> float:
        """
        Возвращает общий вес отгрузки в килограммах.
        """
        return sum(batch.quantity * batch.product.spec.weight_kg for batch in self.items)

    def get_item_count(self) -> int:
        """
        Возвращает количество уникальных товаров (по ID продукта) в отгрузке.
        """
        return len(set(batch.product.id for batch in self.items))