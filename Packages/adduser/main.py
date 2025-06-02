import _bootadd
import getpass
import bcrypt
import os


def main(argv:list[str], abspath:str):
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
        "*",
        "$"
    )
    if len(argv) == 1:
        print("Передайте имя пользователя в аргументы!")
        return 1
    if any(char in rejected_symbols for char in argv[1]):
        print("Не используйте запрещенные символы в имени!")
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