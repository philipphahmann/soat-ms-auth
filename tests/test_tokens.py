from datetime import datetime, timezone

def test_make_token_success_cache_miss(client, mock_dynamo_service):
    """
    Cenário: Token não existe no DynamoDB.
    Espera-se: Criar novo token, salvar no banco e retornar source='generated'.
    """
    # Configura o Mock para retornar None (como se não achasse nada no banco)
    mock_dynamo_service.get_token.return_value = None

    response = client.post("/tokens", json={"cpf": "86021414080"})

    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["source"] == "generated"
    
    # Verifica se o método save_token foi chamado corretamente
    mock_dynamo_service.save_token.assert_called_once()


def test_make_token_success_cache_hit(client, mock_dynamo_service):
    """
    Cenário: Token JÁ existe no DynamoDB e é válido.
    Espera-se: Retornar o token do banco e retornar source='cache'.
    """
    # Configura o Mock para retornar um item simulado
    fake_token = "token_mockado_do_banco"
    fake_expiry = int(datetime.now(timezone.utc).timestamp()) + 600
    
    mock_dynamo_service.get_token.return_value = {
        "token": fake_token,
        "expires_at": fake_expiry
    }

    response = client.post("/tokens", json={"cpf": "86021414080"})

    assert response.status_code == 200
    data = response.json()
    assert data["token"] == fake_token
    assert data["source"] == "cache"
    
    # Verifica que save_token NÃO foi chamado (pois pegou do cache)
    mock_dynamo_service.save_token.assert_not_called()


def test_make_invalid_token(client):
    response = client.post("/tokens", json={"cpf": "123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "CPF inválido"


# Testes do endpoint GET /tokens/validate (mantidos similares, mas usando client fixture)
def test_validar_token_sucesso(client):
    # Precisamos gerar um token válido real para passar na validação do JWT
    from app.core.security import criar_jwt
    token, _ = criar_jwt("86021414080")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tokens/validate", headers=headers)

    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["valid"] is True
    assert json_resp["data"]["cpf"] == "86021414080"

def test_validate_invalid_token(client):
    headers = {"Authorization": "Bearer token_invalido"}
    response = client.get("/tokens/validate", headers=headers)
    assert response.status_code == 401

def test_expired_token(client):
    # Criar token expirado manualmente para teste
    import jwt
    from app.settings import settings
    from datetime import timedelta
    
    payload = {
        "cpf": "86021414080",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1), # Passado
        "iat": datetime.now(timezone.utc) - timedelta(minutes=10),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tokens/validate", headers=headers)
    assert response.status_code == 401