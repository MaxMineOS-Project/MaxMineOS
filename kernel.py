# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Main OS executable file - OS Kernel

from Libraries import authlib, lexer, parser
import getpass
import pendulum
import asyncio

start_time = None
KERNEL_VERSION = "maxmine-1.0.1-mm1-31.05.25"
KERNEL_VERSION_SHORT = 1.01

async def start_timer():
    global start_time
    start_time = pendulum.now()

def get_elapsed():
    return start_time.diff_for_humans(pendulum.now(), absolute=True)


async def timer():
    await start_timer()
asyncio.run(timer())

current_user:str
def auth(users:dict):
    global current_user
    while True:
        user = input("Введите имя пользователя: ")
        upass = getpass.getpass(("Введите пароль пользователя: "))
        if user in users:
            if authlib.auth(users, user, upass):
                print(f"Вы успешно вошли в систему под именем {user}")
                current_user = user
                break
            else:
                print("Неправильные имя пользователя и\\или пароль. Повторите попытку")
                continue
        else:
            print("Неправильные имя пользователя и\\или пароль. Повторите попытку")
            continue

def main(internet_connection:bool, repos:list[str], abspath:str, users:dict, ver:str, hostname:str):
    global current_user
    #region AUTH
    auth(users)
    #endregion
    #region WORKCYCLE
    while True:
        prompt = input(f"{current_user}:#")
        if prompt == "":
            continue
        lexered_prompt = lexer.lexer(prompt)
        if lexered_prompt == 1:
            continue
        exit_code = parser.parse(lexered_prompt, current_user, abspath, repos, internet_connection)
        if exit_code == "exit":
            return 0
        elif exit_code == "reboot":
            return 1
        elif exit_code == "logout":
            current_user = ""
            auth(users)
        elif exit_code == "hostnamectl":
            print(f"Система: MaxMineOS {ver}")
            print(f"Версия ядра: {KERNEL_VERSION}")
            print(f"Краткая версия ядра: {KERNEL_VERSION_SHORT}")
            print(f"Имя системы: {hostname}")
            print(f"Текущий пользователь: {current_user}")
            print(f"Подключение к интернету: {"Да" if internet_connection else "Нет"}")
        elif exit_code == "whoami":
            print(current_user)
        elif exit_code == "ver":
            print("Версия системы: " + ver)
        elif exit_code == "uptime":
            print(get_elapsed())
        elif exit_code == "invalid":
            print("Неизвестная команда! Проверьте правильность набора!")
            continue

    #endregion