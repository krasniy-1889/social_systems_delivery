from sqlalchemy import update

from app.auth.schemas import UserDTO
from app.models import UserORM
from app.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserORM

    async def update_balance(self, user: UserDTO, pay_price: int) -> UserORM:
        "обновляет баланс у пользовтаелй после оформления ордера"
        stmt = (
            update(self.model)
            .values(money=user.money - pay_price)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()
