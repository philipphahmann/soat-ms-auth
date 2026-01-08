from fastapi import APIRouter, HTTPException, Depends
from app.adapters.input.api.schemas import CpfRequest
from app.application.use_cases import CreateTokenUseCase

from app.adapters.output.dynamo_repository import DynamoDBTokenRepository
from app.adapters.output.jwt_service import JwtCryptoService

router = APIRouter(prefix="/tokens", tags=["Tokens"])

# Função simples de injeção de dependência
def get_create_token_use_case():
    repo = DynamoDBTokenRepository()
    crypto = JwtCryptoService()
    return CreateTokenUseCase(repo, crypto)

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