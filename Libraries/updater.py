# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# System Updater


import os
import shutil
import requests
import zipfile

def update_system(abspath: str, log):
    try:
        log.info("Starting system update...")
        url = "https://max-mine.ru/files/" + "MaxMineOS.zip"
        print(f"GET {url}")
        r = requests.get(url)
        if r.status_code != 200:
            print(f"ERROR {r.status_code} {url} {r.elapsed.total_seconds() * 1000} мс")
            log.error(f"Error while downloading update: {r.status_code}")
            print("Ошибка во время скачивания обновления!")
            return 1
        print(f"OK {url} {r.elapsed.total_seconds() * 1000} мс")
        update_zip = os.path.join(abspath, "System", "temp", "update.zip")
        with open(update_zip, "wb") as f:
            f.write(r.content)
        log.info("Unpacking update...")
        temp_extract_dir = os.path.join(abspath, "System", "temp", "update_temp")
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
        os.makedirs(temp_extract_dir, exist_ok=True)
        with zipfile.ZipFile(update_zip, 'r') as archive:
            archive.extractall(temp_extract_dir)
        for folder in ["System", "boot"]:
            src = os.path.join(temp_extract_dir, folder)
            dst = os.path.join(abspath, folder)
            if os.path.exists(src):
                log.info(f"Updating {folder}/...")
                for root, dirs, files in os.walk(src):
                    rel_path = os.path.relpath(root, src)
                    dst_dir = os.path.join(dst, rel_path)
                    os.makedirs(dst_dir, exist_ok=True)
                    for file in files:
                        shutil.copy2(os.path.join(root, file), os.path.join(dst_dir, file))
        log.info("Update succesfully complete.")
        print("Обновление успешно!")
        return 0
    except Exception as e:
        log.error(f"Error while updating! Error: {e}")
        print("Ошибка в овремя обновления!")
        return 1
