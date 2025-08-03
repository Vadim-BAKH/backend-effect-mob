"""Модель ресурса."""

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.pk_mix import UUIDMixin

if TYPE_CHECKING:
    from fastapi_app.models.permission import Permission


class Resource(UUIDMixin, Base):
    """Модель ресурса, к которому привязываются разрешения."""

    __tablename__ = "resources"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        back_populates="resource",
    )

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return f"<Resource(id={self.id}, name={self.name!r})>"
