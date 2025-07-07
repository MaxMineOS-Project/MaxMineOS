# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# PKG Manifest Library

import json
import os
from .Package import Package

def get_manifest(abspath:str, current_user:str) -> list[Package]:
    if not os.path.exists(os.path.join(abspath, "Users", current_user, "MANIFEST.json")):
        with open(os.path.join(abspath, "Users", current_user, "MANIFEST.json"), "w", encoding="utf-8") as file:
            json.dump({}, file)
            file.close()
    with open(os.path.join(abspath, "Users", current_user, "MANIFEST.json"), "r", encoding="utf-8") as file:
        manifest:dict[str, dict[str, str | float]] = json.load(file)
    
    packages:list[Package] = []

    for name, pkg in manifest.items():
        packages.append(Package(name, pkg["version"], pkg.get("help", "")))

    return packages

def add_to_manifest(pkg:Package, manifest:list[Package]) -> list[Package]:
    manifest.append(pkg)
    return manifest


def del_from_manifest(pkg:Package, manifest:list[Package]) -> list[Package]:
    if pkg in manifest:
        manifest.remove(pkg)
    else:
        # Finding package by name
        for pka in manifest:
            if pka.name == pkg.name:
                if pka in manifest:
                    manifest.remove(pka)
                else:
                    pass # Package not in manifest
    return manifest

def save_manifest(manifest:list[Package], abspath:str, current_user:str):
    data = {}
    for pkg in manifest:
        data[pkg.name] = {
            "version": pkg.version,
            "help": pkg.helptext
        }

    with open(os.path.join(abspath, "Users", current_user, "MANIFEST.json"), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
