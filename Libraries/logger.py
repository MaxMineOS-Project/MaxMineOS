# Copyright 2025 © The MaxMineOS Project
# All rights reserved

# Command Logger

import logging
import os

def setup_logger(log_path:str):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logging.basicConfig(filename=log_path, level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filemode="a", encoding="utf-8")



def get_logger(name:str):
    return logging.getLogger(name)