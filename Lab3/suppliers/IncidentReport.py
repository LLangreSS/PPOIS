from __future__ import annotations
from suppliers.Supplier import Supplier
from staff.Employee import Employee
from deliveries.Delivery import Delivery
from datetime import datetime

class IncidentReport:
    """
    Фиксирует инцидент по поставке: недостача, брак, задержка, повреждение.
    Служит основой для претензий и анализа качества поставщика.
    """
    def __init__(
        self,
        id: str,
        delivery: Delivery,
        supplier: Supplier,
        reporter: Employee,
        description: str,
        severity: str
    ):
        if severity not in {"low", "medium", "high"}:
            raise ValueError("Severity must be: low/medium/high")
        if not description.strip():
            raise ValueError("Incident description cannot be empty")
        self.id = id
        self.delivery = delivery
        self.supplier = supplier
        self.reporter = reporter
        self.description = description.strip()
        self.severity = severity
        self.reported_at = datetime.now()

    def is_critical(self) -> bool:
        """
        Проверяет, является ли инцидент критическим.
        """
        return self.severity == "high"