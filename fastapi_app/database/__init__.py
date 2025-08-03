"""Инициализация сессии базы данных."""

__all__ = [
    "get_session_db",
]

from fastapi_app.database.async_generator import get_session_db
