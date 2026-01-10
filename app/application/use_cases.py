from app.domain.entities import CPF, Token
from app.domain.ports.repositories import TokenRepository
from app.domain.ports.services import CryptoService

class CreateTokenUseCase:
    def __init__(self, repository: TokenRepository, crypto_service: CryptoService):
        self.repository = repository
        self.crypto_service = crypto_service

    def execute(self, cpf_str: str) -> Token:
        # 1. Valida Domínio (CPF)
        try:
            cpf_entity = CPF(cpf_str)
        except ValueError as e:
            raise ValueError(str(e)) # Ou exceção de domínio específica

        # 2. Verifica Cache/Banco via Porta
        cached_token = self.repository.get_by_cpf(cpf_entity.value)
        
        # 3. Regra de Negócio: Se existe e não expirou, retorna cache
        if cached_token and not cached_token.is_expired():
            cached_token.source = "cache"
            return cached_token

        # 4. Se não, gera novo via Porta de Serviço
        token_str, expires_at = self.crypto_service.generate_token(cpf_entity.value)
        
        new_token = Token(
            cpf=cpf_entity.value,
            access_token=token_str,
            expires_at=expires_at,
            source="generated"
        )

        # 5. Salva via Porta
        self.repository.save(new_token)
        
        return new_token

class ValidateTokenUseCase:
    def __init__(self, crypto_service: CryptoService):
        self.crypto_service = crypto_service

    def execute(self, token: str):
        return self.crypto_service.decode_token(token)