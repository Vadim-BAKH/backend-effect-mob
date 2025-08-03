"""Модель разрешения."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.pk_mix import UUIDMixin

if TYPE_CHECKING:
    from fastapi_app.models.resource import Resource
    from fastapi_app.models.role_permission import RolePermission


class Permission(UUIDMixin, Base):
    """Модель разрешения, связывает действие и ресурс."""

    __tablename__ = "permissions"

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    resource_id: Mapped[PG_UUID] = mapped_column(
        ForeignKey("resources.id"),
    )

    resource: Mapped["Resource"] = relationship(
        "Resource",
        back_populates="permissions",
    )
    roles: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="permission",
    )

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return (
            f"<Permission(id={self.id}, action={self.action!r}, "
            f"resource_id={self.resource_id})>"
        )
