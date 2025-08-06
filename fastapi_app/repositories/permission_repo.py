"""Репозиторий для работы с правами."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from fastapi_app.exceptions import ResourceNotFound
from fastapi_app.models import (
    Permission,
    Resource,
    Role,
    RolePermission,
    UserRole,
)
from fastapi_app.schemas import PermissionCreate, PermissionOut


class PermissionRepo:
    """Репозиторий для CRUD операций с правами на действие."""

    def __init__(self, session):
        """Инициализация сессии базы данных."""
        self.session = session

    async def create(self, data: PermissionCreate) -> PermissionOut:
        """Создать право на действие."""
        stmt = select(Resource).where(Resource.name == data.resource)
        result = await self.session.execute(stmt)
        resource = result.scalar_one_or_none()
        if not resource:
            raise ResourceNotFound()

        permission = Permission(action=data.action, resource_id=resource.id)
        self.session.add(permission)
        await self.session.commit()
        await self.session.refresh(permission)
        return PermissionOut(
            id=permission.id,
            resource=data.resource,
            action=permission.action,
        )

    async def get_all(self) -> list[PermissionOut]:
        """Просмотреть все права на действие."""
        stmt = select(Permission).options(joinedload(Permission.resource))
        result = await self.session.execute(stmt)
        permissions = result.unique().scalars().all()

        return [
            PermissionOut(
                id=perm.id,
                action=perm.action,
                resource=perm.resource.name,
            )
            for perm in permissions
        ]

    async def delete(self, permission_id: UUID):
        """Удалить право на действие по ID."""
        await self.session.execute(
            delete(Permission).where(Permission.id == permission_id),
        )
        await self.session.commit()

    async def get_user_permissions(self, user_id: UUID) -> list[Permission]:
        """Получить права для пользователя по tuj ID."""
        stmt = (
            select(Permission)
            .join(RolePermission)
            .join(Role)
            .join(UserRole)
            .where(UserRole.user_id == user_id)
            .options(joinedload(Permission.resource))
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_by_action_and_resource(
        self,
        action: str,
        resource_name: str,
    ) -> Permission | None:
        """Получить право по действию и ресурсу."""
        stmt = (
            select(Permission)
            .options(joinedload(Permission.resource))
            .where(Permission.action == action, Resource.name == resource_name)
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()
