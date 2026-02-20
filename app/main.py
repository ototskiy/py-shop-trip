import json
from typing import List, Dict
from datetime import datetime
import os
from decimal import Decimal

from app.customer import Customer
from app.shop import Shop
from app.car import trip_cost


def shop_trip() -> None:
    with open(os.path.join("app", "config.json"), "r") as config_file:
        config_data = json.load(config_file)

    fuel_price = config_data["FUEL_PRICE"]
    customers: List[Customer] = []
    shops: Dict[Shop] = {}

    for customer in config_data["customers"]:
        customers.append(Customer(
            customer["name"],
            customer["product_cart"],
            customer["location"],
            customer["money"],
            customer["car"]
        ))

    for shop in config_data["shops"]:
        shops[shop["name"]] = (Shop(
            shop["name"],
            shop["location"],
            shop["products"]
        ))

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")
        lowest_price_dict = {}
        lwst_shop = ""
        total_price_shop = 0

        for shop in shops.values():
            trip_cost_for_one_direction = trip_cost(
                customer.location,
                shop.location,
                fuel_price,
                customer.car["fuel_consumption"]
            )
            shop_total_price = 0
            for product, product_amount in customer.product_cart.items():
                shop_total_price += (Decimal(product_amount)
                                     * Decimal(shop.products[product]))
            total_price_trip = round(
                Decimal(shop_total_price)
                + Decimal(trip_cost_for_one_direction) * 2, 2
            )
            print(f"{customer.name}'s trip to the "
                  f"{shop.name} costs {total_price_trip}")

            if customer.money >= total_price_trip:
                lowest_price_dict[shop.name] = total_price_trip

        if lowest_price_dict:
            lwst_shop = min(lowest_price_dict, key=lowest_price_dict.get)
            total_price_shop = min(lowest_price_dict.values())
            print(f"{customer.name} rides to {lwst_shop}\n")
        else:
            print(f"{customer.name} doesn't have "
                  f"enough money to make a purchase in any shop")

        if lwst_shop:
            datetime_format = "%m/%d/%Y, %H:%M:%S"
            print(f"Date: {datetime.now().strftime(datetime_format)}")
            print(f"Thanks, {customer.name}, for your purchase!")
            print("You have bought:")
            for product, product_amount in customer.product_cart.items():
                print(f"{product_amount} "
                      f"{product}s for "
                      f"{product_amount * shops[lwst_shop].products[product]}"
                      f" dollars")
            print(f"Total cost is {total_price_shop} dollars")
            print("See you again!\n")
            print(f"{customer.name} rides home")
            print(f"{customer.name} now has "
                  f"{round(customer.money - total_price_shop, 2)} dollars\n")


shop_trip()
