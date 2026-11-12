from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from system.config import load_env

app = FastAPI(title="AgentOS")

env = load_env()
API_KEY = env.get("API_KEY", "dev-key")

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost",
    "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

last_call = 0


async def check_key(request: Request):
    key = request.headers.get("Authorization", "").replace("Bearer ", "")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


def rate_limit():
    global last_call
    now = time.time()
    if now - last_call < 0.5:
        raise HTTPException(status_code=429, detail="Too many requests")
    last_call = now


from api.routes.status import router as status_router
from api.routes.agents import router as agents_router
from api.routes.data import router as data_router

app.include_router(status_router, prefix="/status")
app.include_router(agents_router, prefix="/agents")
app.include_router(data_router, prefix="/data")
