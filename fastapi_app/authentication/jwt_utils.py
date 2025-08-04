"""Утилиты JWT-токена и хеширования паролей."""

import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from fastapi_app.configs import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    """Генерирует JWT-токен с заданным содержимым и временем жизни."""
    now = datetime.now(tz=timezone.utc)
    expire = now + (
        expire_timedelta
        or timedelta(
            minutes=expire_minutes,
        )
    )

    to_encode = payload.copy()
    to_encode.update(
        {
            "exp": expire,
            "iat": now,
            "jti": str(uuid.uuid4()),
        },
    )

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """Декодирует и проверяет JWT-токен с помощью публичного ключа."""
    return jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )


def hash_password(password: str) -> bytes:
    """Хеширует пароль с использованием bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    """Проверяет, соответствует ли пароль хешу."""
    return bcrypt.checkpw(
        password.encode(),
        hashed_password,
    )
