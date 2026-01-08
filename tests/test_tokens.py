from fastapi.testclient import TestClient
from app.main import app
from app.settings import settings
import jwt
from datetime import datetime, timedelta, timezone


client = TestClient(app)


def create_token(cpf: str, minutes: int = 10):
    payload = {
        "cpf": cpf,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=minutes),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def test_make_token_success():
    response = client.post("/tokens", json={"cpf": "12345678901"})
    assert response.status_code == 200
    assert "token" in response.json()


def test_make_invalid_token():
    response = client.post("/tokens", json={"cpf": "123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "CPF inválido"


# ------------------------------------------------------
# Testes do endpoint GET /tokens/validate
# ------------------------------------------------------
def test_validar_token_sucesso():
    token = create_token("12345678901")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/tokens/validate", headers=headers)

    assert response.status_code == 200
    json = response.json()
    assert json["valid"] is True
    assert json["data"]["cpf"] == "12345678901"


def test_validate_invalid_token():
    headers = {"Authorization": "Bearer token_invalido"}

    response = client.get("/tokens/validate", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido"


def test_expired_token():
    token = create_token("12345678901", minutes=-1)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/tokens/validate", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Token expirado"
