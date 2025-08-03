"""Схема токена."""

from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from fastapi_app.schemas.user import UserOut


class TokenInfo(BaseModel):
    """Моделирует токен."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int


class TokenPayload(BaseModel):
    """Представление токена."""

    sub: PG_UUID
    exp: int
    type: str  # "access" or "refresh"


class LoginRequest(BaseModel):
    """Модель запроса при авторизации."""

    email: EmailStr
    password: SecretStr


class LoginResponse(TokenInfo):
    """Модель ответа при авторизации."""

    user: UserOut

    model_config = ConfigDict(from_attributes=True)
