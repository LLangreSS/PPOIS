from __future__ import annotations
from typing import List, Optional
from products.ProductCategory import ProductCategory
from products.ProductSpecification import ProductSpecification
from products.Barcode import Barcode
from suppliers.Supplier import Supplier
from products.UnitOfMeasure import UnitOfMeasure
from products.ProductTag import ProductTag

class Product:
    """
    Представляет отдельный товар в системе склада.
    Инкапсулирует идентификацию, классификацию, физические свойства и информацию о поставщике.
    """

    def __init__(
        self,
        id: str,
        name: str,
        category: ProductCategory,
        spec: ProductSpecification,
        barcode: Barcode,
        supplier: Supplier,
        unit: UnitOfMeasure,
        tags: Optional[List[ProductTag]] = None
    ):
        self.id = id
        self.name = name
        self.category = category
        self.spec = spec
        self.barcode = barcode
        self.supplier = supplier
        self.unit = unit
        self.tags = tags or []
        self.is_active = True

    def is_hazardous(self) -> bool:
        """
        Определяет, классифицируется ли товар как опасный на основе его тегов.
        """
        return any(tag.name.lower() in ["hazardous"] for tag in self.tags)

    def requires_special_storage(self) -> bool:
        """
        Проверяет, требует ли товар специальных условий хранения.
        """
        return self.is_hazardous() or self.spec.is_fragile or self.spec.requires_temperature_control()

    def get_storage_requirements(self) -> List[str]:
        """
        Возвращает список требований к хранению товара.
        """
        requirements = []
        if self.is_hazardous():
            requirements.append("Hazardous materials")
        if self.spec.is_fragile:
            requirements.append("Fragile goods")
        if self.spec.requires_temperature_control():
            requirements.append("Temperature control")
        return requirements

    def validate_for_storage(self) -> bool:
        """
        Проверяет, готов ли товар к размещению на складе.
        """
        return (
            self.barcode.validate() and
            self.spec.weight_kg > 0 and
            all(dim > 0 for dim in self.spec.dimensions)
        )