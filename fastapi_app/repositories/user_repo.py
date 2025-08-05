"""Репозиторий для работы с пользователями в базе данных."""

from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select, update
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

    async def delete_by_id(self, user_id: UUID) -> None:
        """Soft delete: Деактивировать пользователя по ID."""
        stmt = (
            update(User)
            .where(User.id == user_id, User.is_active)
            .values(is_active=False)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_by_id(
        self,
        user_id: UUID,
        first_name: str | None = None,
        last_name: str | None = None,
        middle_name: str | None = None,
        email: str | None = None,
        password: bytes | None = None,
    ) -> User | None:
        """Обновить данные пользователя по ID. Возвращает обновлённого пользователя."""
        stmt = select(User).where(User.id == user_id, User.is_active)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if middle_name is not None:
            user.middle_name = middle_name
        if email is not None:
            user.email = email
        if password is not None:
            user.password = password

        await self.session.commit()
        await self.session.refresh(user)
        return user
