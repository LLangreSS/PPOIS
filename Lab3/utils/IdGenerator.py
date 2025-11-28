class IdGenerator:
    """
    Генерирует уникальные идентификаторы с заданным префиксом.
    """

    _counters = {}

    def __init__(self, prefix: str):
        self.prefix = prefix
        if prefix not in IdGenerator._counters:
            IdGenerator._counters[prefix] = 0

    def generate(self) -> str:
        """
        Генерирует следующий уникальный идентификатор для префикса.
        """
        IdGenerator._counters[self.prefix] += 1
        number = IdGenerator._counters[self.prefix]
        return f"{self.prefix}-{number:04d}"

    @classmethod
    def reset_counter(cls, prefix: str = None) -> None:
        """
        Сбрасывает счетчик для префикса или всех префиксов.
        """
        if prefix is None:
            cls._counters.clear()
        elif prefix in cls._counters:
            cls._counters[prefix] = 0