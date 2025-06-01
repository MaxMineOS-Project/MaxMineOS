import _bootadd
import getpass
import bcrypt
import os


def main(argv:list[str], abspath:str):
    if len(argv) == 1:
        print("Передайте имя пользователя в аргументы!")
        return 1
    if os.path.exists(os.path.join(abspath, "Users", argv[1])):
        print(f"Пользователь с именем {argv[1]} уже существует!")
        return 1
    upass = getpass.getpass("Введите пароль для нового пользователя: ")
    if upass == "":
        print("Пароль не может быть пустым!")
        return 1
    if upass.__contains__(" "):
        print("Пробелы не разрешены в пароле!")
    hashed_upass = bcrypt.hashpw(upass.strip().replace(" ", "").encode(), bcrypt.gensalt()).decode()
    _bootadd.bootadd(argv[1], hashed_upass, abspath)
    return 0