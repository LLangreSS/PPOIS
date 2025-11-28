class SlotAllocationError(Exception):
    """Вызывается, когда система не может выделить физический или логический слот хранения."""

    def __init__(self, message: str, zone_id: str = None, product_id: str = None):
        self.zone_id = zone_id
        self.product_id = product_id
        super().__init__(message)

