"""Модуль сервиса авторизации."""

import logging
from typing import Any

from jwt.exceptions import InvalidTokenError

from fastapi_app.authentication.jwt_utils import decode_jwt
from fastapi_app.authentication.token_utils import (
    ensure_access_token_type,
    ensure_refresh_token_type,
)
from fastapi_app.exceptions import InvalidToken, UserInActive
from fastapi_app.models import User
from fastapi_app.repositories import UserRepo

log = logging.getLogger(__name__)


class AuthService:
    """Сервис авторизации и проверки JWT токенов."""

    def __init__(self, user_repo: UserRepo):
        """
        Инициализирует сервис авторизации.

        :param user_repo: Репозиторий пользователя
        """
        self.user_repo = user_repo

    async def get_current_token_payload(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Получает payload из JWT токена.

        :param token: JWT токен
        :raises InvalidToken: Если токен некорректен
        :return: Раскодированный payload токена
        """
        try:
            payload = decode_jwt(token=token)
        except InvalidTokenError as ite:
            log.warning("Получен недопустимый токен")
            raise InvalidToken() from ite
        return payload

    async def get_current_auth_user(self, token: str) -> User:
        """
        Получает пользователя по access-токену.

        :param token: Access JWT токен
        :raises InvalidToken: Если токен некорректен или пользователь не найден
        :return: Пользователь из БД
        """
        payload = await self.get_current_token_payload(token)
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

    async def get_current_refresh_user(self, token: str) -> User:
        """
        Получает пользователя по refresh-токену.

        :param token: Refresh JWT токен
        :raises InvalidToken: Если токен некорректен или пользователь не найден
        :return: Пользователь из БД
        """
        payload = await self.get_current_token_payload(token)
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

    async def get_active_auth_user(self, token: str) -> User:
        """
        Получает только активного пользователя по access-токену.

        :param token: Access JWT токен
        :raises InvalidToken: Если токен некорректен или пользователь не найден
        :raises UserInActive: Если пользователь не активен
        :return: Активный пользователь из БД
        """
        user = await self.get_current_auth_user(token)
        if not user.is_active:
            log.warning("Пользователь %s неактивен", user.email)
            raise UserInActive()
        return user
