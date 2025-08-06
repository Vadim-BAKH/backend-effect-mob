"""Роутер для управления ролями, правами, ресурсами."""

from uuid import UUID

from fastapi import APIRouter, Depends, status

from fastapi_app.dependencies import DBSessionDep, check_permission
from fastapi_app.models import RolePermission, UserRole
from fastapi_app.repositories import (
    PermissionRepo,
    ResourceRepo,
    RoleRepo,
)
from fastapi_app.schemas import (
    PermissionCreate,
    PermissionOut,
    ResourceCreate,
    ResourceOut,
    RoleCreate,
    RoleOut,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post(
    "/roles",
    response_model=RoleOut,
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_201_CREATED,
)
async def create_role(data: RoleCreate, session: DBSessionDep):
    """Создание новой роли."""
    return await RoleRepo(session=session).create(data=data)


@router.get(
    "/roles",
    response_model=list[RoleOut],
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_200_OK,
)
async def get_roles(session: DBSessionDep):
    """Получение списка ролей."""
    return await RoleRepo(session=session).get_all()


@router.delete(
    "/roles/{role_id}",
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_role(role_id: UUID, session: DBSessionDep):
    """Удаление роли по ID."""
    await RoleRepo(session=session).delete(role_id=role_id)
    return {"detail": "Role deleted"}


@router.post(
    "/resources",
    response_model=ResourceOut,
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_201_CREATED,
)
async def create_resource(
    data: ResourceCreate,
    session: DBSessionDep,
):
    """Создание ресурса."""
    return await ResourceRepo(session=session).create(data=data)


@router.get(
    "/resources",
    response_model=list[ResourceOut],
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_200_OK,
)
async def get_resources(session: DBSessionDep):
    """Получение списка ресурсов."""
    return await ResourceRepo(session=session).get_all()


@router.delete(
    "/resources/{resource_id}",
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resource(
    resource_id: UUID,
    session: DBSessionDep,
):
    """Удаление ресурса по ID."""
    await ResourceRepo(session=session).delete(resource_id=resource_id)


# --- Permission ---
@router.post(
    "/permissions",
    response_model=PermissionOut,
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_201_CREATED,
)
async def create_permission(
    data: PermissionCreate,
    session: DBSessionDep,
):
    """создание разрешения."""
    return await PermissionRepo(session=session).create(data=data)


@router.get(
    "/permissions",
    response_model=list[PermissionOut],
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_200_OK,
)
async def get_permissions(session: DBSessionDep):
    """Получение списка разрешений."""
    return await PermissionRepo(session=session).get_all()


@router.delete(
    "/permissions/{permission_id}",
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_permission(permission_id: UUID, session: DBSessionDep):
    """Удаление разрешения по ID."""
    await PermissionRepo(session=session).delete(permission_id=permission_id)


@router.post(
    "/assign",
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def assign_permission_to_role(
    role_id: UUID,
    permission_id: UUID,
    session: DBSessionDep,
):
    """Назначение разрешения роли."""
    rp = RolePermission(role_id=role_id, permission_id=permission_id)
    session.add(rp)
    await session.commit()
    return {"detail": "Permission assigned to role"}


@router.post(
    "/assign-role",
    dependencies=[
        Depends(check_permission("superuser", "main")),
    ],
    status_code=status.HTTP_201_CREATED,
)
async def assign_role_to_user(
    user_id: UUID,
    role_id: UUID,
    session: DBSessionDep,
):
    """Назначение роли пользователю."""
    ur = UserRole(user_id=user_id, role_id=role_id)
    session.add(ur)
    await session.commit()
    return {"detail": "Role assigned to user"}
