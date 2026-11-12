import os
from pathlib import Path


def load_env(path: str = ".env"):
    env = {}
    file_path = Path(path)

    if not file_path.exists():
        return env

    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue

            key, value = raw.split("=", 1)
            env[key.strip()] = value.strip().strip('"').strip("'")

    return env
