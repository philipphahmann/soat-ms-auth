from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any

class CryptoService(ABC):
    @abstractmethod
    def generate_token(self, cpf: str) -> Tuple[str, int]:
        """Retorna (token, timestamp_expiracao)"""
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Dict[str, Any]:
        pass