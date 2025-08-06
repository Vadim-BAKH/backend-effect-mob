"""Модуль зависимостей FastAPI для работы с пользователями и авторизацией."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.authentication import validate_password
from fastapi_app.database import get_session_db
from fastapi_app.exceptions import NotRightEnough, UserUnauthorized
from fastapi_app.models import User
from fastapi_app.repositories import OrderRepo, PermissionRepo, UserRepo
from fastapi_app.services import AuthService, OrderService, PermissionService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/jwt/login/")

DBSessionDep = Annotated[
    AsyncSession,
    Depends(get_session_db),
]


def get_user_repo(session: DBSessionDep) -> UserRepo:
    """
    Зависимость получения репозитория пользователей.

    :param session: Сессия базы данных
    :return: Экземпляр UserRepo
    """
    return UserRepo(session=session)


def get_auth_service(
    user_repo: Annotated[UserRepo, Depends(get_user_repo)],
) -> AuthService:
    """
    Зависимость получения сервиса авторизации.

    :param user_repo: Репозиторий пользователей
    :return: Экземпляр AuthService
    """
    return AuthService(user_repo=user_repo)


def get_order_repo() -> OrderRepo:
    """
    Зависимость получения репозитория заказов.

    :return: Экземпляр OrderRepo.
    """
    return OrderRepo()


async def get_order_service(
    repo: OrderRepo = Depends(get_order_repo),
) -> OrderService:
    """
    Зависимость получения сервиса заказа.

    :param repo: Экземпляр OrderRepo.
    :return: Экземпляр OrderService.
    """
    return OrderService(repo=repo)


async def get_curr_active_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """
    Получение текущего активного пользователя из access-токена.

    :param token: JWT access токен
    :param auth_service: Сервис авторизации
    :return: Объект пользователя
    """
    return await auth_service.get_active_auth_user(token)


async def get_curr_refresh_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """
    Получение пользователя по refresh-токену.

    :param token: JWT refresh токен
    :param auth_service: Сервис авторизации
    :return: Объект пользователя
    """
    return await auth_service.get_current_refresh_user(token)


async def validate_auth_user(
    session: DBSessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> User:
    """
    Валидация пользователя по данным формы авторизации.

    Принимает OAuth2PasswordRequestForm (username/password),
    где username — это email.

    :param session: Сессия БД
    :param form_data: Данные из формы авторизации (OAuth2)
    :raises UserUnauthorized: Если пользователь не найден или пароль неверен
    :return: Объект пользователя
    """
    user_repo = UserRepo(session=session)
    user: User = await user_repo.get_by_email(
        email=form_data.username,
    )
    if not user or not validate_password(form_data.password, user.password):
        raise UserUnauthorized()

    return user


CurrentUser = Annotated[
    User,
    Depends(validate_auth_user),
]

CurrActiveUser = Annotated[
    User,
    Depends(get_curr_active_user),
]

CurrRefreshUser = Annotated[
    User,
    Depends(get_curr_refresh_user),
]


def check_permission(resource: str, action: str):
    """
    Создаёт зависимость для проверки разрешения пользователя на действие с ресурсом.

    :param resource: Имя ресурса, для которого проверяется разрешение.
    :param action: Действие, на которое проверяется разрешение.
    :return: Асинхронная функция зависимость для проверки прав.
    """

    async def _check_permission(
        user: CurrActiveUser,
        session: DBSessionDep,
    ) -> None:
        """
        Проверяет, имеет ли пользователь права на требуемое действие.

        :param user: Текущий активный пользователь.
        :param session: Асинхронная сессия базы данных.
        :raises NotRightEnough: Если прав недостаточно, выбрасывает исключение.
        :return: None при успешной проверке.
        """
        repo = PermissionRepo(session=session)
        service = PermissionService(permission_repo=repo)

        has_perm = await service.has_permission(user, resource, action)
        if not has_perm:
            raise NotRightEnough
        return None  # Внутренняя должна возвращать None

    return _check_permission  # Внешняя возвращает функцию
