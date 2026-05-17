from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import os
from system.config import load_env

app = FastAPI()

env = load_env()
API_KEY = env.get("API_KEY", "dev-key")

# Разрешённые домены (сайт-визитка)
origins = [
    "https://yourdomain.com",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Простая защита: API-ключ
async def check_key(request: Request):
    key = request.headers.get("Authorization", "").replace("Bearer ", "")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# Rate-limit (очень простой)
last_call = 0
def rate_limit():
    global last_call
    now = time.time()
    if now - last_call < 0.5:
        raise HTTPException(status_code=429, detail="Too many requests")
    last_call = now

# Подключаем маршруты
from api.routes.status import router as status_router
from api.routes.agents import router as agents_router
from api.routes.data import router as data_router

app.include_router(status_router, prefix="/status")
app.include_router(agents_router, prefix="/agents")
app.include_router(data_router, prefix="/data")
