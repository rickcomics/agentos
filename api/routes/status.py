from fastapi import APIRouter, Request
from system.config import load_env

router = APIRouter()

@router.get("/")
async def system_status(request: Request):
    return {
        "system": "running",
        "agents": "active",
        "version": "0.1"
    }
