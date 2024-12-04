from typing import Annotated, List
from venv import logger

from fastapi import APIRouter, Depends
from starlette import status

from app.auth.auth import (
    get_current_user,
)
from app.auth.schemas import UserDTO
from app.delivery.exceptions import DishesAlreadyExists, RestaurantAlreadyExists
from app.delivery.schemas import (
    DishAddDTO,
    DishDTO,
    RestaurantAddDTO,
    RestaurantDishesDTO,
    RestaurantDTO,
    ShopCartReadDTO,
    ShoppingCartAddDTO,
)
from app.delivery.service import DishService, RestaurantService, ShopCartService
from app.loggers import set_logger
from app.utils.dependencies import UOWDep

router = APIRouter(
    prefix="",
    tags=["Доставка"],
)

set_logger(__name__)


# это нужно вынести в отдельнуый файл dependecies.py
# но так как проект маленький и тестовый, то оставил здесь
def get_dish_service() -> DishService:
    return DishService()


def get_restaurant_service() -> RestaurantService:
    return RestaurantService()


def get_shop_cart_service() -> ShopCartService:
    return ShopCartService()


@router.get("/")
async def root():
    return {"msg": "Social Systems"}


@router.get("/menu", response_model=List[RestaurantDishesDTO])
async def list_menu(
    # current_user: Annotated[UserDTO, Depends(get_current_user)],
    uow: UOWDep,
    restaurant_service: Annotated[RestaurantService, Depends(get_restaurant_service)],
    query: str | None = None,
):
    restaurants = await restaurant_service.find_all(uow, query)
    logger.debug(restaurants)
    return restaurants


@router.post("/add_dish", response_model=DishDTO, status_code=status.HTTP_201_CREATED)
async def add_dish(
    uow: UOWDep,
    dish: DishAddDTO,
    dish_service: Annotated[DishService, Depends(get_dish_service)],
):
    exists = await dish_service.find_one(uow, name=dish.name)
    if exists:
        raise DishesAlreadyExists

    dish = await dish_service.add_dish(uow, dish)
    return dish


@router.post(
    "/add_restaurant", response_model=RestaurantDTO, status_code=status.HTTP_201_CREATED
)
async def add_restaurant(
    uow: UOWDep,
    restaurant: RestaurantAddDTO,
    restaurant_service: Annotated[RestaurantService, Depends(get_restaurant_service)],
):
    exists = await restaurant_service.find_one(uow, name=restaurant.name)
    if exists:
        raise RestaurantAlreadyExists

    restaurant = await restaurant_service.add_restaurant(uow, restaurant)
    return restaurant


@router.post("/add_to_cart", status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    uow: UOWDep,
    current_user: Annotated[UserDTO, Depends(get_current_user)],
    shop_cart: ShoppingCartAddDTO,
    shop_cart_service: Annotated[ShopCartService, Depends(get_shop_cart_service)],
):
    res = await shop_cart_service.add_dish_to_cart(uow, shop_cart, current_user.id)
    return res


@router.post("/update_cart", status_code=status.HTTP_200_OK)
async def update_cart(
    uow: UOWDep,
    current_user: Annotated[UserDTO, Depends(get_current_user)],
    shop_cart: ShoppingCartAddDTO,
    shop_cart_service: Annotated[ShopCartService, Depends(get_shop_cart_service)],
):
    await shop_cart_service.update_cart(uow, shop_cart, current_user.id)
    return "ok"


@router.post(
    "/show_cart",
    response_model=ShopCartReadDTO,
    status_code=status.HTTP_200_OK,
)
async def show_cart(
    uow: UOWDep,
    current_user: Annotated[UserDTO, Depends(get_current_user)],
    shop_cart_service: Annotated[ShopCartService, Depends(get_shop_cart_service)],
):
    res = await shop_cart_service.show_cart(uow, current_user.id)
    return res


@router.post("/pay_cart", status_code=status.HTTP_200_OK)
async def pay_cart(
    uow: UOWDep,
    current_user: Annotated[UserDTO, Depends(get_current_user)],
    shop_cart_service: Annotated[ShopCartService, Depends(get_shop_cart_service)],
):
    res = await shop_cart_service.pay_cart(uow, current_user)
    return res
