from __future__ import annotations
from typing import List
from staff.Employee import Employee
from warehouse.InternalTransfer import InternalTransfer
from exceptions.UnauthorizedOperationError import UnauthorizedOperationError

class WarehouseOperator:
    """
    Ролевой интерфейс для сотрудников, выполняющих складские операции.
    Обеспечивает соблюдение разрешений перед выполнением чувствительных действий.
    """

    def __init__(self, employee: Employee):
        if not employee.role.name.lower().endswith("operator"):
            raise UnauthorizedOperationError("Employee is not a warehouse operator")
        self.employee = employee

    def execute_transfer(self, transfer: InternalTransfer) -> None:
        """
        Выполняет внутреннюю передачу товаров с проверкой разрешений.
        """
        if not self.employee.can_perform("execute_transfer"):
            raise UnauthorizedOperationError(
                f"Operator {self.employee.id} does not have permission to execute transfers"
            )
        transfer.status = "executed_by_operator"

    def can_handle_hazardous(self) -> bool:
        """
        Проверяет, может ли оператор работать с опасными материалами.
        """
        return self.employee.can_perform("handle_hazardous")

    def get_operator_certifications(self) -> List[str]:
        """
        Возвращает список сертификатов оператора.
        """
        certifications = ["basic_training"]
        if self.can_handle_hazardous():
            certifications.append("hazardous_materials")
        if self.employee.can_perform("operate_forklift"):
            certifications.append("forklift")
        return certifications