"""Роутер для регистрации пользователей и аутентификации."""

from fastapi import APIRouter, Body, status

from fastapi_app.dependencies import (
    CurrActiveUser,
    DBSessionDep,
    get_user_repo,
)
from fastapi_app.schemas import (
    UserCreate,
    UserOut,
    UserUpdate,
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
    user_repo = get_user_repo(session=session)
    user_service = UserService(user_repo=user_repo)
    user = await user_service.register_user(user_in=user_in)
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


@router.patch(
    "/users/me",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
async def update_current_user(
    user: CurrActiveUser,
    session: DBSessionDep,
    user_update: UserUpdate = Body(...),
):
    """
    Обновление информации о текущем пользователе.

    Поля, которые не переданы — не изменятся.
    """
    user_repo = get_user_repo(session=session)
    user_service = UserService(user_repo=user_repo)
    updated_user = await user_service.update_user_by_id(
        user_id=user.id,
        user_update=user_update,
    )
    return UserOut.model_validate(updated_user)


@router.delete(
    "/users/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_current_user(
    user: CurrActiveUser,
    session: DBSessionDep,
):
    """
    Удаление (деактивация) текущего пользователя.

    Требуется access-токен.
    """
    user_repo = get_user_repo(session=session)
    user_service = UserService(user_repo=user_repo)
    await user_service.delete_user_by_id(user_id=user.id)
