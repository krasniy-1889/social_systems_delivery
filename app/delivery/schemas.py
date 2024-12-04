import datetime

from pydantic import BaseModel, PositiveFloat, PositiveInt


class SearchDTO(BaseModel):
    query: str | None = None


class RestaurantDishAdd(BaseModel):
    restaurant_id: PositiveInt
    dish_id: PositiveInt


class DishDTO(BaseModel):
    id: int
    name: str
    price: PositiveFloat
    created_at: datetime.datetime
    updated_at: datetime.datetime


class DishAddDTO(BaseModel):
    name: str
    price: PositiveFloat
    restaurant_id: PositiveInt


class RestaurantDTO(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class RestaurantDishesDTO(RestaurantDTO):
    dishes: list[DishDTO] = []


class RestaurantAddDTO(BaseModel):
    name: str


class ShoppingCartAddDTO(BaseModel):
    dish_id: PositiveInt
    quantity: PositiveInt


class ShoppingCartWithIdDTO(ShoppingCartAddDTO):
    shopping_cart_id: PositiveInt


class ShopCartPostitionDTO(BaseModel):
    id: PositiveInt
    name: str
    quantity: PositiveInt
    price: PositiveFloat


class ShopCartReadDTO(BaseModel):
    total_price: PositiveInt
    positions: list[ShopCartPostitionDTO]
