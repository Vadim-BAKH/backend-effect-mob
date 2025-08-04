"""Роутер для регистрации пользователей и аутентификации."""

from fastapi import APIRouter, status

from fastapi_app.dependencies import (
    CurrActiveUser,
    DBSessionDep,
    get_user_repo,
)
from fastapi_app.schemas import (
    UserCreate,
    UserOut,
)
from fastapi_app.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: UserCreate,
    session: DBSessionDep,
):
    """Регистрация нового пользователя."""
    user_repo = get_user_repo(session)
    user_service = UserService(user_repo)
    user = await user_service.register_user(user_in)
    return user


@router.get(
    "/users/me",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
async def get_auth_user_self_info(
    user: CurrActiveUser,
) -> UserOut:
    """
    Возвращает информацию о текущем авторизованном пользователе.

    Требуется валидный JWT-токен.
    """
    return UserOut.model_validate(user)
