"""Роутер для управления Моковыми заявками."""

from uuid import UUID

from fastapi import APIRouter, Depends, status

from fastapi_app.dependencies import check_permission, get_order_service
from fastapi_app.schemas import OrderCreate, OrderOut
from fastapi_app.services import OrderService

router = APIRouter(prefix="/orders", tags=["Order"])


@router.get(
    "/",
    response_model=list[OrderOut],
    status_code=status.HTTP_200_OK,
)
async def list_orders(
    _: None = Depends(check_permission("orders", "read")),
    service: OrderService = Depends(get_order_service),
):
    """Получение списка заявок."""
    return await service.list_orders()


@router.post(
    "/",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order: OrderCreate,
    _: None = Depends(check_permission("orders", "create")),
    service: OrderService = Depends(get_order_service),
):
    """Создание заявки."""
    return await service.create_order(order)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order(
    order_id: UUID,
    _: None = Depends(check_permission("orders", "delete")),
    service: OrderService = Depends(get_order_service),
):
    """Удаление заявки по ID."""
    await service.delete_order(order_id)
