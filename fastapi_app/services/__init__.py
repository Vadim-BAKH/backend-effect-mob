"""Инициализация сервисов."""

__all__ = [
    "AuthService",
    "UserService",
    "OrderService",
    "PermissionService",
]
from fastapi_app.services.auth_service import AuthService
from fastapi_app.services.order_service import OrderService
from fastapi_app.services.permission import PermissionService
from fastapi_app.services.user_service import UserService
