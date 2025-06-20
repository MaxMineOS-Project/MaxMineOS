# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Help System


def main(argv:list[str]):
    if len(argv) == 1:
        print("Доступные команды:")
        print("exit")
        print("reboot")
        print("logout")
        print("pkg")
        print("hostnamectl")
        print("whoami")
        print("ver")
        print("uptime")
        print('help')
        print("Установленные пакеты запускаются по их имени")
        print("Справку по определенной команде можно увидеть командой: help <команда>")
        print("Для получения помощи по определенному пакету запустите: pkghelp <пакет>")
        return 0
    else:
        if argv[1] == "exit":
            print("exit - завершение работы системы")
            return 0
        elif argv[1] == "reboot":
            print("reboot - перезапуск системы")
            return 0
        elif argv[1] == "logout":
            print("logout - завершение сеанса текущего пользователя")
            return 0
        elif argv[1] == "pkg":
            print("pkg - удобный пакетный менеджер")
            print("pkg install - установка пакетов")
            print("Синтаксис: pkg install <пакет>")
            print("pkg delete - удаление пакетов")
            print("Синтаксис: pkg delete <пакет>")
            print("pkg list - список пакетов")
            print("pkg update - обновление пакетов")
            print("Синтаксис: pkg update <пакет>")
            return 0
        elif argv[1] == "hostnamectl":
            print("hostnamectl - выводит комплексную информацию о системе")
            return 0
        elif argv[1] == "whoami":
            print("whoami - показывает имя текущего пользователя")
            return 0
        elif argv[1] == "ver":
            print("ver - показывает версию системы")
            return 0
        elif argv[1] == "uptime":
            print("uptime - показывает время работы системы с последнего перезапуска")
            return 0
        elif argv[1] == "help":
            print("help - справочная система")
            print("help - выводит общую справку")
            print("help <команда> - выводит справку по отдельной команде")
            return 0
        elif argv[1] == "pkghelp":
            print("pkghelp - справочная система по пакетам.")
            print("Синтаксис: pkghelp <пакет>")
            return 0
        else:
            print(f"Команда {argv[1]} не найдена в справочной системе")
            return 1