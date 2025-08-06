"""Роутер для управления Моковыми заявками."""

from uuid import UUID

from fastapi import APIRouter, Depends

from fastapi_app.dependencies import check_permission, get_order_service
from fastapi_app.schemas import OrderCreate, OrderOut
from fastapi_app.services import OrderService

router = APIRouter(prefix="/orders", tags=["Order"])


@router.get("/", response_model=list[OrderOut])
async def list_orders(
    _: None = Depends(check_permission("orders", "read")),
    service: OrderService = Depends(get_order_service),
):
    """Получение списка заявок."""
    return await service.list_orders()


@router.post("/", response_model=OrderOut)
async def create_order(
    order: OrderCreate,
    _: None = Depends(check_permission("orders", "create")),
    service: OrderService = Depends(get_order_service),
):
    """Создание заявки."""
    return await service.create_order(order)


@router.delete("/{order_id}", response_model=OrderOut)
async def delete_order(
    order_id: UUID,
    _: None = Depends(check_permission("orders", "delete")),
    service: OrderService = Depends(get_order_service),
):
    """Удаление заявки по ID."""
    return await service.delete_order(order_id)
