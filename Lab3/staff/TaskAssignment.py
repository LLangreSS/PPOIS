from __future__ import annotations
from staff.Employee import Employee

class TaskAssignment:
    """
    Связывает конкретную задачу (например, передача, сборка) с сотрудником.
    Используется для отслеживания рабочей нагрузки и подотчетности.
    """

    def __init__(self, employee_id: str, task_id: str, task_type: str):
        if not task_type.strip():
            raise ValueError("Task type cannot be empty")
        self.employee_id = employee_id
        self.task_id = task_id
        self.task_type = task_type.strip()
        from datetime import datetime
        self.assigned_date = datetime.now()
        self.status = "assigned"

    def assign_to(self, employee: Employee) -> None:
        """
        Назначает задачу конкретному сотруднику.
        """
        if employee.id != self.employee_id:
            raise ValueError("Employee ID mismatch")
        self.status = "active"

    def complete(self) -> None:
        """
        Отмечает задачу как выполненную.
        """
        self.status = "completed"

    def get_assignment_info(self) -> dict:
        """
        Возвращает информацию о назначении задачи.
        """
        return {
            "employee_id": self.employee_id,
            "task_id": self.task_id,
            "task_type": self.task_type,
            "assigned_date": self.assigned_date,
            "status": self.status
        }