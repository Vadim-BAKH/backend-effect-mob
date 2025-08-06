"""Инициализация маршрутов."""

__all__ = [
    "auth_rout",
    "jwt_rout",
    "order_rout",
    "admin_rout",
]
from fastapi_app.routes.admin import router as admin_rout
from fastapi_app.routes.auth import router as auth_rout
from fastapi_app.routes.jwt import router as jwt_rout
from fastapi_app.routes.order import router as order_rout
