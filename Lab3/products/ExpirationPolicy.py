from datetime import datetime, timedelta

class ExpirationPolicy:
    """
    Определяет правила срока годности для скоропортящихся товаров.
    Используется для вычисления дат истечения срока на основе дат производства.
    """

    def __init__(self, shelf_life_days: int, requires_cold_chain: bool = False):
        self.shelf_life_days = shelf_life_days
        self.requires_cold_chain = requires_cold_chain

    def calculate_expiry(self, manufacture_date: datetime) -> datetime:
        """
        Вычисляет дату истечения срока на основе даты производства и срока годности.
        """
        return manufacture_date + timedelta(days=self.shelf_life_days)

    def is_near_expiry(self, expiry_date: datetime, days_threshold: int = 7) -> bool:
        """
        Проверяет, приближается ли срок годности.
        """
        now = datetime.now()
        time_until_expiry = expiry_date - now
        return time_until_expiry <= timedelta(days=days_threshold)

    def validate_storage_conditions(self, current_temperature: float) -> bool:
        """
        Проверяет, соответствуют ли условия хранения требованиям политики.
        """
        if self.requires_cold_chain:
            return current_temperature <= 8.0
        return True