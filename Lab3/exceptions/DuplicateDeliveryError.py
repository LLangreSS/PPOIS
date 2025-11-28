class DuplicateDeliveryError(Exception):
    """Вызывается, когда предпринимается попытка получить поставку, которая уже была обработана."""

    def __init__(self, message: str, delivery_id: str = None):
        self.delivery_id = delivery_id
        super().__init__(message)

