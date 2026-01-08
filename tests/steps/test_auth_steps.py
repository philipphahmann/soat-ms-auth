import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from app.main import app

scenarios('../features/auth.feature')

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def context():
    return {}

@given(parsers.parse('que possuo um CPF válido "{cpf}"'))
def cpf_valido(context, cpf):
    context['payload'] = {"cpf": cpf}

@when('eu solicito a criação de um token para este CPF')
def solicitar_token(client, context):
    response = client.post("/tokens", json=context['payload'])
    context['response'] = response

@then(parsers.parse('o sistema deve retornar o código de status {status_code:d}'))
def verificar_status(context, status_code):
    assert context['response'].status_code == status_code

@then('a resposta deve conter um token de acesso')
def verificar_token(context):
    assert "token" in context['response'].json()