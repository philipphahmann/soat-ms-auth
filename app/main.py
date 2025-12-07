from fastapi import FastAPI
from app.api.tokens import router as tokens_router
from app.api.health import router as health_router

app = FastAPI(title="Auth API")

app.include_router(tokens_router)
app.include_router(health_router)