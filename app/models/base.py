import datetime

from sqlalchemy import Integer, event, func
from sqlalchemy.ext.asyncio.session import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.datetime.now,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )


class BaseORM(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@event.listens_for(BaseORM, "before_update")
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
