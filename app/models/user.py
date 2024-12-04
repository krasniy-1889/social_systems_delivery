from typing import List

from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import CheckConstraint

from app.models import BaseORM, TimestampMixin


class UserORM(BaseORM, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    money: Mapped[float] = mapped_column(Float, default=0)
    shopping_cart: Mapped["ShoppingCartORM"] = relationship(
        "ShoppingCartORM", back_populates="user", uselist=False
    )
    orders: Mapped[List["OrderORM"]] = relationship(
        "OrderORM",
        back_populates="user",
    )

    __table_args__ = (
        CheckConstraint(
            "money >= 0", name="check_money_positive"
        ),  # проверяем что денег не может быть меньше 0
    )
