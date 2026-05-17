from fastapi import APIRouter, Request, HTTPException
import os
import signal

router = APIRouter()

@router.post("/start")
async def start_agents(request: Request):
    os.system("python runtime.py &")
    return {"status": "started"}

@router.post("/stop")
async def stop_agents(request: Request):
    os.system("python shutdown.py")
    return {"status": "stopped"}
