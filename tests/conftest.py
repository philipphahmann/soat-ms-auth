import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.domain.entities import Token
from app.domain.ports.repositories import TokenRepository
from app.application.use_cases import CreateTokenUseCase
from app.adapters.output.jwt_service import JwtCryptoService

# 1. Criamos um "Fake" Repository que salva em memória (Dicionário)
# Isso elimina a necessidade de mockar o Boto3/DynamoDB complexamente
class FakeTokenRepository(TokenRepository):
    def __init__(self):
        self._storage = {}

    def get_by_cpf(self, cpf: str) -> Token | None:
        return self._storage.get(cpf)

    def save(self, token: Token) -> None:
        self._storage[token.cpf] = token

# 2. Fixture que substitui a injeção de dependência real pelo Fake
@pytest.fixture
def client():
    # Instanciamos as versões fake/reais que queremos usar nos testes
    fake_repo = FakeTokenRepository()
    jwt_service = JwtCryptoService() # Podemos usar o serviço real pois é apenas lógica matemática

    # Função que será injetada no lugar da original
    def get_create_token_use_case_override():
        return CreateTokenUseCase(fake_repo, jwt_service)

    # A mágica do FastAPI: Dependency Overrides
    # Substituímos a dependência do tipo CreateTokenUseCase pela nossa versão com repo falso
    app.dependency_overrides[CreateTokenUseCase] = get_create_token_use_case_override
    
    # Se você usou a função "get_create_token_use_case" no router.py como Depends, 
    # você deve sobrescrever ELA. Vamos assumir que você injetou a classe ou a função factory.
    # Para garantir, vamos importar a função original do router se ela existir.
    from app.adapters.input.api.router import get_create_token_use_case
    app.dependency_overrides[get_create_token_use_case] = get_create_token_use_case_override

    with TestClient(app) as test_client:
        yield test_client
    
    # Limpeza após o teste
    app.dependency_overrides.clear()