"""Сериализатор пользователя."""

from typing import Annotated, Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    model_validator,
)

from fastapi_app.exceptions import PasswordsDoNotMatch


class UserBase(BaseModel):
    """Базовая модель пользователя."""

    first_name: Annotated[
        str,
        Field(description="Имя", max_length=255),
    ]

    last_name: Annotated[
        str,
        Field(description="Имя", max_length=255),
    ]
    middle_name: Optional[
        Annotated[
            str,
            Field(description="Имя", max_length=255),
        ]
    ] = ""
    email: EmailStr


class UserCreate(UserBase):
    """Создание пользователя с паролем."""

    password: Annotated[
        SecretStr,
        Field(description="Пароль", min_length=8),
    ]
    password_confirm: Annotated[
        SecretStr,
        Field(description="Пароль", min_length=8),
    ]

    @model_validator(mode="after")
    def passwords_match(cls, model):
        """Проверяет валидность второго пароля с первым."""
        if (
            model.password.get_secret_value()
            != model.password_confirm.get_secret_value()
        ):
            raise PasswordsDoNotMatch()
        return model


class UserUpdate(BaseModel):
    """Обновление пользователя."""

    first_name: Annotated[
        Optional[str],
        Field(max_length=255, description="Имя"),
    ] = None
    last_name: Annotated[
        Optional[str],
        Field(max_length=255, description="Фамилия"),
    ] = None
    middle_name: Annotated[
        Optional[str],
        Field(max_length=255, description="Отчество"),
    ] = None
    email: Annotated[
        Optional[EmailStr],
        Field(description="Email"),
    ] = None
    password: Annotated[
        Optional[SecretStr],
        Field(min_length=8, description="Новый пароль"),
    ] = None


class UserOut(UserBase):
    """Ответ при получении пользователя."""

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    is_active: bool
