import datetime

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserDTO(BaseModel):
    id: int
    username: str
    money: float
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserAddDTO(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=3, max_length=75)


class UserPasswordReadDTO(UserDTO):
    password: str
