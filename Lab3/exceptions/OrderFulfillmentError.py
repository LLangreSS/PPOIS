class OrderFulfillmentError(Exception):
    """Вызывается, когда заказ не может быть выполнен из-за ограничений по запасам или системе."""

    def __init__(self, message: str, order_id: str = None, product_id: str = None):
        self.order_id = order_id
        self.product_id = product_id
        super().__init__(message)

