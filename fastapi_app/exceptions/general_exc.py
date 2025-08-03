"""Регистрация исключений."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError, IntegrityError, OperationalError

from fastapi_app.exceptions.base.base_api_exc import BaseApiException

log = logging.getLogger(__name__)


def register_exception_handler(app: FastAPI) -> None:
    """Регистрирует общие исключения."""

    @app.exception_handler(BaseApiException)
    async def handle_base_api_exception(
        request: Request,
        exc: BaseApiException,
    ) -> ORJSONResponse:
        """Обработка кастомных API исключений."""
        log.warning(
            "API Exception: %s - %s",
            exc.code,
            exc.message,
        )
        return ORJSONResponse(
            status_code=exc.status_code,
            content={"code": exc.code, "message": exc.message},
        )

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> ORJSONResponse:
        """Обработка ошибок валидации запросов FastAPI."""
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Request data is not correct",
                "errors": exc.errors(),
            },
        )

    @app.exception_handler(ValidationError)
    async def handle_pydantic_validation_error(
        request: Request,
        exc: ValidationError,
    ) -> ORJSONResponse:
        """Обработка ошибок валидации Pydantic моделей."""
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Data validation error",
                "errors": exc.errors(),
            },
        )

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(
        request: Request,
        exc: IntegrityError,
    ) -> ORJSONResponse:
        """Обработка ошибок ограничений базы данных."""
        log.error("Database integrity error", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Database integrity error",
                "error": str(exc.orig) if exc.orig else str(exc),
            },
        )

    @app.exception_handler(OperationalError)
    async def handle_operational_error(
        request: Request,
        exc: OperationalError,
    ) -> ORJSONResponse:
        """Обработка ошибки подключения, таймаута."""
        log.error("Database operational error", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Database operational error",
            },
        )

    @app.exception_handler(DatabaseError)
    async def handle_database_error(
        request: Request,
        exc: DatabaseError,
    ) -> ORJSONResponse:
        """Обрабатывает общий класс ошибок базы."""
        log.error("Unhandled database error", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected database error has occurred",
            },
        )

    @app.exception_handler(Exception)
    async def handle_generic_exception(
        request: Request,
        exc: Exception,
    ) -> ORJSONResponse:
        """Перехватывает все необработанные исключения."""
        log.error("Unhandled exception", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
