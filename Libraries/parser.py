# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Command Parser

import os

def parse(command:list[str], current_user:str, abspath:str, internet_connection:bool, log, upgradeable:str|list):
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
        return updater.update_system(abspath, log)
    elif command[0] == "pkg":
        from . import pkg
        return pkg.main(command, current_user, abspath, internet_connection, upgradeable)
    elif command[0] == "syslog":
        return "syslog"
    elif command[0] == "help":
        from . import helpsystem
        return helpsystem.main(command)
    elif command[0] == "pkghelp":
        from . import pkghelp
        return pkghelp.main(command)
    elif command[0] == "history":
        if len(command) < 2:
            return "history"
        elif command[1] == "clean":
            return "historyclean"
        else:
            return "history"
    elif command[0] == "exitcode":
        return "exitcode"
    elif os.path.exists(os.path.join(abspath, "Users",  current_user, "Packages", command[0] + ".mos")) or os.path.exists(os.path.join(abspath, "Users", current_user, "Packages", command[0])):
        from . import apprun
        return apprun.main(command[0], command, current_user, abspath)
    else:
        return "invalid"