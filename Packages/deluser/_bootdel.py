import os
import shutil

def bootdel(username: str, abspath: str):
    users_file = os.path.join(abspath, "boot", "users")
    passwords_file = os.path.join(abspath, "boot", "passwords")

    with open(users_file, "r", encoding="utf-8") as f:
        users = [line.strip() for line in f if line.strip()]

    with open(passwords_file, "r", encoding="utf-8") as f:
        passwords = [line.strip() for line in f if line.strip()]

    if username not in users:
        print("Пользователь не найден в списке.")
        return

    index = users.index(username)
    users.pop(index)
    passwords.pop(index)

    with open(users_file, "w", encoding="utf-8") as f:
        f.write("\n".join(users) + ("\n" if users else ""))

    with open(passwords_file, "w", encoding="utf-8") as f:
        f.write("\n".join(passwords) + ("\n" if passwords else ""))

    user_dir = os.path.join(abspath, "Users", username)
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)
