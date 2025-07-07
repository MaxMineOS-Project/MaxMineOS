# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Main OS executable file - OS Kernel

from Libraries import authlib, lexer, parser, logger, pkgmanifest
from Libraries.Package import Package
import getpass
import pendulum
import asyncio
import os
import requests
import json

start_time = None
KERNEL_VERSION = "maxmine-1.3.3-mm13-04.07.25"
KERNEL_VERSION_SHORT = 1.33
TARGET_SYSTEM_VERSION = 13
async def start_timer():
    global start_time
    start_time = pendulum.now()



async def timer():
    await start_timer()
asyncio.run(timer())
current_user:str

def check_updates(abspath):
    global current_user
    manifest:list[Package] = pkgmanifest.get_manifest(abspath, current_user)
    server_manifest = requests.get("https://max-mine.ru/pkg/MANIFEST.json/").content
    server_manifest_json:dict[str, dict[str, str | float]] = json.loads(server_manifest)
    upgradeable:list[Package] = []
    for package in manifest:
        if float(package.version) < float(server_manifest_json[package.name]["version"]):
            upgradeable.append(package)
    if len(upgradeable) == 0:
        return "no"
    else:
        return upgradeable
    
def check_system_updates():
    r = requests.get("https://max-mine.ru/pkg/SYSVER/")
    if r.status_code == 200:
        server_system_version = float(r.content)
    return server_system_version

def auth(users:dict):
    global current_user
    while True:
        user = input("Введите имя пользователя: ")
        log.info(f"User entered name {user}")
        upass = getpass.getpass(("Введите пароль пользователя: "))
        if user in users:
            if authlib.auth(users, user, upass):
                print(f"Вы успешно вошли в систему под именем {user}")
                current_user = user
                log.info(f"User authorized with name {current_user}")
                break
            else:
                print("Неправильные имя пользователя и\\или пароль. Повторите попытку")
                log.error("User entered wrong password")
                continue
        else:
            print("Неправильные имя пользователя и\\или пароль. Повторите попытку")
            log.error("User entered wrong username")
            continue

def main(ic:bool, abspath:str, users:dict, ver:str, hostname:str):
    global log, current_user, internet_connection, prompt, exit_code
    internet_connection = ic
    log_file = os.path.join(abspath, "System", "logs", "system.log")
    logger.setup_logger(log_file)
    log = logger.get_logger("MaxMineOS")
    log.info("System booted.")
    log.info("Checking system updates...")
    new_system_version = check_system_updates()
    if float(ver) < new_system_version:
        log.info(f"Found update! New version: {new_system_version}")
        print("Доступна новая версия системы! Обновите систему командой sysupdate!")
    else:
        log.info("Update not found")
    auth(users)
    print("Введите help для получения помощи")
    log.info("Checking package updates...")
    upgradeable_packages = check_updates(abspath)
    if upgradeable_packages == "no":
        print("Все пакеты имеют последние версии")
    else:
        print(f"Для обновления доступно {len(upgradeable_packages)} пакетов. Введите pkg list upgradeable для их просмотра и pkg update --upgradeable для их обновления")
    while True:
        prompt = input(f"{current_user}@{hostname}:#")
        if not prompt == "":
            with open(os.path.join(abspath, "System", "history"), "at", encoding="utf-8") as file:
                file.write(prompt + "\n")
                file.close()
        log.info(f"User performed command {prompt}")
        if prompt == "":
            continue
        lexered_prompt = lexer.lexer(prompt)
        if lexered_prompt == 1:
            log.error("Error while lexing command!")
            continue
        exit_code = parser.parse(lexered_prompt, current_user, abspath, internet_connection, log, upgradeable_packages)
        log.info(f"Exit code: {exit_code}")
        if exit_code == "exit":
            log.info("EXIT")
            return 0
        elif exit_code == "reboot":
            log.info("REBOOT")
            return 1
        elif exit_code == "logout":
            log.info("LOGOUT")
            current_user = ""
            auth(users)
        elif exit_code == "hostnamectl":
            try:
                r = requests.head("https://max-mine.ru/")
                if r.status_code == 200:
                    internet_connection = True
                else:
                    internet_connection = False
            except Exception:
                internet_connection = False
            print(f"Система: MaxMineOS {ver}")
            print(f"Версия ядра: {KERNEL_VERSION}")
            print(f"Краткая версия ядра: {KERNEL_VERSION_SHORT}")
            print(f"Имя системы: {hostname}")
            print(f"Путь установки системы: {abspath}")
            print(f"Текущий пользователь: {current_user}")
            print(f"Подключение к интернету: {'Да' if internet_connection else 'Нет'}")
        elif exit_code == "whoami":
            print(current_user)
        elif exit_code == "ver":
            print("Версия системы: " + ver)
        elif exit_code == "uptime":
            print(start_time.diff_for_humans(pendulum.now(), absolute=True))
        elif exit_code == "syslog": # Undocumented
            with open(log_file, "r", encoding="utf-8") as file:
                print(file.read())
                file.close()
        elif exit_code == "history":
            with open(os.path.join(abspath, "System", "history"), "rt", encoding='utf-8') as file:
                print(file.read().strip())
                file.close()
        elif exit_code == "historyclean":
            with open(os.path.join(abspath, "System", "history"), "w", encoding="utf-8") as file:
                file.close()
            print("История успешно очищена!")
        elif exit_code == "invalid":
            log.error("User entered unknown command!")
            print("Неизвестная команда! Проверьте правильность набора!")
            special_exit_code = -1
            continue
        elif exit_code == "exitcode":
            print(f"Последний код выхода: {special_exit_code}")
        else:
            special_exit_code = exit_code