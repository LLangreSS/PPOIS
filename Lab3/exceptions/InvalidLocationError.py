class InvalidLocationError(Exception):
    """Вызывается, когда код местоположения неправильно сформирован или не существует на складе."""

    def __init__(self, message: str, location_code: str = None):
        self.location_code = location_code
        super().__init__(message)

