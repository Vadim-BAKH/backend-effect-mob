"""Репозиторий для работы с пользователями в базе данных."""

from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.models import User


class UserRepo:
    """Репозиторий для CRUD операций с пользователями."""

    def __init__(self, session: AsyncSession):
        """Инициализация сессии базы данных."""
        self.session = session

    async def get_by_email(self, email: EmailStr) -> User | None:
        """Получить активного пользователя по email."""
        stmt = select(User).where(
            User.email == email,
            User.is_active,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Получить активного пользователя по ID."""
        stmt = select(User).where(
            User.id == user_id,
            User.is_active,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: EmailStr) -> bool:
        """Проверить существование активного пользователя по email."""
        stmt = select(User.id).where(
            User.email == email,
            User.is_active,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def create(
        self,
        email: EmailStr,
        password: bytes,
        first_name: str,
        last_name: str,
        middle_name: str = "",
    ) -> User:
        """Создать нового пользователя с указанными данными."""
        user = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
