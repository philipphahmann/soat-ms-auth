from fastapi import APIRouter, HTTPException, Depends
from app.adapters.input.api.schemas import CpfRequest, TokenValidationRequest
from app.application.use_cases import CreateTokenUseCase, ValidateTokenUseCase

from app.adapters.output.dynamo_repository import DynamoDBTokenRepository
from app.adapters.output.jwt_service import JwtCryptoService

router = APIRouter(prefix="/tokens", tags=["Tokens"])
router = APIRouter(prefix="/tokens", tags=["Tokens"])

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

@router.post("/validate")
def validate_token(body: TokenValidationRequest, use_case: ValidateTokenUseCase = Depends(get_validate_token_use_case)):
    try:
        decoded_data = use_case.execute(body.token)
        return {"valid": True, "data": decoded_data}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")