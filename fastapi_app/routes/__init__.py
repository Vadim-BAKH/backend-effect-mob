"""Инициализация маршрутов."""

__all__ = [
    "auth_rout",
    "jwt_rout",
]
from fastapi_app.routes.auth import router as auth_rout
from fastapi_app.routes.jwt import router as jwt_rout
