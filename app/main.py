from fastapi import FastAPI
from app.adapters.input.api import router as tokens_router
from app.adapters.input.api import health as health_router

app = FastAPI(title="Auth API")

app.include_router(health_router.router)
app.include_router(tokens_router.router)