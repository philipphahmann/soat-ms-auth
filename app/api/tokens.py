from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .schemas.cpf import CpfRequest

from app.core.security import criar_jwt, validar_jwt, validar_cpf

router = APIRouter(prefix="/tokens", tags=["Tokens"])

auth_scheme = HTTPBearer()


@router.post("")
def make_token(body: CpfRequest):
    if not validar_cpf(body.cpf):
        raise HTTPException(status_code=400, detail="CPF inválido")

    token = criar_jwt(body.cpf)
    return {"token": token}


@router.get("/validate")
def validate_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    decoded = validar_jwt(token)
    return {"valid": True, "data": decoded}
