
from fastapi.exceptions import HTTPException
from starlette import status


class DishesAlreadyExists(HTTPException):
    def __init__(self, *args, **kwargs) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = "Название блюда уже занято"


class DishNotFound(HTTPException):
    def __init__(self, *args, **kwargs) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Блюдо не найдено"


class ShopCartNotFound(HTTPException):
    def __init__(self, *args, **kwargs) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Корзина не найдена"


class ShopCartItemsNotFound(HTTPException):
    def __init__(self, *args, **kwargs) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Товара в корзине нет"


class ShopCartItemsAlreadyExists(HTTPException):
    def __init__(self, *args, **kwargs) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = "Товар уже добавлен в корзину"


class RestaurantNotFound(HTTPException):
    def __init__(self, *args, **kwargs) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Ресторан не найдено"


class RestaurantAlreadyExists(HTTPException):
    def __init__(self, *args, **kwargs) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = "Название ресторана уже занято"
