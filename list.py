import json
import colorama
import requests

with open("stores.json", encoding='utf-8') as f:
    # Parsed from (search for "allStores=["):
    # https://www.ikea.com/us/en/products/javascripts/range-stockcheck.961382cd6f9231488e60.js
    stores = json.load(f)


def calculate_stock(availability):
    store_id = availability["classUnitKey"]["classUnitCode"]
    store_name = \
        [store["name"] for store in stores if store["value"] == store_id]
    if len(store_name) < 1:
        return None

    store_name = store_name[0]

    next_restock = None
    try:
        availability_info = availability["buyingOption"]["cashCarry"]["availability"]
        quantity = int(availability_info["quantity"])
        if "restocks" in availability_info:
            next_restock = availability_info["restocks"][0]
    except KeyError:
        quantity = 0

    return {
        "store": store_name,
        "quantity": quantity,
        "next_restock": next_restock,
    }


def pretty_print_stock(stock):
    store = stock["store"]
    quantity = stock["quantity"]
    next_restock = stock["next_restock"]

    s = ""
    if quantity > 0:
        s += colorama.Fore.GREEN
    else:
        s += colorama.Fore.RED
    s += store
    s += colorama.Fore.RESET
    s += " "
    s += str(quantity)

    if next_restock is not None:
        s += colorama.Fore.LIGHTBLACK_EX
        s += " (restock of "
        s += colorama.Fore.RESET
        s += str(next_restock["quantity"])
        s += colorama.Fore.LIGHTBLACK_EX
        s += " coming "
        s += colorama.Fore.RESET
        s += next_restock["earliestDate"]
        s += " ~ "
        s += next_restock["latestDate"]
        s += colorama.Fore.LIGHTBLACK_EX
        s += ")"
        s += colorama.Fore.RESET

    print(s)


def main():
    colorama.init()

    print("Fetching BLÅHAJ listings…\n")

    availabilities = requests.get("https://api.ingka.ikea.com/cia/availabilities/ru/us?itemNos=90373590&expand=StoresList,Restocks,SalesLocations", headers={
        "Accept": "application/json;version=2",
        "X-Client-ID": "b6c117e5-ae61-4ef5-b4cc-e0b1e37f0631"
    })
    availabilities = availabilities.json()

    sharks = []
    for availability in availabilities["availabilities"]:
        stock = calculate_stock(availability)
        if stock is None:
            continue
        sharks.append(stock)
    sharks.sort(key=lambda s: s["quantity"], reverse=True)

    for stock in sharks:
        pretty_print_stock(stock)


main()
