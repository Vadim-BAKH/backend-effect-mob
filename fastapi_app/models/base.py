"""Базовая модель."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для декларативных моделей SQLAlchemy."""

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return f"<{self.__class__.__name__}()>"
