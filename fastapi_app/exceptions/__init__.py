"""Инициализация исключений c базовым классом HTTPException."""

__all__ = [
    "register_exception_handler",
    "PasswordsDoNotMatch",
    "EmailExists",
]


from fastapi_app.exceptions.detail_exc.bad_request import (
    EmailExists,
    PasswordsDoNotMatch,
)
from fastapi_app.exceptions.general_exc import register_exception_handler
