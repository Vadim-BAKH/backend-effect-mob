"""Репозиторий для работы с ресурсами."""

from uuid import UUID

from sqlalchemy import delete, select

from fastapi_app.models import Resource
from fastapi_app.schemas import ResourceCreate, ResourceOut


class ResourceRepo:
    """Репозиторий для CRUD операций с ресурсами."""

    def __init__(self, session):
        """Инициализация сессии базы данных."""
        self.session = session

    async def create(self, data: ResourceCreate) -> ResourceOut:
        """Создание ресурса."""
        resource = Resource(**data.model_dump())
        self.session.add(resource)
        await self.session.commit()
        await self.session.refresh(resource)
        return ResourceOut.model_validate(resource)

    async def get_all(self) -> list[ResourceOut]:
        """Получить все ресурсы."""
        result = await self.session.execute(select(Resource))
        return [ResourceOut.model_validate(row) for row in result.scalars()]

    async def delete(self, resource_id: UUID):
        """Удалить ресурс по ID."""
        await self.session.execute(
            delete(Resource).where(Resource.id == resource_id),
        )
        await self.session.commit()
