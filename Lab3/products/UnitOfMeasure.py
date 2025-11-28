class UnitOfMeasure:
    """
    Представляет единицу измерения количества товара,
    такую как 'штука', 'килограмм' или 'литр'.
    Поддерживает различие между дискретными и непрерывными единицами.
    """

    def __init__(self, symbol: str, name: str, is_discrete: bool = True):
        self.symbol = symbol
        self.name = name
        self.is_discrete = is_discrete

    def convert(self, quantity: float, target_unit: "UnitOfMeasure") -> float:
        """
        Конвертирует количество в целевую единицу измерения.
        В реальной системе здесь была бы логика конвертации.
        """
        if self == target_unit:
            return quantity
        if self.symbol == "kg" and target_unit.symbol == "g":
            return quantity * 1000
        elif self.symbol == "g" and target_unit.symbol == "kg":
            return quantity / 1000
        else:
            raise ValueError(f"Conversion from {self.symbol} to {target_unit.symbol} is not supported")

    def __eq__(self, other):
        return self.symbol == other.symbol and self.name == other.name