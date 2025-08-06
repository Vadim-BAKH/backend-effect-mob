"""Схемы для ресурса."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ResourceCreate(BaseModel):
    """Модель создания ресурса."""

    name: str
    description: str | None = None


class ResourceOut(ResourceCreate):
    """Модель просмотра ресурса."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)
