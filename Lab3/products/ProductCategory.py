class ProductCategory:
    """
    Иерархическая категория для товаров (например, 'Электроника > Телефоны').
    Поддерживает родительско-дочерние отношения для вложенной категоризации.
    """

    def __init__(self, id: str, name: str, parent: "ProductCategory" = None):
        self.id = id
        self.name = name
        self.parent = parent
        self.children = []

    def full_path(self) -> str:
        """
        Возвращает полный путь категории, например 'Электроника/Телефоны/Смартфоны'.
        """
        if self.parent is None:
            return self.name
        return f"{self.parent.full_path()}/{self.name}"

    def add_child(self, child_category: "ProductCategory") -> None:
        """Добавляет дочернюю категорию."""
        self.children.append(child_category)
        child_category.parent = self

    def get_all_products_count(self, product_registry) -> int:
        """Возвращает общее количество товаров во всех подкатегориях."""
        count = 0
        for product in product_registry:
            if product.category == self or self._is_ancestor_of(product.category):
                count += 1
        return count

    def _is_ancestor_of(self, category: "ProductCategory") -> bool:
        """Проверяет, является ли текущая категория предком указанной."""
        current = category
        while current is not None:
            if current == self:
                return True
            current = current.parent
        return False

