"""Мягкое удаление модели."""

from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column


class ActiveMixin:
    """Миксин для мягкой деактивации (soft delete) через is_active."""

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    def deactivate(self):
        """Отключить объект (soft delete)."""
        self.is_active = False

    def activate(self):
        """Активировать объект."""
        self.is_active = True
