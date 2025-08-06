"""Репозиторий для работы с ролями."""

from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.models import Role
from fastapi_app.schemas import RoleCreate


class RoleRepo:
    """Репозиторий для CRUD операций с ролями."""

    def __init__(self, session: AsyncSession):
        """Инициализация сессии базы данных."""
        self.session = session

    async def create(self, data: RoleCreate) -> Role:
        """Создание роли."""
        role = Role(name=data.name, description=data.description)
        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)
        return role

    async def get_all(self) -> Sequence[Role]:
        """Получение ролей."""
        stmt = select(Role)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete(self, role_id: UUID) -> None:
        """Удаление роли по ID."""
        role = await self.session.get(Role, role_id)
        if role:
            await self.session.delete(role)
            await self.session.commit()
