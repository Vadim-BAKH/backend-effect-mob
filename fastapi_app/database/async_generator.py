"""Генератор асинхронной сессии."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.configs import async_session


async def get_session_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессий базы данных.

    Создания и предоставления асинхронной сессии в контексте.
    :return:Асинхронный генератор, выдающий объект AsyncSession.
    """
    async with async_session() as session:
        yield session
