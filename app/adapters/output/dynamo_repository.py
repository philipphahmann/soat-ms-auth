import boto3
from app.settings import settings
from app.domain.ports.repositories import TokenRepository
from app.domain.entities import Token

class DynamoDBTokenRepository(TokenRepository):
    def __init__(self):
        self.client = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
        self.table = self.client.Table(settings.DYNAMODB_TABLE)

    def get_by_cpf(self, cpf: str) -> Token | None:
        try:
            response = self.table.get_item(Key={'cpf': cpf})
            item = response.get('Item')
            if item:
                return Token(
                    cpf=item['cpf'],
                    access_token=item['token'],
                    expires_at=int(item['expires_at'])
                )
            return None
        except Exception as e:
            print(f"Erro Dynamo: {e}")
            return None

    def save(self, token: Token) -> None:
        try:
            self.table.put_item(
                Item={
                    'cpf': token.cpf,
                    'token': token.access_token,
                    'expires_at': token.expires_at
                }
            )
        except Exception as e:
            print(f"Erro salvar Dynamo: {e}")