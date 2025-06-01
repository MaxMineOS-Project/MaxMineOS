# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# The OS Loader

print("Booting MaxMineOS")
import subprocess
import importlib
import os
import sys

def check_kernel_updates(kernel_version:int):
    global repos
    import requests
    r = requests.get(repos[0] + "MANIFEST.MF")
    server_kernel_version = float(r.content)
    if kernel_version < server_kernel_version:
        print("Updating kernel...")
        log.info("Updating kernel...")
        kernel_path = abspath + "System\\kernel.py"
        with open(kernel_path, "wb") as file:
            r = requests.get(repos[1] + "kernel.py")
            file.write(r.content)
            file.close()
        print(f"Kernel updated to version {server_kernel_version}")
        log.info(f"Kernel updated to version {server_kernel_version}")
    else:
        print("Kernel is up-to-date")
        log.info("Kernel is up-to-date!")

def check_strong_depencies():
    try:
        import requests, bcrypt, pendulum, dateutil, tzdata
    except ImportError:
        subprocess.run("pip install requests bcrypt pendulum python-dateutil tzdata", shell=True)

def load_hostname():
    global hostname
    with open(abspath + r"boot\hostname", "rt", encoding="utf-8") as file:
        hostname = file.read()
        file.close()

def check_internet_connection():
    global internet_connection
    import requests
    r = requests.get("https://max-mine.ru/")
    if r.status_code != 200:
        print("Info: Unable to connect to max-mine server! Please, check the internet connection!")
        print("PKG tool won't work!")
        log.warning("Cannot connect to the internet!")
        internet_connection = False
    else:
        internet_connection = True

def load_repos():
    global repos
    with open(abspath + r"boot\repos", "rt", encoding="utf-8") as file:
        repos = file.readlines()
        repos[0] = repos[0].replace("\n", "")
        file.close()

def load_abspath():
    global abspath
    abspath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\"

def load_users():
    global usernames
    with open(abspath + r"boot\users", "rt", encoding="utf-8") as file:
        usernames = [line.strip() for line in file]

def load_passwords():
    global passwords
    with open(abspath + r"boot\passwords", "r") as file:
        passwords = [line.strip().replace("\n", "").encode() for line in file.readlines()]

def two_list_to_cort():
    global users
    users = {}
    for username, password in zip(usernames, passwords):
        users[username] = password

def load_ver():
    global VER
    with open(abspath + r"boot\ver") as file:
        VER = file.readline()

def reboot():
    subprocess.run("python " + abspath + r"boot\boot.py")
    exit(0)

def shutdown() -> None:
    exit(0)

if __name__ == "__main__":
    load_abspath()
    check_strong_depencies()
    check_internet_connection()
    load_hostname()
    load_repos()
    load_users()
    load_passwords()
    two_list_to_cort()
    load_ver()
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "System"))
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "System", "Libraries"))
    logger = importlib.import_module("logger")
    log_file = os.path.join(abspath, "System", "logs", "system.log")
    logger.setup_logger(log_file)
    log = logger.get_logger("MaxMineOS")
    log.info("Booting System...")
    kernel = importlib.import_module("kernel")
    check_kernel_updates(kernel.KERNEL_VERSION_SHORT)
    try:
        exitcode:int = kernel.main(internet_connection, repos, abspath, users, VER, hostname)
    except KeyboardInterrupt:
        print("Exiting...")
        log.critical("User Hit ^C")
        shutdown()
    except EOFError:
        print("Exiting...")
        log.critical("User Hit ^Z")
        shutdown()
    if exitcode == 0:
        shutdown()
    elif exitcode == 1:
        reboot()
