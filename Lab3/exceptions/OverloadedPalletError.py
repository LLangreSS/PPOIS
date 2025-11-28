class OverloadedPalletError(Exception):
    """Вызывается, когда операция может привести к превышению паллетом своей грузоподъемности."""

    def __init__(self, message: str, pallet_id: str = None, current_weight: float = None, max_weight: float = None):
        self.pallet_id = pallet_id
        self.current_weight = current_weight
        self.max_weight = max_weight
        super().__init__(message)

