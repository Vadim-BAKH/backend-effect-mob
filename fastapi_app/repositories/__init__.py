"""Инициализация репозиториев."""

__all__ = [
    "UserRepo",
    "OrderRepo",
    "PermissionRepo",
    "RoleRepo",
    "ResourceRepo",
]

from fastapi_app.repositories.order_repo import OrderRepo
from fastapi_app.repositories.permission_repo import PermissionRepo
from fastapi_app.repositories.resource_repo import ResourceRepo
from fastapi_app.repositories.role_repo import RoleRepo
from fastapi_app.repositories.user_repo import UserRepo
