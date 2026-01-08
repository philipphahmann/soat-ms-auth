from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .schemas.cpf import CpfRequest

from app.core.security import criar_jwt, validar_jwt, validar_cpf
from app.services.dynamo_service import DynamoService

router = APIRouter(prefix="/tokens", tags=["Tokens"])
auth_scheme = HTTPBearer()
dynamo_service = DynamoService()

@router.post("")
def make_token(body: CpfRequest):
    if not validar_cpf(body.cpf):
        raise HTTPException(status_code=400, detail="CPF inválido")

    cached_data = dynamo_service.get_token(body.cpf)
    if cached_data:
        return {
            "token": cached_data['token'],
            "expires_at": int(cached_data['expires_at']),
            "source": "cache"
        }
    
    token, expires_at = criar_jwt(body.cpf)

    dynamo_service.save_token(body.cpf, token, expires_at)

    return {
        "token": token,
        "expires_at": expires_at,
        "source": "generated"
    }


@router.get("/validate")
def validate_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    decoded = validar_jwt(token)
    return {"valid": True, "data": decoded}
