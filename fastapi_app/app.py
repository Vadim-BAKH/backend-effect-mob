"""Приложение FastApi."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from fastapi_app.configs import async_engine, settings
from fastapi_app.exceptions import register_exception_handler


@asynccontextmanager
async def database_life_cycle(app: FastAPI) -> AsyncIterator:
    """
    Асинхронное соединение с базой движка.

    Устанавливает и закрывает соединение.
    """
    yield
    await async_engine.dispose()


app_ = FastAPI(
    lifespan=database_life_cycle,
    default_response_class=ORJSONResponse,
)

register_exception_handler(app_)


app_.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,  # разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],  # разрешённые HTTP методы
    # allow_headers=["*"],
    allow_headers=["Content-Type", "X-My-Fancy-Header"],
    expose_headers=["Content-Type", "X-Custom-Header"],
)
