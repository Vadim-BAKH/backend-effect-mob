"""Репозиторий для работы с mock-заказами."""

from typing import Optional
from uuid import UUID, uuid4

from fastapi_app.schemas.order import OrderCreate, OrderOut

MOCK_ORDERS: dict[UUID, OrderOut] = {}


class OrderRepo:
    """Мок-репозиторий заказов."""

    async def get(self, order_id: UUID) -> Optional[OrderOut]:
        """Получение заказа по ID."""
        return MOCK_ORDERS.get(order_id)

    async def list(self) -> list[OrderOut]:
        """Получение списка заказов."""
        return list(MOCK_ORDERS.values())

    async def create(self, order_create: OrderCreate) -> OrderOut:
        """Создание заказа."""
        order_id = uuid4()
        order = OrderOut(id=order_id, **order_create.model_dump())
        MOCK_ORDERS[order_id] = order
        return order

    async def delete(self, order_id: UUID) -> bool:
        """Удаление заказа."""
        return MOCK_ORDERS.pop(order_id, None) is not None
