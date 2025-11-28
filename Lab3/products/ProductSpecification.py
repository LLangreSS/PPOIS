from typing import Tuple

class ProductSpecification:
    """
    Инкапсулирует физические и эксплуатационные характеристики товара,
    такие как размеры, вес и хрупкость.
    Используется для определения совместимости хранения и транспортировки.
    """

    def __init__(
        self,
        dimensions: Tuple[float, float, float],
        weight_kg: float,
        is_fragile: bool = False,
        storage_notes: str = "",
        min_temperature: float = None,
        max_temperature: float = None
    ):
        self.dimensions = dimensions
        self.weight_kg = weight_kg
        self.is_fragile = is_fragile
        self.storage_notes = storage_notes
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature

    def fits_in(self, pallet) -> bool:
        """
        Проверяет, можно ли разместить этот товар на заданном паллете
        на основе размерных и весовых ограничений.
        """
        max_l, max_w, _ = pallet.max_dimensions
        prod_l, prod_w, _ = self.dimensions
        if prod_l > max_l or prod_w > max_w:
            return False
        if self.weight_kg > pallet.remaining_capacity_kg:
            return False
        return True

    def volume(self) -> float:
        """Вычисляет объем товара в кубических метрах."""
        l, w, h = self.dimensions
        return l * w * h

    def requires_temperature_control(self) -> bool:
        """Проверяет, требуется ли температурный контроль."""
        return self.min_temperature is not None or self.max_temperature is not None

    def get_temperature_range(self) -> Tuple[float, float]:
        """Возвращает допустимый температурный диапазон."""
        return (self.min_temperature or -float('inf'), self.max_temperature or float('inf'))

