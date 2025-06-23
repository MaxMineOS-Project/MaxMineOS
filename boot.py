# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# The OS Loader

print("Booting MaxMineOS")
import subprocess
import importlib
import os
import sys
import py_compile


def check_kernel_updates(kernel_version:int):
    if not internet_connection:
        print("Can't check kernel updates!")
        log.error("Can't check kernel updates, no internet connection")
        return
    import requests
    r = requests.get("https://max-mine.ru/pkg/" + "MANIFEST.MF")
    server_kernel_version = float(r.content)
    kernel_path = abspath + "System\\kernel.pyc"
    with open(kernel_path, "rb+") as file:
        previos_kernel = file.read()
        file.truncate(0)
        file.seek(0)
        
        r = requests.get("https://max-mine.ru/files/" + "kernel.py")
        file.write(r.content)
        compiled_kernel:str = py_compile.compile(kernel_path, "kernel.pyc")
        with open(compiled_kernel, "rb") as file2:
            content = file2.read()
            file.truncate(0)
            file.seek(0)
            file.write(content)
            file2.close()
            os.remove(compiled_kernel)
        target_version = importlib.import_module("kernel").TARGET_SYSTEM_VERSION
        file.close()
    if kernel_version < server_kernel_version:
        if int(target_version) != int(VER):
            print("Kernel not updated! Reason: incompatible system.")
            log.error(f"Kernel not updated! Reason: incompatible version system. System version: {VER}, but required: {target_version}")
            with open(kernel_path, "wb") as file:
                file.write(previos_kernel)
                file.close()
            return
        print("Updating kernel...")
        log.info("Updating kernel...")
        with open(kernel_path, "rb+") as file:
            r = requests.get("https://max-mine.ru/files/" + "kernel.py")
            file.write(r.content)
            file.close()
        print(f"Kernel updated to version {server_kernel_version}")
        log.info(f"Kernel updated to version {server_kernel_version}")
    else:
        print("Kernel is up-to-date")
        with open(kernel_path, "wb") as file:
            file.write(previos_kernel)
            file.close()
        log.info("Kernel is up-to-date!")

def check_strong_depencies():
    try:
        import requests, bcrypt, pendulum, dateutil, tzdata, ping3
    except ImportError:
        subprocess.run("pip install requests bcrypt pendulum python-dateutil tzdata ping3", shell=True)

def load_hostname():
    global hostname
    with open(abspath + r"boot\hostname", "rt", encoding="utf-8") as file:
        hostname = file.read()
        file.close()

def check_internet_connection():
    global internet_connection, log
    import requests
    try:
        r = requests.head("https://max-mine.ru/")
    except Exception:
        print("Info: Unable to connect to max-mine server! Please, check the internet connection!")
        print("PKG tool won't work!")
        log.warning("Cannot connect to the internet!")
        internet_connection = False
    if r.status_code != 200:
        print("Info: Unable to connect to max-mine server! Please, check the internet connection!")
        print("PKG tool won't work!")
        log.warning("Cannot connect to the internet!")
        internet_connection = False
    else:
        internet_connection = True

def load_abspath():
    global abspath
    abspath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    try:
        subprocess.run("python " + abspath + r"boot\boot.py")
    except KeyboardInterrupt:
        exit(-1)
    except EOFError:
        exit(-2)
    exit(0)

def shutdown():
    exit(0)

if __name__ == "__main__":
    load_abspath()
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "System"))
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "System", "Libraries"))
    logger = importlib.import_module("logger")
    log_file = os.path.join(abspath, "System", "logs", "system.log")
    logger.setup_logger(log_file)
    log = logger.get_logger("MaxMineOS")
    log.info("Booting System...")
    check_strong_depencies()
    check_internet_connection()
    load_hostname()
    load_users()
    load_passwords()
    two_list_to_cort()
    load_ver()
    kernel = importlib.import_module("kernel")
    check_kernel_updates(kernel.KERNEL_VERSION_SHORT)
    try:
        exitcode:int = kernel.main(internet_connection, abspath, users, VER, hostname)
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