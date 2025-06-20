# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Package Class

class Package:
    def __init__(self, name:str, version:str, helptext:str=""):
        self.name = name
        self.version = version
        self.helptext = helptext
        