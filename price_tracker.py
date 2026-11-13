import json
import requests
import time

def save_data(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)

def load_data(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def update_record(coin, price, filename):
    records = load_data(filename)
    records[coin]= price
    save_data(records, filename)

def get_price(coin):
    url= f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json() 
    return data[coin]["usd"]

old_data = load_data("last_price.json")

text = input("Введите монеты через запятую: ")
coins = [coin.strip() for coin in text.split(",") if coin.strip()]

growing = 0
falling = 0

for coin in coins:
    try:
        price = get_price(coin)  
    except KeyError:
        print(f"Не удалось получить цену {coin}, пропускаю")
        continue

    if coin in old_data:
        print(f"--- {coin} ---")
        difference = price - old_data[coin]
        percent = round(difference / old_data[coin] * 100, 2)

        if percent > 0:
            growing += 1
        elif percent < 0:
            falling += 1

        if percent >= 0:
            text = f"+{percent}"
        else:
            text = f"{percent}"
        print(f"Прошлая цена: ${old_data[coin]}")
        print(f"Сейчас: ${price}")
        print(f"Изменение: {text}%")
    else:
        print("Первый запуск, сравнивать пока не с чем")

    update_record(coin, price, "last_price.json")
    time.sleep(2)   

print(f"Выросло: {growing}, упало: {falling}") 