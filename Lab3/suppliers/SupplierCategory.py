from __future__ import annotations
from typing import Set
from suppliers.Supplier import Supplier

class SupplierCategory:
    """
    Классифицирует поставщиков по типу: стратегический, тактический, резервный и т.д.
    Позволяет применять разные политики взаимодействия.
    """
    def __init__(self, name: str, description: str):
        if not name.strip():
            raise ValueError("Name cannot be empty")
        self.name = name.strip()
        self.description = description
        self.suppliers: Set[Supplier] = set()

    def add_supplier(self, supplier: Supplier) -> None:
        self.suppliers.add(supplier)

    def remove_supplier(self, supplier: Supplier) -> None:
        self.suppliers.discard(supplier)

    def get_supplier_ids(self) -> Set[str]:
        return {s.id for s in self.suppliers}