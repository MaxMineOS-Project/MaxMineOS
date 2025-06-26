# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Command Parser

import os
from . import apprun
import time

def parse(command:list[str], current_user:str, abspath:str, internet_connection:bool, log, upgradeable):
    if command[0] == "shutdown" or command[0] == "exit":
        return "exit"
    elif command[0] == "reboot" or command[0] == "restart":
        return "reboot"
    elif command[0] == "logout":
        return "logout"
    elif command[0] == "ver":
        return "ver"
    elif command[0] == "hostnamectl":
        return "hostnamectl"
    elif command[0] == "uptime":
        return "uptime"
    elif command[0] == "whoami":
        return "whoami"
    elif command[0] == "sysupdate":
        from . import updater
        updater.update_system(abspath, log)
    elif command[0] == "pkg":
        from . import pkg
        pkg.main(command, current_user, abspath, internet_connection, upgradeable)
        return 0
    elif command[0] == "syslog":
        return "syslog"
    elif command[0] == "help":
        from . import helpsystem
        helpsystem.main(command)
        return 0
    elif command[0] == "pkghelp":
        from . import pkghelp
        pkghelp.main(command)
        return 0
    elif command[0] == "history":
        return "history"
    elif command[0] == "history" and command[1] == "clean":
        return "historyclean"
    elif os.path.exists(os.path.join(abspath, "Users",  current_user, "Packages", command[0] + ".mos")):
        apprun.main(command[0], command, current_user, abspath)
        return 0
    else:
        return "invalid"
