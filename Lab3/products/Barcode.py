import re

class Barcode:
    """
    Представляет штрих-код товара (например, EAN-13).
    Обеспечивает проверку корректности формата и определение типа.
    """

    def __init__(self, value: str):
        self.value = value

    def validate(self) -> bool:
        """
        Проверяет формат штрих-кода (например, 13-значный числовой для EAN-13).
        """
        return bool(re.fullmatch(r"\d{13}", self.value))

    def get_barcode_type(self) -> str:
        """
        Определяет тип штрих-кода на основе его длины и формата.
        """
        if len(self.value) == 13 and self.validate():
            return "EAN-13"
        elif len(self.value) == 8:
            return "EAN-8"
        elif len(self.value) == 12:
            return "UPC-A"
        else:
            return "Unknown format"

    def generate_image_data(self) -> str:
        """
        Генерирует упрощенные данные для визуализации штрих-кода.
        """
        return f"|| {self.value} ||"