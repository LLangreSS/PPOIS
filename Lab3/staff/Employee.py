from __future__ import annotations
from staff.Role import Role
from staff.Shift import Shift

class Employee:
    """
    Представляет сотрудника склада с назначенной ролью и сменой.
    Контролирует доступ к операциям через ролевые разрешения.
    """

    def __init__(self, id: str, name: str, role: Role, shift: Shift):
        self.id = id
        self.name = name
        self.role = role
        self.shift = shift
        self.is_active = True

    def can_perform(self, task: str, resource: str = None) -> bool:
        """
        Проверяет, может ли сотрудник выполнить задачу в текущей смене.
        """
        if not self.shift.is_active():
            return False
        return self.role.has_permission(task, resource)

    def get_employee_info(self) -> dict:
        """
        Возвращает информацию о сотруднике.
        """
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.name,
            "shift_active": self.shift.is_active(),
            "status": "active" if self.is_active else "inactive"
        }

    def transfer_to_role(self, new_role: Role) -> None:
        """
        Переводит сотрудника на новую роль.
        """
        self.role = new_role