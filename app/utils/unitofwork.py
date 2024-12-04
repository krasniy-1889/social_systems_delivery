from abc import ABC, abstractmethod
from typing import Type

from app.auth.repository import UserRepository
from app.db.db import async_session_maker
from app.delivery.repository import (
    DishRepository,
    RestaurantRepository,
    ShoppingCartRepository,
)


class IUnitOfWork(ABC):
    users: Type[UserRepository]
    dishes: Type[DishRepository]
    restaurants: Type[RestaurantRepository]
    shopping_carts: Type[ShoppingCartRepository]

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...
    @abstractmethod
    async def flush(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.dishes = DishRepository(self.session)
        self.restaurants = RestaurantRepository(self.session)
        self.shopping_carts = ShoppingCartRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def flush(self):
        await self.session.flush()

    async def rollback(self):
        await self.session.rollback()
