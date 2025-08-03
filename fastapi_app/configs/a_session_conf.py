"""Настройки асинхронных движка и сессии."""

from uuid import uuid4

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastapi_app.configs.main_conf import settings

async_engine = create_async_engine(
    url=str(settings.db.url),
    echo=settings.db.echo,
    future=True,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    connect_args={
        "prepared_statement_name_func": lambda: f"__asyncpg_{uuid4()}__",
    },
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
