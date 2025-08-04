"""Инициализация сервисов."""

__all__ = [
    "AuthService",
    "UserService",
]
from fastapi_app.services.auth_service import AuthService
from fastapi_app.services.user_service import UserService
