from __future__ import annotations

class Cafeteria:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.menu: list[str] = []

    def add_dish(self, dish: str) -> None:
        self.menu.append(dish)

    def serve_meal(self, person) -> bool:
        return len(self.menu) > 0

    def restock(self, items: list[str]) -> None:
        self.menu.extend(items)
