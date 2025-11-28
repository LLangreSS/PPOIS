class ProductTag:
    """
    Простой тег, прикрепленный к товару для фильтрации или инструкций по обращению.
    Примеры: 'хрупкий', 'опасный', 'акция'.
    """

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    def is_handling_instruction(self) -> bool:
        """
        Проверяет, является ли тег инструкцией по обращению.
        """
        handling_tags = ["fragile", "hazardous", "temperature", "humidity"]
        return self.name.lower() in handling_tags

    def get_color_code(self) -> str:
        """
        Возвращает цветовой код для визуального отображения тега.
        """
        color_map = {
            "hazardous": "red",
            "fragile": "orange",
            "promo": "green",
            "new": "blue"
        }
        return color_map.get(self.name.lower(), "gray")