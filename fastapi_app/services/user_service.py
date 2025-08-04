"""Модуль сервиса работы с пользователями."""

from fastapi_app.authentication import hash_password
from fastapi_app.exceptions import EmailExists
from fastapi_app.models import User
from fastapi_app.repositories import UserRepo
from fastapi_app.schemas.user import UserCreate


class UserService:
    """Сервис для управления логикой пользователей."""

    def __init__(self, user_repo: UserRepo):
        """Инициализация с репозиторием пользователей."""
        self.user_repo = user_repo

    async def register_user(self, user_in: UserCreate) -> User:
        """Регистрация нового пользователя с хешированием пароля."""
        if await self.user_repo.exists_by_email(user_in.email):
            raise EmailExists()
        hashed_password = hash_password(user_in.password.get_secret_value())
        user = await self.user_repo.create(
            email=user_in.email,
            password=hashed_password,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            middle_name=user_in.middle_name,
        )
        return user
