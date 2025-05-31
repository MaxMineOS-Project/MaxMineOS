# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Command Lexer

import shlex

def lexer(rawstring:str):
    try:
        command = shlex.split(rawstring)
    except ValueError:
        print("Ошибка разбора команды! Попробуйте еще раз!")
        return 1
    return command