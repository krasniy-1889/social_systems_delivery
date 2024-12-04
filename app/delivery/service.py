from app.auth.exceptions import UserMoneyNotExists
from app.auth.schemas import UserDTO
from app.delivery.exceptions import (
    RestaurantNotFound,
    ShopCartItemsAlreadyExists,
    ShopCartItemsNotFound,
    ShopCartNotFound,
)
from app.delivery.schemas import (
    DishAddDTO,
    DishDTO,
    RestaurantAddDTO,
    RestaurantDishesDTO,
    RestaurantDTO,
    ShopCartPostitionDTO,
    ShopCartReadDTO,
    ShoppingCartAddDTO,
    ShoppingCartWithIdDTO,
)
from app.utils.unitofwork import IUnitOfWork


class DishService:
    async def add_dish(self, uow: IUnitOfWork, dish: DishAddDTO) -> DishDTO:
        dish_dict = dish.model_dump()
        async with uow:
            restaurant = await uow.restaurants.find_one(id=dish.restaurant_id)

            if not restaurant:
                raise RestaurantNotFound

            dish = await uow.dishes.add_one(dish_dict)
            await uow.commit()
            return dish

    async def find_one(self, uow: IUnitOfWork, **filter_by) -> DishDTO | None:
        async with uow:
            dish = await uow.dishes.find_one(**filter_by)
            if dish:
                return dish


class RestaurantService:
    async def add_restaurant(
        self, uow: IUnitOfWork, restaurant: RestaurantAddDTO
    ) -> RestaurantDTO:
        restaurant_dict = restaurant.model_dump()
        async with uow:
            restaurant = await uow.restaurants.add_one(restaurant_dict)
            await uow.commit()
            return restaurant

    async def find_one(self, uow: IUnitOfWork, **filter_by) -> RestaurantDTO | None:
        async with uow:
            restaurant = await uow.restaurants.find_one(**filter_by)
            if restaurant:
                return restaurant

    async def find_all(
        self, uow: IUnitOfWork, query: str | None = None
    ) -> list[RestaurantDishesDTO] | list:
        async with uow:
            restaurants = await uow.restaurants.find_all(query)
            if restaurants:
                res = []
                for restaurant in restaurants:
                    dishes = [DishDTO(**dish.as_dict()) for dish in restaurant.dishes]
                    res.append(
                        RestaurantDishesDTO(
                            id=restaurant.id,
                            name=restaurant.name,
                            created_at=restaurant.created_at,
                            updated_at=restaurant.updated_at,
                            dishes=dishes,
                        )
                    )

                return res

            return []


class ShopCartService:
    async def add_dish_to_cart(
        self,
        uow: IUnitOfWork,
        shop_cart_dto: ShoppingCartAddDTO,
        user_id: int,
    ):
        async with uow:
            shop_cart = await uow.shopping_carts.find_one(user_id=user_id)
            if not shop_cart:
                # если корзина не создалась при регистрации. написть логику созданиии ее тут
                # впрочем такого быть не должно, выпадет ошибка. Но все же)
                raise ShopCartNotFound
            sc = ShoppingCartWithIdDTO(
                shopping_cart_id=shop_cart.id,
                dish_id=shop_cart_dto.dish_id,
                quantity=shop_cart_dto.quantity,
            )
            exists = await uow.shopping_carts.check_if_items_exists(sc)

            if exists:
                raise ShopCartItemsAlreadyExists

            res = await uow.shopping_carts.add_dish_items(sc)

            await uow.commit()
            return res

    async def update_cart(
        self,
        uow: IUnitOfWork,
        shop_cart_dto: ShoppingCartAddDTO,
        user_id: int,
    ):
        async with uow:
            shop_cart = await uow.shopping_carts.find_one(user_id=user_id)
            if not shop_cart:
                raise ShopCartNotFound
            sc = ShoppingCartWithIdDTO(
                shopping_cart_id=shop_cart.id,
                dish_id=shop_cart_dto.dish_id,
                quantity=shop_cart_dto.quantity,
            )
            exists = await uow.shopping_carts.check_if_items_exists(sc)

            if not exists:
                raise ShopCartItemsNotFound

            res = await uow.shopping_carts.update_dish_items(sc)

            await uow.commit()
            return res

    async def get_position(
        self,
        uow: IUnitOfWork,
        shopping_cart_id: int,
    ):
        async with uow:
            positions = await uow.shopping_carts.get_position(shopping_cart_id)
            if positions:
                positions = [
                    ShopCartPostitionDTO(
                        id=row[0],
                        name=row[1],
                        price=row[2] * row[3],  # умножаем цену на количество
                        quantity=row[3],
                    )
                    for row in positions
                ]
                return positions
            return []

    async def show_cart(
        self,
        uow: IUnitOfWork,
        user_id: int,
    ):
        async with uow:
            shop_cart = await uow.shopping_carts.find_one(user_id=user_id)

            if not shop_cart:
                raise ShopCartNotFound

            total_price = await uow.shopping_carts.calculate_quantity_sum(shop_cart.id)
            positions = await self.get_position(uow, shop_cart.id)

            cart = ShopCartReadDTO(
                total_price=total_price,
                positions=positions,
            )
            return cart

    async def pay_cart(
        self,
        uow: IUnitOfWork,
        user: UserDTO,
    ):
        async with uow:
            shop_cart = await uow.shopping_carts.find_one(user_id=user.id)

            if not shop_cart:
                raise ShopCartNotFound

            total_price = await uow.shopping_carts.calculate_quantity_sum(shop_cart.id)

            if user.money < float(total_price):
                raise UserMoneyNotExists

            await uow.users.update_balance(user, total_price)

            # тут дальше должна логика добавления в orders

            await uow.commit()

            return
