class StorageCondition:
    """
    Определяет требования к окружающей среде для хранения чувствительных товаров,
    такие как температурный диапазон и влажность.
    """

    def __init__(
        self,
        temp_min: float = -float('inf'),
        temp_max: float = float('inf'),
        humidity_max: float = 100.0,
        requires_ventilation: bool = False,
        light_sensitive: bool = False
    ):
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.humidity_max = humidity_max
        self.requires_ventilation = requires_ventilation
        self.light_sensitive = light_sensitive

    def satisfied_by(self, env_temp: float, env_humidity: float) -> bool:
        """
        Проверяет, удовлетворяют ли заданные условия окружающей среды требованиям хранения.
        """
        temp_ok = self.temp_min <= env_temp <= self.temp_max
        humidity_ok = env_humidity <= self.humidity_max
        return temp_ok and humidity_ok

    def get_condition_description(self) -> str:
        """
        Возвращает текстовое описание условий хранения.
        """
        conditions = []
        if self.temp_min > -float('inf') or self.temp_max < float('inf'):
            conditions.append(f"Temperature: {self.temp_min}°C - {self.temp_max}°C")
        if self.humidity_max < 100.0:
            conditions.append(f"Humidity: up to {self.humidity_max}%")
        if self.requires_ventilation:
            conditions.append("Ventilation required")
        if self.light_sensitive:
            conditions.append("Light sensitive")
        return "; ".join(conditions) if conditions else "Standard conditions"