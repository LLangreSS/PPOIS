from __future__ import annotations
from datetime import datetime


class ShippingLabel:
    """
    Этикетка для внешней отгрузки, содержащая информацию для отслеживания и маршрутизации.
    Используется перевозчиками для доставки.
    """

    def __init__(self, tracking_number: str, destination: str, weight_kg: float):
        if weight_kg <= 0:
            raise ValueError("Weight must be positive")
        self.tracking_number = tracking_number
        self.destination = destination
        self.weight_kg = weight_kg
        self.created_date = datetime.now()

    def print(self) -> None:
        """
        Печатает человеко-читаемую этикетку для складского персонала.
        """
        print(f"[LABEL] TO: {self.destination} | TRACK: {self.tracking_number} | WT: {self.weight_kg}kg")

    def get_shipping_cost(self, rate_per_kg: float = 5.0) -> float:
        """
        Рассчитывает стоимость доставки на основе веса и тарифа за килограмм.
        """
        return self.weight_kg * rate_per_kg

    def is_international(self) -> bool:
        """
        Определяет, является ли доставка международной.
        Считает доставку в следующие города РФ внутренней: Moscow, Saint Petersburg, Novosibirsk, Yekaterinburg, Kazan.
        """
        domestic_cities = {"Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"}
        return self.destination not in domestic_cities