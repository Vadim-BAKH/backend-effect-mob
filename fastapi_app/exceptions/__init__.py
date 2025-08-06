"""Инициализация исключений c базовым классом HTTPException."""

__all__ = [
    "register_exception_handler",
    "PasswordsDoNotMatch",
    "EmailExists",
    "NotAccessTokenType",
    "NotRefreshTokenType",
    "NoUserByThisId",
    "UserUnauthorized",
    "InvalidToken",
    "UserInActive",
    "UserNotFound",
    "NotRightEnough",
    "ResourceNotFound",
]

from fastapi_app.exceptions.detail_exc.bad_request import (
    EmailExists,
    PasswordsDoNotMatch,
)
from fastapi_app.exceptions.detail_exc.forbidden import (
    NotRightEnough,
    UserInActive,
)
from fastapi_app.exceptions.detail_exc.not_found import (
    NoUserByThisId,
    ResourceNotFound,
    UserNotFound,
)
from fastapi_app.exceptions.detail_exc.unauthorized import (
    InvalidToken,
    NotAccessTokenType,
    NotRefreshTokenType,
    UserUnauthorized,
)
from fastapi_app.exceptions.general_exc import register_exception_handler
