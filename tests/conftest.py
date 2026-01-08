import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.domain.entities import Token
from app.domain.ports.repositories import TokenRepository
from app.application.use_cases import CreateTokenUseCase
from app.adapters.output.jwt_service import JwtCryptoService

class FakeTokenRepository(TokenRepository):
    def __init__(self):
        self._storage = {}

    def get_by_cpf(self, cpf: str) -> Token | None:
        return self._storage.get(cpf)

    def save(self, token: Token) -> None:
        self._storage[token.cpf] = token

@pytest.fixture
def client():
    fake_repo = FakeTokenRepository()
    jwt_service = JwtCryptoService()

    def get_create_token_use_case_override():
        return CreateTokenUseCase(fake_repo, jwt_service)

    app.dependency_overrides[CreateTokenUseCase] = get_create_token_use_case_override
    
    from app.adapters.input.api.router import get_create_token_use_case
    app.dependency_overrides[get_create_token_use_case] = get_create_token_use_case_override

    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()