"""Схемы для создания заказа."""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    """Модель создания заказа."""

    title: str = Field(..., max_length=255)
    description: Optional[str] = None


class OrderOut(BaseModel):
    """Модель представления заказа."""

    id: UUID
    title: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)
