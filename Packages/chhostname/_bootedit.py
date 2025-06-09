import os
def boot_edit(new_hostname:str, abspath:str):
    with open(os.path.join(abspath, "boot", "hostname"), "wt", encoding="utf-8") as file:
        file.write(new_hostname)
        file.close()
        