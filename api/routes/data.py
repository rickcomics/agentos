from fastapi import APIRouter
from system.notion import get_new_items, get_routed_items

router = APIRouter()

@router.get("/new")
async def new_items():
    return get_new_items()

@router.get("/routed/{route_name}")
async def routed_items(route_name: str):
    return get_routed_items(route_name)
