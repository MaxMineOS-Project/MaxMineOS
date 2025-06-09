# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# PKG Tool

import requests
import os

def main(argv:list[str], repos:list[str], current_user:str, abspath:str, internet_connection:bool):
    if len(argv) < 3:
        print("Не все аргументы указаны!")
        return 1
    if argv[1] == "install":
        if not internet_connection:
            print("Интернет не подключен! Установка недоступна!")
            return 1
        package_file = os.path.join(abspath, "Users", current_user, "Packages", argv[2] + ".mos")
        if os.path.exists(package_file):
            print("Пакет уже установлен!")
            return 1
        print(f"Установка пакета {argv[2]}...")
        print(f"GET https://max-mine.ru/pkg/{argv[2]}.mos")
        r = requests.get(f"{repos[0]}{argv[2]}.mos")
        if r.status_code == 200:
            print(f"OK https://max-mine.ru/pkg/{argv[2]}.mos {round(r.elapsed.total_seconds() * 1000, 3)} мс")
            with open(package_file, "wb") as file:
                file.write(r.content)
                file.close()
            print("Пакет успешно установлен!")
            return 0
        else:
            print(f"ERROR {r.status_code} https://max-mine.ru/pkg/{argv[2]}.mos {round(r.elapsed.total_seconds() * 1000, 3)} мс")
            if r.status_code != 404:
                print("Сервер недоступен")
            else:
                print("Пакет не существует!")
            return 1
    elif argv[1] == "delete":
        print(f"Удаление пакета {argv[2]}...")
        package_file = os.path.join(abspath, "Users", current_user, "Packages", argv[2] + ".mos")
        while True:
            answer = input("Вы уверены? (д/н): ")
            if answer == "Д" or answer == "д" or answer == "Y" or answer == "y":
                if os.path.exists(package_file):
                    os.remove(package_file)
                    return 0
                else:
                    print("Пакет уже удален!")
                    return 1
            elif answer == "Н" or answer == "н" or answer == "N" or answer == "n":
                print("Отмена...")
                return 0
            else:
                continue
    elif argv[1] == "update":
        print(f"Обновление пакета {argv[2]}...")
        if not internet_connection:
            print("Интернет не подключен! Обновление недоступно!")
            return 1
        package_file = os.path.join(abspath, "Users", current_user, "Packages", argv[2] + ".mos")
        print(f"GET https://max-mine.ru/pkg/{argv[2]}.mos")
        r = requests.get(f"{repos[0]}{argv[2]}.mos")
        if r.status_code == 200:
            print(f"OK https://max-mine.ru/pkg/{argv[2]}.mos {round(r.elapsed.total_seconds() * 1000, 3)} мс")
            with open(package_file, "wb") as file:
                file.write(r.content)
                file.close()
            print("Пакет успешно обновлен!")
            return 0
        else:
            print(f"ERROR {r.status_code} https://max-mine.ru/pkg/{argv[2]}.mos {round(r.elapsed.total_seconds() * 1000, 3)} мс")
            if r.status_code != 404:
                print("Сервер недоступен")
            else:
                print("Пакет не существует!")
            return 1
    elif argv[1] == "list":
        print("Получение списка пакетов...")
        packages = [f for f in os.listdir(os.path.join(abspath, "Users", current_user, "Packages")) if f.endswith(".mos")]
        if len(packages) == 0:
            print("У вас не установлено ни одного пакета!")
            return 0
        print("Список пакетов: ")
        for name in packages:
            print(name + "\n")
        return 0
    else:
        print("Команда не найдена! Повторите попытку!")
        return 1