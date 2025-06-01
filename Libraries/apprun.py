# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# App Runner

import zipfile
import sys
import os
import importlib.util
import shutil
import uuid

def main(appname: str, args: list[str], current_user: str, abspath: str) -> int:
    temp_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp")
    sys.path.append(temp_path)
    path_to_package = os.path.join(abspath, "Users", current_user, "Packages", appname + ".mos")
    archive = zipfile.ZipFile(path_to_package)
    archive.extractall(temp_path)
    archive.close()
    unique_module_name = f"main_{uuid.uuid4().hex}"
    main_path = os.path.join(temp_path, "main.py")
    spec = importlib.util.spec_from_file_location(unique_module_name, main_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        ret = module.main(args, abspath, current_user) # New package type
    except TypeError:
        try:
            ret = module.main(args, abspath) # Older package type
        except TypeError:
            ret = module.main(args) # Very old package type
    del module
    shutil.rmtree(temp_path)
    os.mkdir(temp_path)
    return ret
