# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# PKG Tool

import requests
import os
import json
from . import pkgmanifest
from .Package import Package

def main(argv:list[str], current_user:str, abspath:str, internet_connection:bool, upgradeable:list[Package]|str):
    try:
        if len(argv) < 3 and argv[1] != "list":
            print("Не все аргументы указаны!")
            return 1
    except IndexError:
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
        r = requests.get(f"{'https://max-mine.ru/pkg/'}{argv[2]}.mos")
        if r.status_code == 200:
            print(f"OK https://max-mine.ru/pkg/{argv[2]}.mos {round(r.elapsed.total_seconds() * 1000, 3)} мс")
            with open(package_file, "wb") as file:
                file.write(r.content)
                file.close()
            server_manifest = requests.get("https://max-mine.ru/pkg/MANIFEST.json").content
            server_manifest_json:dict[str, dict[str, str | float]] = json.loads(server_manifest)
            manifest = pkgmanifest.get_manifest(abspath, current_user)
            manifest = pkgmanifest.add_to_manifest(Package(argv[2], server_manifest_json[argv[2]]["version"], server_manifest_json[argv[2]]["help"]), manifest)
            pkgmanifest.save_manifest(manifest, abspath, current_user)
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
        if not os.path.exists(package_file):
            print("Пакет не установлен!")
            return 1
        while True:
            answer = input("Вы уверены? (д/н): ")
            if answer == "Д" or answer == "д" or answer == "Y" or answer == "y":
                os.remove(package_file)
                server_manifest = requests.get("https://max-mine.ru/pkg/MANIFEST.json").content
                server_manifest_json:dict[str, dict[str, str | float]] = json.loads(server_manifest)
                manifest = pkgmanifest.get_manifest(abspath, current_user)
                manifest = pkgmanifest.del_from_manifest(manifest[2], server_manifest_json[argv[2]]["help"], manifest)
                pkgmanifest.save_manifest(manifest, abspath, current_user)
                print("Пакет успешно удалён!")
                return 0
            elif answer == "Н" or answer == "н" or answer == "N" or answer == "n":
                print("Отмена...")
                return 0
            else:
                continue
    elif argv[1] == "update":
        if argv[2] == "--upgradeable":
            if upgradeable == "no":
                print("Все пакеты уже имеют последние версии!")
            for pkg in upgradeable:
                main(["pkg", "update", pkg.name], current_user, abspath, internet_connection, upgradeable)
            print("Все пакеты обновлены!")
        print(f"Обновление пакета {argv[2]}...")
        if not internet_connection:
            print("Интернет не подключен! Обновление недоступно!")
            return 1
        package_file = os.path.join(abspath, "Users", current_user, "Packages", argv[2] + ".mos")
        print(f"GET https://max-mine.ru/pkg/{argv[2]}.mos")
        r = requests.get(f"{'https://max-mine.ru/pkg/'}{argv[2]}.mos")
        if r.status_code == 200:
            print(f"OK https://max-mine.ru/pkg/{argv[2]}.mos {round(r.elapsed.total_seconds() * 1000, 3)} мс")
            with open(package_file, "wb") as file:
                file.write(r.content)
                file.close()
            server_manifest = requests.get("https://max-mine.ru/pkg/MANIFEST.json").content
            server_manifest_json:dict[str, dict[str, str | float]] = json.loads(server_manifest)
            manifest = pkgmanifest.get_manifest(abspath, current_user)
            manifest = pkgmanifest.del_from_manifest(manifest[2], server_manifest_json[argv[2]]["help"], manifest, False)
            manifest = pkgmanifest.add_to_manifest(Package(argv[2], server_manifest_json[argv[2]]["version"], server_manifest_json[argv[2]]["help"]), manifest)
            pkgmanifest.save_manifest(manifest, abspath, current_user)
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
        if argv[2] == "upgradeable":
            if upgradeable == "no":
                print("Все пакеты имеют последнюю версию")
            print("Пакеты доступные для обновления: ")
            for i in upgradeable:
                print(i.name + "\n")
            return 0
        print("Получение списка пакетов...")
        packages = [f for f in os.listdir(os.path.join(abspath, "Users", current_user, "Packages")) if f.endswith(".mos")]
        if len(packages) == 0:
            print("У вас не установлено ни одного пакета!")
            return 0
        print("Список пакетов: ")
        for name in packages:
            print(name.removesuffix(".mos") + "\n")
        return 0
    else:
        print("Команда не найдена! Повторите попытку!")
        return 1