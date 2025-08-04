"""Модели обработки исключений 'HTTP_403_FORBIDDEN'."""

from fastapi import HTTPException, status


class UserInActive(HTTPException):
    """Модель исключения 'UserIsNotActive'."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive",
        )
