class InsufficientStockError(Exception):
    """Вызывается, когда операция запрашивает большее количество товара, чем доступно на складе."""

    def __init__(self, message: str, product_id: str = None, available: int = None, requested: int = None):
        self.product_id = product_id
        self.available = available
        self.requested = requested
        super().__init__(message)

