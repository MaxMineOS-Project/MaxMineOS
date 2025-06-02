import _bootedit
import getpass
import os

def main(argv: list[str], abspath: str, current_user: str):
    success = _bootedit.change_password(current_user, abspath)
    if success:
        print("Пароль успешно изменён.")
        return 0
    else:
        print("Не удалось изменить пароль.")
        return 1
