class UnauthorizedOperationError(Exception):
    """Вызывается, когда сотрудник пытается выполнить действие, которое ему не разрешено."""

    def __init__(self, message: str, employee_id: str = None, operation: str = None):
        self.employee_id = employee_id
        self.operation = operation
        super().__init__(message)

