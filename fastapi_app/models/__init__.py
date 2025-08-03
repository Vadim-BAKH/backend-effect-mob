"""Инициализация моделей."""

__all__ = [
    "Base",
    "User",
    "Role",
    "Permission",
    "RolePermission",
    "Resource",
    "UserRole",
    "UUIDMixin",
    "ActiveMixin",
]

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.pk_mix import UUIDMixin
from fastapi_app.models.mixins.soft_delete import ActiveMixin
from fastapi_app.models.permission import Permission
from fastapi_app.models.resource import Resource
from fastapi_app.models.role import Role
from fastapi_app.models.role_permission import RolePermission
from fastapi_app.models.user import User
from fastapi_app.models.user_role import UserRole
