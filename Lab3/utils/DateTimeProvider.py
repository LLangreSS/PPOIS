from datetime import datetime

class DateTimeProvider:
    """
    Абстрагирует доступ ко времени для обеспечения детерминированного тестирования.
    Продакшен-реализация возвращает реальное время.
    """

    def now(self) -> datetime:
        return datetime.now()

    def today(self) -> datetime:
        return datetime.today()

    def is_weekend(self) -> bool:
        """Проверяет, является ли текущий день выходным."""
        today = self.today()
        return today.weekday() >= 5

