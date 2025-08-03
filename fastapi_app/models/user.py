"""Модель пользователя."""

from typing import TYPE_CHECKING

from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.pk_mix import UUIDMixin
from fastapi_app.models.mixins.soft_delete import ActiveMixin

if TYPE_CHECKING:
    from fastapi_app.models.user_role import UserRole


class User(UUIDMixin, ActiveMixin, Base):
    """Модель пользователя с основной информацией и ролями."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
        index=True,
    )
    password: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    middle_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        default="",
    )

    roles: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete",
    )

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return (
            f"<User(id={self.id}, email={self.email!r}, "
            f"first_name={self.first_name!r}, last_name={self.last_name!r})>"
        )
