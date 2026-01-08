from fastapi import APIRouter
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/health", tags=["Health"])

health_scheme = HTTPBearer()


@router.get("/")
def health():
    return {"health": True}
