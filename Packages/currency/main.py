import os
import requests
import time
import json

def main(argv:list[str], abspath):
    print("Введите код валюты (например, USD, EUR, GBP):")
    target = input("→ ").strip().upper()

    if not target or len(target) != 3:
        print("Ошибка: введите трёхбуквенный код валюты, например USD.")
        return 1

    base = "RUB"
    cache_file = os.path.join(abspath, "System", "temp", "currency_cache.json")

    rates = {}

    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
                timestamp = cache.get("timestamp", 0)
                if time.time() - timestamp < 3600:
                    rates = cache.get("rates", {})
        except:
            pass

    if target not in rates:
        url = f"https://open.er-api.com/v6/latest/{base}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get("result") != "success":
                print("Не удалось получить данные о курсе.")
                return 1
            rates = data.get("rates", {})
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({
                    "timestamp": time.time(),
                    "rates": rates
                }, f)
        except Exception as e:
            print(f"Ошибка запроса курса!")
            return 1

    if target not in rates:
        print(f"Валюта '{target}' не найдена.")
        return 1

    rate = rates[target]
    print(f"1 {base} = {rate:.4f} {target}")
    return 0
