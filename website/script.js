import os
import subprocess
import sys
from pathlib import Path

from fastapi import APIRouter

router = APIRouter()


def repo_root():
    return str(Path(__file__).resolve().parents[2])


@router.post("/start")
async def start_agents():
    root = repo_root()
    subprocess.Popen(
        [sys.executable, "runtime.py"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return {"status": "started"}


@router.post("/stop")
async def stop_agents():
    root = repo_root()
    subprocess.Popen(
        [sys.executable, "shutdown.py"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return {"status": "stopped"}
