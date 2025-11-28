class Manufacturer:
    """
    Представляет производителя товара.
    Включает базовую информацию об идентификации и происхождении.
    """

    def __init__(self, id: str, name: str, country: str, quality_rating: float = 5.0):
        self.id = id
        self.name = name
        self.country = country
        self.quality_rating = quality_rating

    def is_european(self) -> bool:
        """
        Проверяет, является ли производитель европейским.
        """
        eu_countries = ["Germany", "France", "Italy", "Spain", "Poland"]
        return self.country in eu_countries

    def update_quality_rating(self, new_rating: float) -> None:
        """
        Обновляет рейтинг качества производителя.
        """
        if 0 <= new_rating <= 10:
            self.quality_rating = new_rating
        else:
            raise ValueError("Rating must be between 0 and 10")