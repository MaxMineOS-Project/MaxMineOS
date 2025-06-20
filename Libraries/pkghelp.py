# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Package Help Library


import json
import requests

def main(argv:list[str]):
    if len(argv) < 2:
        print("Имя пакета не указано!")
        return 1
    manifest = requests.get("https://max-mine.ru/pkg/MANIFEST.json/").content
    manifest_json:dict[str, dict[str, str | float]] = json.loads(manifest)
    if manifest_json[argv[1]]:
        print(manifest_json[argv[1]]["help"])
        return 0
    else:
        print("Такого пакета не существует!")
        return 1