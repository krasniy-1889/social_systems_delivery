from fastapi.exceptions import HTTPException
from starlette import status

# class UserAlreadyExists(HTTPException):
#     pass


class UserAlreadyExists(HTTPException):
    def __init__(self, *args, **kwargs) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = "Даннный username уже занят"


class UserMoneyNotExists(HTTPException):
    def __init__(self, *args, **kwargs) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Недостаточно средтств на счету"
