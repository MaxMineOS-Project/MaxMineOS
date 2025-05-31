# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Authorization Library

import bcrypt

def auth(users:dict, username:str, input:str):
    return bcrypt.checkpw(input.encode(), users[username])