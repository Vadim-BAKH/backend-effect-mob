"""Модель создания токенов."""

from datetime import timedelta

from fastapi_app.authentication.jwt_utils import encode_jwt
from fastapi_app.configs import settings
from fastapi_app.models import User

TOKEN_TYPE_FIELD = "type"  # nosec
ACCESS_TOKEN_TYPE = "access"  # nosec
REFRESH_TOKEN_TYPE = "refresh"  # nosec


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    """Создаёт токены."""
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: User) -> str:
    """Создаёт access_token."""
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: User) -> str:
    """Создаёт refresh_token."""
    jwt_payload = {
        "sub": str(user.id),
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(
            days=settings.auth_jwt.refresh_token_expire_days,
        ),
    )
