"""Схемы для ролей."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    """Модель создания роли."""

    name: str
    description: str | None = None


class RoleOut(RoleCreate):
    """Модель получения роли."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)
