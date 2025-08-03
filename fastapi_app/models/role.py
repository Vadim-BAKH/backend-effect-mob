"""Модель роли."""

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.pk_mix import UUIDMixin

if TYPE_CHECKING:
    from fastapi_app.models.role_permission import RolePermission
    from fastapi_app.models.user_role import UserRole


class Role(UUIDMixin, Base):
    """Модель роли, объединяющая пользователей и разрешения."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    users: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="role",
        cascade="all, delete",
    )
    permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete",
    )

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return f"<Role(id={self.id}, name={self.name!r})>"
