from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/auth.feature')

@given(parsers.parse('que possuo um cpf válido "{cpf}"'), target_fixture="cpf_payload")
def set_cpf(cpf):
    return {"cpf": cpf}

@when('eu solicito a criação de um token para este CPF', target_fixture="response")
def request_token(client, cpf_payload):
    return client.post("/tokens", json=cpf_payload)

@then(parsers.parse('o sistema deve retornar o código de status {status_code:d}'))
def check_status(response, status_code):
    assert response.status_code == status_code

@then('a resposta deve conter um token de acesso')
def check_token(response):
    data = response.json()
    assert "token" in data
    assert len(data["token"]) > 10