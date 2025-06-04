# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Main OS executable file - OS Kernel

from Libraries import authlib, lexer, parser, logger
import getpass
import pendulum
import asyncio
import os

start_time = None
KERNEL_VERSION = "maxmine-1.1.1-mm6-04.06.25"
KERNEL_VERSION_SHORT = 1.11
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

def main(internet_connection:bool, repos:list[str], abspath:str, users:dict, ver:str, hostname:str):
    global log, current_user
    log_file = os.path.join(abspath, "System", "logs", "system.log")
    logger.setup_logger(log_file)
    log = logger.get_logger("MaxMineOS")
    log.info("System booted!")
    #region AUTH
    auth(users)
    #endregion
    #region WORKCYCLE
    while True:
        prompt = input(f"{current_user}:#")
        log.info(f"User performed command {prompt}")
        if prompt == "":
            continue
        lexered_prompt = lexer.lexer(prompt)
        if lexered_prompt == 1:
            log.error("Error while lexing command!")
            continue
        exit_code = parser.parse(lexered_prompt, current_user, abspath, repos, internet_connection, log)
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
        elif exit_code == "syslog":
            with open(log_file, "r", encoding="utf-8") as file:
                print(file.read())
                file.close()
        elif exit_code == "invalid":
            log.error("User entered unknown command!")
            print("Неизвестная команда! Проверьте правильность набора!")
            continue

    #endregion