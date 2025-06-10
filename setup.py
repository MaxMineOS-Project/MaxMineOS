# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# MaxMineOS Installer

import requests
import bcrypt
import os
import zipfile
import getpass
import sys
import random
import string

def install():
    print("=== Добро пожаловать в установщик MaxMineOS ===")
    confirm = input("Вы уверены, что хотите установить систему? (д/н): ")
    if confirm.lower() not in ("д", "y"):
        print("Установка отменена.")
        return

    print("Запуск установки...")
    print("GET https://max-mine.ru/files/MaxMineOS.zip...")
    try:
        r = requests.get("https://max-mine.ru/files/MaxMineOS.zip")
    except Exception:
        print("Не удалось скачать архив с системой. Попробуйте перезапустить установщик")
        os.system("pause")
        sys.exit(1)
    if r.status_code == 200:
        print(f"OK 200 https://max-mine.ru/files/MaxMineOS.zip {round(r.elapsed.total_seconds() * 1000, 3)} мс")
    else:
        print(f"ERROR {r.status_code} https://max-mine.ru/files/MaxMineOS.zip")
        os.system("pause")
        sys.exit(-1)

    install_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(install_dir, "MaxMineOS.zip")

    print("Сохранение архива...")
    with open(zip_path, "wb") as file:
        file.write(r.content)

    print("Распаковка архива...")
    with zipfile.ZipFile(zip_path, 'r') as archive:
        archive.extractall(install_dir)
    os.remove(os.path.join(install_dir, "MaxMineOS.zip"))
    hostname = input("Введите имя ПК. Его нельзя будет изменить в будущем. Оставьте пустым для случайного значения: ")
    if hostname == "":
        hostname = "PC-" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
    users = []
    passwords = []
    rejected_symbols = (
        "~",
        "`",
        "!",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "@",
        "\"",
        "\\",
        "-",
        "_",
        "=",
        "+",
        ";",
        "%",
        "^",
        ":",
        "&",
        "?",
        ",",
        ".",
        "/",
        ">",
        "<",
        "\t",
        "'",
        "[",
        "]",
        "{",
        "}",
        "(",
        ")",
        "*"
    )
    while True:
        user = input("Введите имя пользователя. Чтобы закончить, введите $end: ")
        if any(char in rejected_symbols for char in user):
            print("Не используйте запрещенные символы в имени!")
            continue
        if user.startswith("$") and not users:
            print("Создайте хотя бы одного пользователя!")
            continue
        if user == "":
            print("Имя пользователя не может быть пустым")
            continue
        if user == "$end" or user.startswith("$"):
            break
        if user in users:
            print("Такой пользователь уже существует!")
            continue
        user = user.replace(" ", "")
        users.append(user)
        while True:
            upass = getpass.getpass(f"Введите пароль для пользователя {user}: ")
            if upass == "":
                print("Пароль не может быть пустым! Это небезопасно!")
                continue
            if upass.__len__().__lt__(8):
                print("Пароль не может быть короче 8 символов!")
                continue
            upass = upass.replace(" ", "")
            hashed = bcrypt.hashpw(upass.encode(), bcrypt.gensalt()).decode()
            passwords.append(hashed)
            break

    print("Заполнение...")
    boot_path = os.path.join(install_dir, "boot")
    os.makedirs(boot_path, exist_ok=True)

    with open(os.path.join(boot_path, "repos"), "w") as file:
        file.write("https://max-mine.ru/pkg/\nhttps://max-mine.ru/files/")

    with open(os.path.join(boot_path, "hostname"), "w") as file:
        file.write(hostname)

    with open(os.path.join(boot_path, "users"), "w") as file:
        file.write("\n".join(users))

    with open(os.path.join(boot_path, "passwords"), "w") as file:
        file.write("\n".join(passwords))

    print("Создание пользовательских директорий...")
    for username in users:
        user_folder = os.path.join(install_dir, "Users", username)
        packages_folder = os.path.join(user_folder, "Packages")
        os.makedirs(packages_folder, exist_ok=True)

    os.makedirs(os.path.join(install_dir, "System", "temp"), mode=0o777, exist_ok=True)

    print("Система установлена успешно! Пользуйтесь!")
    os.remove(os.path.join(install_dir, "setup.exe"))
    os.remove(os.path.join(install_dir, "README.txt"))
    sys.exit(0)


# Главный цикл
while True:
    prompt = input("Installer:# ").strip()
    if prompt == "help":
        print("install - установка системы")
        print("exit - выход из установщика")
        print("help - эта справка")
    elif prompt == "exit":
        sys.exit(0)
    elif prompt == "install":
        install()
    elif prompt == "":
        continue
    else:
        print("Неизвестная команда!")