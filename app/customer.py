import datetime
import math
from typing import Any

from app.car import Car
from app.shop import Shop


class Customer:
    def __init__(
            self,
            name: str,
            product_cart: dict,
            location: list,
            money: int,
            car: Car
    ) -> None:

        self.name = name
        self.product_cart = product_cart
        self.location = location
        self.money = money
        self.car = car

    def has_money(self) -> None:
        print(f"{self.name} has {self.money} dollars")

    def cost_per_km(self) -> float:
        return self.car.fuel_consumption / 100

    def calculate_road_expenses(self, shops: Any, fuel_cost: float) -> float:
        distance = math.dist(self.location, shops.location)
        return distance * self.cost_per_km() * fuel_cost

    def cost_by_category(self, shopping_price: dict) -> None:
        total_amount = 0
        for product, amount in self.product_cart.items():
            price = (amount * shopping_price[product])
            total_amount += price
            print(f"{amount} {product}s for {price} dollars")

    def product_cost(self, shops: Shop) -> float:
        total_expanse = 0
        for product, price in shops.products.items():
            total_expanse += (price * self.product_cart.get(product))
        return total_expanse

    def bill_by_shop(self, shops: list[Shop], fuel_cost: float) -> None:
        cheapest_shop = {}

        for shop in shops:
            spent_for_shopping = round((self.calculate_road_expenses(
                shop, fuel_cost
            )) * 2 + self.product_cost(shop), 2)

            if spent_for_shopping > self.money:
                print(f"{self.name} doesn't have enough money "
                      f"to make a purchase in any shop")
                break

            print(f"{self.name}'s trip to the {shop.name} "
                  f"costs {spent_for_shopping}")
            cheapest_shop[shop] = spent_for_shopping

        chosen_shop = min(cheapest_shop, key=cheapest_shop.get)
        print(f"{self.name} rides to {chosen_shop.name}")
        self.money -= float(cheapest_shop[chosen_shop])
        data = datetime.datetime.now().strftime("%d/%m/20%y %H:%M:%S")
        print(f"Date: {data}")
        print(f"Thanks, {self.name}, for your purchase!")
        print("You have bought: ")
        self.cost_by_category(chosen_shop.products)
        print(f"Total cost is {self.product_cost(chosen_shop)} dollars")
        print("See you again!")

    def return_home(self) -> None:
        print(f"{self.name} rides home")
        print(f"{self.name} now has {round(self.money, 2)} dollars")
