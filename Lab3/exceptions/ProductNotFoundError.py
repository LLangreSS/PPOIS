class ProductNotFoundError(Exception):
    """Вызывается, когда товар с указанным идентификатором не существует в системе."""

    def __init__(self, message: str, product_id: str = None):
        self.product_id = product_id
        super().__init__(message)

