from __future__ import annotations
from typing import List
from staff.Permission import Permission

class Role:
    """
    Коллекция разрешений, назначенных сотрудникам.
    Используется для контроля доступа к складским операциям.
    """

    def __init__(self, name: str, permissions: List[Permission]):
        self.name = name
        self.permissions = permissions

    def has_permission(self, action: str, resource: str = None) -> bool:
        """
        Проверяет, есть ли у роли разрешение на указанное действие и ресурс.
        """
        if resource is None:
            return any(p.action == action for p in self.permissions)
        return any(p.matches(action, resource) for p in self.permissions)

    def add_permission(self, permission: Permission) -> None:
        """
        Добавляет разрешение в роль.
        """
        self.permissions.append(permission)

    def remove_permission(self, action: str, resource: str) -> bool:
        """
        Удаляет разрешение из роли.
        """
        for i, perm in enumerate(self.permissions):
            if perm.matches(action, resource):
                self.permissions.pop(i)
                return True
        return False