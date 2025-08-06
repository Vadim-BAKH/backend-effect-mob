"""Модуль сервиса работы с правами на действие."""

from fastapi_app.models import User
from fastapi_app.repositories import PermissionRepo


class PermissionService:
    """Сервис для управления логикой прав на действие."""

    def __init__(self, permission_repo: PermissionRepo):
        """Инициализация с репозиторием прав на действие."""
        self.permission_repo = permission_repo

    async def has_permission(
        self,
        user: User,
        resource: str,
        action: str,
    ) -> bool:
        """Проверяет, имеет ли пользователь разрешение на действие."""
        permissions = await self.permission_repo.get_user_permissions(user.id)
        for perm in permissions:
            if perm.resource.name == resource and perm.action == action:
                return True
        return False
