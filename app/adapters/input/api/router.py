from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.adapters.input.api.schemas import CpfRequest
from app.application.use_cases import CreateTokenUseCase, ValidateTokenUseCase

from app.adapters.output.dynamo_repository import DynamoDBTokenRepository
from app.adapters.output.jwt_service import JwtCryptoService

router = APIRouter(prefix="/tokens", tags=["Tokens"])

security = HTTPBearer()

def get_create_token_use_case():
    repo = DynamoDBTokenRepository()
    crypto = JwtCryptoService()
    return CreateTokenUseCase(repo, crypto)

def get_validate_token_use_case():
    crypto = JwtCryptoService()
    return ValidateTokenUseCase(crypto)

@router.post("")
def make_token(body: CpfRequest, use_case: CreateTokenUseCase = Depends(get_create_token_use_case)):
    try:
        token_entity = use_case.execute(body.cpf)
        return {
            "token": token_entity.access_token,
            "expires_at": token_entity.expires_at,
            "source": token_entity.source
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/validate")
def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    use_case: ValidateTokenUseCase = Depends(get_validate_token_use_case)
):
    token = credentials.credentials
    
    try:
        decoded_data = use_case.execute(token)
        return {"valid": True, "data": decoded_data}
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")