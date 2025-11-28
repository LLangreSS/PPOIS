class Permission:
    """
    Представляет детальное разрешение на выполнение действия над ресурсом.
    Пример: действие='выполнить_заказ', ресурс='CustomerOrder'
    """

    def __init__(self, action: str, resource: str):
        self.action = action
        self.resource = resource

    def __str__(self) -> str:
        return f"{self.action}_{self.resource}"

    def matches(self, action: str, resource: str) -> bool:
        """Проверяет, соответствует ли разрешение заданному действию и ресурсу."""
        return self.action == action and self.resource == resource

