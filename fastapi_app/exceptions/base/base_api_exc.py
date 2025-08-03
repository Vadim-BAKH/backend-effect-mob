"""Базовая модель API исключения."""

from typing import Optional, Union

from fastapi import HTTPException, status


class BaseApiException(HTTPException):
    """
    Базовое API исключение с кодом ошибки и сообщением.

    Атрибуты:
        code: машинно-читаемый код ошибки;
        message: читаемое сообщение для пользователя;
        status_code: HTTP статус ошибки.
    """

    code: str = ("base_api_exception",)
    message: Optional[Union[str]] = "Base API Exception"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message: Optional[Union[str, Exception]] = None,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        """
        Инициализация исключения.

        Аргументы:
            message: дополнительное сообщение (строка или исключение);
            code: код ошибки, если нужно переопределить;
            status_code: HTTP-статус, если нужно переопределить.
        """
        if message is not None:
            if isinstance(message, Exception):
                self.message = str(message)
            else:
                self.message = message
        if code is not None:
            self.code = code
        if status_code is not None:
            self.status_code = status_code
        super().__init__(
            status_code=status_code,
            detail={
                "code": self.code,
                "message": self.message,
            },
        )

    @classmethod
    def generate_openapi(cls) -> dict:
        """
        Генерация описания исключения для OpenAPI.

        Возвращает словарь с примером ошибки.
        """
        return {
            cls.status_code: {
                "description": cls.message,
                "content": {
                    "application/json": {
                        "example": {
                            "code": cls.code,
                            "message": cls.message,
                        },
                    },
                },
            },
        }
