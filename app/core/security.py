import jwt
import re
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from app.settings import settings

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r"\D", "", cpf)
    return len(cpf) == 11 and cpf.isdigit()

def criar_jwt(cpf: str):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXP_MINUTES)
    payload = {
        "cpf": cpf,
        "iss": settings.TOKEN_ISSUER,
        "exp": expiration,
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, int(expiration.timestamp())

def validar_jwt(token: str):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
