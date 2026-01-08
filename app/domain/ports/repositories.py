from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities import Token

class TokenRepository(ABC):
    @abstractmethod
    def get_by_cpf(self, cpf: str) -> Optional[Token]:
        pass

    @abstractmethod
    def save(self, token: Token) -> None:
        pass