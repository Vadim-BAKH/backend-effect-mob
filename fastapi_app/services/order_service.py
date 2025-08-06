"""Модуль сервиса работы с заказами."""

from uuid import UUID

from fastapi_app.repositories import OrderRepo
from fastapi_app.schemas import OrderCreate, OrderOut


class OrderService:
    """Сервис для управления логикой заказов."""

    def __init__(self, repo: OrderRepo):
        """Инициализация с репозиторием заказов."""
        self.repo = repo

    async def get_order(self, order_id: UUID) -> OrderOut | None:
        """Получить заказ по id."""
        return await self.repo.get(order_id)

    async def list_orders(self) -> list[OrderOut]:
        """Получить список всех заказов."""
        return await self.repo.list()

    async def create_order(self, order_create: OrderCreate) -> OrderOut:
        """Создать заказ."""
        return await self.repo.create(order_create)

    async def delete_order(self, order_id: UUID) -> bool:
        """Удалить заказ."""
        return await self.repo.delete(order_id)
