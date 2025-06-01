import _bootdel
import os
import getpass
import bcrypt

def main(argv: list[str], abspath: str):
    if len(argv) == 1:
        print("Передайте имя пользователя в аргументы!")
        return 1

    username = argv[1]

    if not os.path.exists(os.path.join(abspath, "Users", username)):
        print(f"Пользователь {username} не найден!")
        return 1

    users_file = os.path.join(abspath, "boot", "users")
    passwords_file = os.path.join(abspath, "boot", "passwords")

    with open(users_file, "r", encoding="utf-8") as f:
        users = [line.strip() for line in f if line.strip()]
    with open(passwords_file, "r", encoding="utf-8") as f:
        passwords = [line.strip() for line in f if line.strip()]

    if username not in users:
        print(f"Пользователь {username} не найден в базе.")
        return 1

    index = users.index(username)
    stored_hash = passwords[index].encode()

    entered_password = getpass.getpass(f"Введите пароль пользователя {username} для подтверждения удаления: ")

    if not bcrypt.checkpw(entered_password.encode(), stored_hash):
        print("Неверный пароль! Удаление отменено.")
        return 1

    _bootdel.bootdel(username, abspath)
    print(f"Пользователь {username} успешно удалён.")
    return 0
