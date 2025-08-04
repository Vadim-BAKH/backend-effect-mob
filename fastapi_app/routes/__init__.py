"""Инициализация маршрутов."""

__all__ = ["auth_rout"]
from fastapi_app.routes.auth import router as auth_rout
