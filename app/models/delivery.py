from typing import List

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import CheckConstraint

from app.models import BaseORM, TimestampMixin


class RestaurantORM(BaseORM, TimestampMixin):
    """Модель ресторанов"""

    __tablename__ = "restaurants"

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )  # тут мы выставили unique=True, так как это естовое задание. Но в вроде названия могу повторяться
    dishes: Mapped[list["DishORM"]] = relationship(
        "DishORM",
        back_populates="restaurant",
    )


class DishORM(BaseORM, TimestampMixin):
    """Модель блюд"""

    __tablename__ = "dishes"

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )  # тут мы выставили unique=True, но в жизни название могу повторяться
    price: Mapped[float] = mapped_column(Float, nullable=False)
    restaurant_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False,
    )
    restaurant: Mapped["RestaurantORM"] = relationship(
        "RestaurantORM",
        back_populates="dishes",
    )
    __table_args__ = (
        CheckConstraint(
            "price > 0", name="check_price_positive"
        ),  # проверяем что цена не может быть меньше 0
    )


class ShoppingCartORM(BaseORM):
    "корзина заказов"

    __tablename__ = "shopping_cart"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    user: Mapped["UserORM"] = relationship("UserORM", back_populates="shopping_cart")

    cart_items: Mapped[List["ShoppingCartItemsORM"]] = relationship(
        "ShoppingCartItemsORM",
        back_populates="shopping_cart",
    )


class ShoppingCartItemsORM(BaseORM, TimestampMixin):
    "модель блюд связанных с корзиной"

    __tablename__ = "shopping_cart_items"

    shopping_cart_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("shopping_cart.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    dish_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dishes.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    shopping_cart: Mapped["ShoppingCartORM"] = relationship(
        "ShoppingCartORM",
        back_populates="cart_items",
    )


class OrderORM(BaseORM, TimestampMixin):
    "Модель оплаченых заказов"

    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    user: Mapped["UserORM"] = relationship("UserORM", back_populates="orders")
