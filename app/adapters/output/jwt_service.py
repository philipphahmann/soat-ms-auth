import jwt
from datetime import datetime, timedelta, timezone
from app.settings import settings
from app.domain.ports.services import CryptoService

class JwtCryptoService(CryptoService):
    def generate_token(self, cpf: str):
        expiration = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXP_MINUTES)
        payload = {
            "cpf": cpf,
            "iss": settings.TOKEN_ISSUER,
            "exp": expiration,
            "iat": datetime.now(timezone.utc),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token, int(expiration.timestamp())

    def decode_token(self, token: str):
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])