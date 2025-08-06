"""Создание суперпользователя при запуске приложения."""

import asyncio
import logging

from sqlalchemy import and_, exists, select

from fastapi_app.configs import async_session, settings
from fastapi_app.models import RolePermission, UserRole
from fastapi_app.repositories import (
    PermissionRepo,
    ResourceRepo,
    RoleRepo,
    UserRepo,
)
from fastapi_app.schemas import (
    PermissionCreate,
    ResourceCreate,
    RoleCreate,
    UserCreate,
)
from fastapi_app.services import UserService

log = logging.getLogger(__name__)


async def create_superuser():
    """Создаёт суперпользователя с ролью и правами."""
    async with async_session() as session:
        # Репозитории
        user_repo = UserRepo(session)
        resource_repo = ResourceRepo(session)
        permission_repo = PermissionRepo(session)
        role_repo = RoleRepo(session)

        user_service = UserService(user_repo)

        # Создание суперпользователя
        user_data = UserCreate(
            email=settings.superuser.email,
            password=settings.superuser.password,
            password_confirm=settings.superuser.password,
            first_name=settings.superuser.first_name,
            last_name=settings.superuser.last_name,
        )

        user = await user_service.user_repo.get_by_email(user_data.email)
        if user:
            log.info("Суперпользователь уже существует: %s", user.email)
        else:
            user = await user_service.register_user(user_data)
            log.info("Суперпользователь создан: %s", user.email)

        # Создание ресурса
        resource = await resource_repo.get_by_name("superuser")
        if not resource:
            resource = await resource_repo.create(
                ResourceCreate(name="superuser"),
            )

        # Создание permission
        permission = await permission_repo.get_by_action_and_resource(
            "main",
            resource.name,
        )
        if not permission:
            permission = await permission_repo.create(
                PermissionCreate(resource=resource.name, action="main"),
            )

        # Создание роли
        role = await role_repo.get_by_name("superuser")
        if not role:
            role = await role_repo.create(RoleCreate(name="superuser"))

            # Привязать permission к роли
            session.add(
                RolePermission(role_id=role.id, permission_id=permission.id),
            )
            await session.commit()

        # Назначение роли пользователю
        existing = await session.scalar(
            select(
                exists().where(
                    and_(
                        UserRole.user_id == user.id,
                        UserRole.role_id == role.id,
                    ),
                ),
            ),
        )
        if not existing:
            session.add(UserRole(user_id=user.id, role_id=role.id))
            await session.commit()
            log.info("Роль superuser назначена пользователю %s", user.email)
        else:
            log.info(
                "Роль superuser уже назначена пользователю %s",
                user.email,
            )


if __name__ == "__main__":
    asyncio.run(create_superuser())
