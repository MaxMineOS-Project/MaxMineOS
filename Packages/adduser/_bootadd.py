import os

def bootadd(username:str, password:str, abspath:str):
    users_file = os.path.join(abspath, "boot", "users")
    passwords_file = os.path.join(abspath, "boot", "passwords")
    with open(users_file, "at") as file:
        file.write("\n" + username)
        file.close()
    with open(passwords_file, "at") as file:
        file.write("\n" + password)
        file.close()
    os.mkdir(os.path.join(abspath, "Users", username))
    os.mkdir(os.path.join(abspath, "Users", username, "Packages"))