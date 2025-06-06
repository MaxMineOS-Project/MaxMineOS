def main(argv:list[str]):
    if len(argv) < 2:
        print("Помощь по пакетам")
        print("pkghelp <пакет> - справка по указанному пакету")
        return 0
    if argv[1] == "adduser":
        print("adduser - создание пользователя")
        print("Синтаксис: adduser <пользователь>")
        return 0
    if argv[1] == "chpwd":
        print("chpwd - смена пароля на текущего пользователя")
        return 0
    if argv[1] == "cls":
        print("cls - очистка консоли")
        return 0
    if argv[1] == "deluser":
        print("deluser - удаление пользователя")
        print("Синтаксис: deluser <пользователь>")
        return 0
    if argv[1] == "echo":
        print("echo - вывод аргументов в консоль")
        print("Синтаксис: echo <аргументы>")
        return 0
    if argv[1] == "hello":
        print("hello - выводит \"Привет, Мир!\" в консоль")
        return 0
    if argv[1] == "ping":
        print("Базовая TCP\\IP утилита. Подробности командой ping")
        return 0
    if argv[1] == "pkghelp":
        print("Справку по этому пакету можно увидеть командой help pkghelp")
        return 0
    else:
        print(f"Пакета {argv[1]} не существует!")
        return 0