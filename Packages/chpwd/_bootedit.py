import os
import bcrypt
import getpass

def change_password(username: str, abspath: str) -> bool:
    users_file = os.path.join(abspath, "boot", "users")
    passwords_file = os.path.join(abspath, "boot", "passwords")

    # Загрузка данных
    with open(users_file, "r", encoding="utf-8") as f:
        users = [line.strip() for line in f if line.strip()]
    with open(passwords_file, "r", encoding="utf-8") as f:
        passwords = [line.strip() for line in f if line.strip()]

    if username not in users:
        print("Пользователь не найден в системе.")
        return False

    index = users.index(username)
    stored_hash = passwords[index]

    # Проверка старого пароля
    old_password = getpass.getpass("Введите текущий пароль: ").strip()
    if not bcrypt.checkpw(old_password.encode(), stored_hash.encode()):
        print("Неверный текущий пароль.")
        return False

    # Новый пароль
    new_password = getpass.getpass("Введите новый пароль: ").strip()
    confirm_password = getpass.getpass("Подтвердите новый пароль: ").strip()

    if new_password != confirm_password:
        print("Пароли не совпадают.")
        return False

    if not new_password:
        print("Пароль не может быть пустым.")
        return False

    new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

    # Обновление хэша
    passwords[index] = new_hash
    with open(passwords_file, "w", encoding="utf-8") as f:
        f.write("\n".join(passwords) + "\n")

    return True
