"""Модели обработки исключений 'HTTP_404_NOT_FOUND'."""

from fastapi import HTTPException, status


class NoUserByThisId(HTTPException):
    """Модель исключения 'NoUserByThisId'."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user by user-ID.",
        )
