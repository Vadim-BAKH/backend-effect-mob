"""Модуль зависимостей FastAPI для работы с пользователями и авторизацией."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.database import get_session_db
from fastapi_app.models import User
from fastapi_app.repositories import UserRepo
from fastapi_app.services import AuthService
from fastapi_app.services.auth_service import oauth2_scheme

DBSessionDep = Annotated[AsyncSession, Depends(get_session_db)]


def get_user_repo(session: DBSessionDep) -> UserRepo:
    """Возвращает репозиторий пользователей сессии БД."""
    return UserRepo(session=session)


def get_auth_service(
    user_repo: Annotated[UserRepo, Depends(get_user_repo)],
) -> AuthService:
    """Создаёт сервис авторизации с репозиторием пользователей."""
    return AuthService(user_repo=user_repo)


async def validate_auth_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """Проверяет токен, возвращает активного пользователя."""
    payload = await auth_service.get_payload_from_token(token)
    user = await auth_service.get_auth_user(payload)
    return await auth_service.get_active_user(user)


CurrentUser = Annotated[User, Depends(validate_auth_user)]
