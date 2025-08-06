"""Схемы для прав доступа к ресурсам."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PermissionCreate(BaseModel):
    """Модель создания права."""

    resource: str  # по имени ресурса
    action: str


class PermissionOut(PermissionCreate):
    """Модель представления права."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)
