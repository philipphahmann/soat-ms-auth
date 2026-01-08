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