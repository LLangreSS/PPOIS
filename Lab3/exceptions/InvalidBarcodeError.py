class InvalidBarcodeError(Exception):
    """Вызывается, когда штрих-код не проходит проверку формата или контрольной суммы."""

    def __init__(self, message: str, barcode_value: str = None):
        self.barcode_value = barcode_value
        super().__init__(message)

