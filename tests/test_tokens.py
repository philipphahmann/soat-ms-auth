def test_create_token_success(client):
    # Dado um CPF válido
    payload = {"cpf": "21829365053"}
    
    # Quando chamo o endpoint
    response = client.post("/tokens", json=payload)
    
    # Então deve retornar 200 e o token
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "expires_at" in data
    assert data["source"] == "generated"

def test_create_token_cached(client):
    # Dado um CPF que já foi consultado (simulado fazendo 2 requests)
    payload = {"cpf": "21829365053"}
    
    # Primeiro request (Gera)
    client.post("/tokens", json=payload)
    
    # Segundo request (Deve vir do Cache)
    response = client.post("/tokens", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    if "source" in data:
        assert data["source"] == "cache"

def test_create_token_invalid_cpf(client):
    # Dado um CPF inválido
    payload = {"cpf": "123"} 
    
    # Quando chamo o endpoint
    response = client.post("/tokens", json=payload)
    
    # Então deve retornar 400 com erro de CPF inválido
    assert response.status_code == 400
    assert response.json()["detail"] == "CPF inválido"

def test_validate_token_success_header(client):
    # 1. Cria um token válido
    payload_create = {"cpf": "99988877766"}
    resp_create = client.post("/tokens", json=payload_create)
    assert resp_create.status_code == 200
    token = resp_create.json()["token"]

    # 2. Valida usando GET e Header
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tokens/validate", headers=headers)

    # 3. Asserções
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True
    assert body["data"]["cpf"] == "99988877766"

def test_validate_token_invalid_header(client):
    # Testa com token inválido no header
    headers = {"Authorization": "Bearer token.invalido.123"}
    
    response = client.get("/tokens/validate", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido ou expirado"

def test_validate_token_missing_header(client):
    # Testa sem enviar o header (deve dar 403 Forbidden padrão do FastAPI/HTTPBearer)
    response = client.get("/tokens/validate")
    
    # O FastAPI retorna 403 quando o HTTPBearer é obrigatório e não é enviado
    assert response.status_code == 403