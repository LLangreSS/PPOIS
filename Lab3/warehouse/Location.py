class Location:
    """
    Представляет физические координаты внутри склада,
    структурированные как (ряд, стеллаж, полка) в пределах зоны.
    """

    def __init__(self, row: str, rack: str, shelf: str, zone_id: str):
        self.row = row
        self.rack = rack
        self.shelf = shelf
        self.zone_id = zone_id

    def to_string(self) -> str:
        """
        Возвращает читаемый код местоположения, например 'A-12-B3'.
        """
        return f"{self.row}-{self.rack}-{self.shelf}"

    def is_in_zone(self, zone_id: str) -> bool:
        """
        Проверяет, находится ли местоположение в указанной зоне.
        """
        return self.zone_id == zone_id

    def get_adjacent_locations(self) -> list:
        """
        Возвращает список соседних местоположений (упрощенная реализация).
        """
        return [
            Location(self.row, str(int(self.rack) + 1), self.shelf, self.zone_id),
            Location(self.row, str(int(self.rack) - 1), self.shelf, self.zone_id),
        ]