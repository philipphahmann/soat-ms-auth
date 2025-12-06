from fastapi import FastAPI
from app.api.tokens import router as tokens_router

app = FastAPI(title="Auth API")

app.include_router(tokens_router)
