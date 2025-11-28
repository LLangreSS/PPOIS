class ExpiredProductError(Exception):
    """Вызывается, когда предпринимается попытка использовать или отгрузить просроченную партию товара."""

    def __init__(self, message: str, batch_id: str = None, expiry_date: str = None):
        self.batch_id = batch_id
        self.expiry_date = expiry_date
        super().__init__(message)

