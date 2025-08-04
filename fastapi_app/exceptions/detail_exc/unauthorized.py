"""Модели обработки исключений 'HTTP_401_UNAUTHORIZED'."""

from fastapi import HTTPException, status


class UserUnauthorized(HTTPException):
    """Модель исключения 'UserUnauthorized'."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


class InvalidToken(HTTPException):
    """Модель исключения InvalidToken."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error.",
        )


class NotAccessTokenType(HTTPException):
    """Модель исключения NotAccessTokenTipe."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type. Expected access",
        )


class NotRefreshTokenType(HTTPException):
    """Модель исключения NotRefreshTokenType."""

    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid token type. Expected refresh token.",
        )
