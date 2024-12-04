from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.sql._elements_constructors import and_, or_

from app.delivery.exceptions import ShopCartItemsNotFound
from app.delivery.schemas import ShoppingCartWithIdDTO
from app.models import (
    DishORM,
    RestaurantORM,
    ShoppingCartItemsORM,
    ShoppingCartORM,
    UserORM,
)
from app.utils.repository import SQLAlchemyRepository


class DishRepository(SQLAlchemyRepository):
    model = DishORM


class ShoppingCartRepository(SQLAlchemyRepository):
    model = ShoppingCartORM
    model_items = ShoppingCartItemsORM

    async def add_one(self, user: UserORM):
        stmt = insert(self.model).values(user_id=user.id).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_dish_items(self, sc: ShoppingCartWithIdDTO):
        "удаление товаров из корзины"
        stmt = delete(self.model_items).where(
            and_(
                self.model_items.shopping_cart_id == sc.shopping_cart_id,
                self.model_items.dish_id == sc.dish_id,
            )
        )
        await self.session.execute(stmt)

        return True

    async def add_dish_items(self, sc: ShoppingCartWithIdDTO):
        """Добавляем блюда в корзину"""
        data = sc.model_dump()
        stmt = insert(self.model_items).values(**data).returning(self.model_items)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def update_dish_items(self, sc: ShoppingCartWithIdDTO):
        """Обновляем блюда"""
        stmt = select(self.model_items).filter(
            and_(
                self.model_items.shopping_cart_id == sc.shopping_cart_id,
                self.model_items.dish_id == sc.dish_id,
            )
        )
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()

        if not item:
            raise ShopCartItemsNotFound

        if item.quantity > sc.quantity:
            stmt = (
                update(self.model_items)
                .where(
                    and_(
                        self.model_items.shopping_cart_id == sc.shopping_cart_id,
                        self.model_items.dish_id == sc.dish_id,
                    )
                )
                .values(quantity=item.quantity - sc.quantity)
                .returning(self.model_items)
            )
            await self.session.execute(stmt)
        else:
            await self.delete_dish_items(sc)

    async def check_if_items_exists(self, sc: ShoppingCartWithIdDTO):
        "Проверка есть ли данный товар уже в корзине"
        stmt = select(self.model_items).filter(
            and_(
                self.model_items.shopping_cart_id == sc.shopping_cart_id,
                self.model_items.dish_id == sc.dish_id,
            )
        )
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def calculate_quantity_sum(self, shopping_cart_id: int) -> int:
        "Общая стоимость товаров в корзине"
        stmt = (
            select(self.model_items.quantity, DishORM.price)
            .join(DishORM, self.model_items.dish_id == DishORM.id)
            .filter(self.model_items.shopping_cart_id == shopping_cart_id)
        )
        res = await self.session.execute(stmt)
        items = res.all()
        total = sum(item.quantity * item.price for item in items)
        return total

    async def get_position(self, shopping_cart_id: int):
        "Товары в корзине"
        stmt = (
            select(
                DishORM.id,
                DishORM.name,
                DishORM.price,
                self.model_items.quantity,
            )
            .join(DishORM, self.model_items.dish_id == DishORM.id)
            .filter(self.model_items.shopping_cart_id == shopping_cart_id)
        )
        res = await self.session.execute(stmt)
        return res.all()


class RestaurantRepository(SQLAlchemyRepository):
    model = RestaurantORM

    async def find_all(self, query: str | None = None):
        "поиск ресторанов и блюд"
        stmt = select(self.model).options(joinedload(self.model.dishes))
        if query:
            stmt = stmt.filter(
                or_(
                    self.model.name.ilike(f"%{query}%"),
                    self.model.dishes.any(DishORM.name.ilike(f"%{query}%")),
                )
            )
        res = await self.session.execute(stmt)
        return res.unique().scalars().all()
