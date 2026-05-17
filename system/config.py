# system/config.py

import os

def load_env():
    env = {}

    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                env[key] = value

    return env
