import requests, json, time, threading, random, os
from urllib3.exceptions import InsecureRequestWarning
from colorama import Fore, Back, Style, init

init()

# Load configuration settings from settings.json
settings = json.load(open("settings.json", "r"))
item_ids = settings["items"]  # Extract item IDs and prices

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

session = requests.session()
session.cookies['.ROBLOSECURITY'] = settings["cookie"]

token = None
payload = [{ "itemType": "Asset", "id": id } for id in item_ids]
cache = []

logs = []
checks = 0

start_time = time.time()

# Create a dictionary to track items that have been warned and bought
item_warnings = {}

def refresh_tokens():
    while True:
        _set_auth()
        time.sleep(150)

def _set_auth():
    global token, session
    try:
        conn = session.post("https://auth.roblox.com/v2/logout")
        if conn.headers.get("x-csrf-token"):
            token = conn.headers["x-csrf-token"]
    except:
        time.sleep(5)
        return _set_auth()

def get_product_id(id):
    try:
        conn = session.get(f"https://economy.roblox.com/v2/assets/{id}/details", verify=False)
        data = conn.json()

        if conn.status_code == 200:
            return  {
                "id": data["ProductId"],
                "creator": data["Creator"]["Id"]
            }
        else:
            time.sleep(1)
            return get_product_id(id)
    except:
        time.sleep(1)
        return get_product_id(id)

def buy_item(product_id, seller_id, price):
    global logs

    try:
        body = {
            "expectedCurrency": 1,
            "expectedPrice": price,
            "expectedSellerId": seller_id
        }
        headers = {
            "x-csrf-token": token,
        }
        conn = session.post(f"https://economy.roblox.com/v1/purchases/products/{product_id}", headers=headers, json=body)
        data = conn.json()
        if conn.status_code == 200:
            if ("purchased" in data) and data["purchased"] == True:
                purchase_time = time.strftime('%H:%M', time.localtime())
                logs.append(f"✅ Bought:[{product_id}] {item['name']} : [💸{price} Robux] at {purchase_time}")

                # Remove the item from the warnings dictionary
                if product_id in item_warnings:
                    del item_warnings[product_id]
        else:
            return buy_item(product_id, seller_id, price)
    except:
        return buy_item(product_id, seller_id, price)

def status_update():
    global checks, logs, item_ids

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        elapsed_time = time.time() - start_time
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        print(Fore.YELLOW + Style.BRIGHT + "😁 Auto Buyer by Yoxilex 🙏" + Style.RESET_ALL)
        print(Fore.WHITE + Style.DIM + "Dm yoxile on Discord if u have any questions" + Style.RESET_ALL)
        print(Fore.CYAN + f"☑️ Checks: {checks}" + Style.RESET_ALL)
        print(Fore.LIGHTCYAN_EX + f"🕒 Elapsed Time: {elapsed_time_str}" + Style.RESET_ALL)

        # Print item IDs and prices
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "🛒 Item IDs and 💲Prices:")
        for item_id, price in item_ids.items():
            print(Fore.LIGHTGREEN_EX + f"🆔 Item ID: [{item_id}] 💸Price: {price} Robux")
        print(Style.RESET_ALL)

        print(Fore.GREEN + Style.BRIGHT + "🪵 Logs:")
        for log in logs[-10:]:
            print(log)
        print(Style.RESET_ALL)

        time.sleep(1)

def watcher():
    global token, session, checks, logs
    while True:
        try:
            headers = {
                "x-csrf-token": token,
                "cache-control": "no-cache",
                "pragma": "no-cache",
            }
            conn = session.post("https://catalog.roblox.com/v1/catalog/items/details", json={ "items": payload }, headers=headers, verify=False)

            data = conn.json()
            if conn.status_code == 200:
                checks += 1
                if "data" in data:
                    for item in data["data"]:
                        item_id = item['id']
                        item_name = item['name']

                        if "price" in item and not item_id in cache:
                            purchase_price = item_ids.get(str(item_id))
                            if purchase_price is not None:
                                if item["price"] > purchase_price:
                                    # Check if the item has already been warned
                                    if item_id not in item_warnings:
                                        item_warnings[item_id] = False
                                        logs.append(Fore.RED + Style.BRIGHT + f"❌ [{item_id}] {item_name} : The price {item['price']} is higher than the one set {purchase_price}" + Style.RESET_ALL)
                                else:
                                    cache.append(item_id)
                                    r_data = get_product_id(item_id)
                                    logs.append(Fore.RED + Style.BRIGHT + f"❌ [{item_id}] {item_name}" + Style.RESET_ALL)

                                    price = item["price"]
                                    purchase_time = None

                                    try:
                                        purchase_time = time.strftime('%H:%M', time.localtime())
                                        buy_item(r_data["id"], r_data["creator"], price)
                                    except Exception as error:
                                        purchase_time = "Failed to buy"

                                    logs[-1] = Fore.GREEN + Style.BRIGHT + f"✅ Bought:[{item_id}] {item_name} : [💸{price} Robux] at {purchase_time}" + Style.RESET_ALL
                            else:
                                logs.append(Fore.RED + Style.BRIGHT + f"❌ [{item_id}] {item_name} : Purchase price not set in settings.json" + Style.RESET_ALL)
            elif conn.status_code == 403:
                logs.append(Fore.BLUE + Style.BRIGHT + "🔄 Force refreshing auth token" + Style.RESET_ALL)
                _set_auth()
        except Exception as error:
            pass
        time.sleep(settings["watch_speed"])

if __name__ == '__main__':
    threading.Thread(target=refresh_tokens).start()
    print(Fore.YELLOW + Style.BRIGHT + "🛈 Waiting to fetch token, update cookies and restart if it takes too long" + Style.RESET_ALL)
    while token == None:
        time.sleep(1)
    print(Fore.YELLOW + Style.BRIGHT + "🎉 Fetched token" + Style.RESET_ALL)
    threading.Thread(target=status_update).start()
    threading.Thread(target=watcher).start()
