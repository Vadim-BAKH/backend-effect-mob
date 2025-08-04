"""Роутер для регистрации пользователей и аутентификации."""

from fastapi import APIRouter, status

from fastapi_app.dependencies import DBSessionDep, get_user_repo
from fastapi_app.schemas.user import UserCreate, UserOut
from fastapi_app.services.user_service import UserService

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
