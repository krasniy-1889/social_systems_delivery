from argon2 import PasswordHasher

from app.auth.auth import UserDTO
from app.auth.schemas import UserAddDTO, UserPasswordReadDTO
from app.utils.unitofwork import IUnitOfWork


class PasswordService:
    ph = PasswordHasher()

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.ph.hash(password)

    @classmethod
    def verify_password(cls, password: str, password_hash: str) -> bool:
        return cls.ph.verify(password_hash, password)


class AuthService:
    async def add_user(self, uow: IUnitOfWork, user: UserAddDTO) -> UserDTO:
        user.password = PasswordService.hash_password(user.password)

        user_dict = user.model_dump()
        async with uow:
            user = await uow.users.add_one(user_dict)
            await uow.shopping_carts.add_one(user)
            await uow.commit()
            return user

    async def find_one(
        self, uow: IUnitOfWork, **filter_by
    ) -> UserPasswordReadDTO | None:
        async with uow:
            user = await uow.users.find_one(**filter_by)
            if user:
                return UserPasswordReadDTO(**user.as_dict())
