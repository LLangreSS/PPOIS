class IncompatibleStorageConditionError(Exception):
    """Вызывается, когда товар размещается в зоне хранения с неподходящими условиями."""

    def __init__(self, message: str, product_id: str = None, zone_id: str = None):
        self.product_id = product_id
        self.zone_id = zone_id
        super().__init__(message)

