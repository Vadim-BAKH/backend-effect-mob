"""Модуль сервиса авторизации."""

import logging
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from fastapi_app.authentication.jwt_utils import decode_jwt
from fastapi_app.authentication.token_utils import (
    ensure_access_token_type,
    ensure_refresh_token_type,
)
from fastapi_app.exceptions import InvalidToken, UserInActive
from fastapi_app.models import User
from fastapi_app.repositories.user_repo import UserRepo

log = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/jwt/login/")


class AuthService:
    """Сервис авторизации и проверки JWT токенов."""

    def __init__(self, user_repo: UserRepo):
        """Инициализация с репозиторием пользователей."""
        self.user_repo = user_repo

    async def get_payload_from_token(self, token: str) -> dict[str, Any]:
        """Декодирует JWT токен и возвращает полезную нагрузку."""
        try:
            payload = decode_jwt(token=token)
            return payload
        except InvalidTokenError as err:
            log.warning("Получен недопустимый токен")
            raise InvalidToken() from err

    async def get_auth_user(self, payload: dict[str, Any]) -> User:
        """Получает пользователя по payload JWT, проверяет тип access-токена."""
        ensure_access_token_type(payload)
        user_id = payload.get("sub")
        if not user_id:
            log.warning("Access-токен не содержит поля 'sub'")
            raise InvalidToken()

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            log.warning("Пользователь с id %s не найден", user_id)
            raise InvalidToken()

        return user

    async def get_refresh_user(self, payload: dict[str, Any]) -> User:
        """Получает пользователя по payload JWT, проверяет тип refresh-токена."""
        ensure_refresh_token_type(payload)
        user_id = payload.get("sub")
        if not user_id:
            log.warning("Refresh-токен не содержит поля 'sub'")
            raise InvalidToken()

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            log.warning("Пользователь с id %s не найден", user_id)
            raise InvalidToken()

        return user

    async def get_active_user(self, user: User) -> User:
        """Проверяет активность пользователя."""
        if not user.is_active:
            log.warning("Пользователь %s неактивен", user.email)
            raise UserInActive()
        return user
