import os
import pytest
from unittest.mock import MagicMock, patch

# 1. Configurar variáveis de ambiente ANTES de importar a aplicação
# Isso evita que o boto3 tente procurar credenciais reais e falhe na inicialização
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["DYNAMODB_TABLE"] = "auth_tokens_test"

# 2. Mockar o boto3 resource para não tentar conectar na AWS de verdade
with patch("boto3.resource") as mock_boto:
    from app.main import app
    from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_dynamo_service():
    """
    Mock para o serviço do DynamoDB.
    Interceptamos a instância que já foi criada no arquivo app/api/tokens.py
    """
    with patch("app.api.tokens.dynamo_service") as mock:
        yield mock