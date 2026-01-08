import boto3
from datetime import datetime, timezone
from app.settings import settings

class DynamoService:
    def __init__(self):
        self.client = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
        self.table = self.client.Table(settings.DYNAMODB_TABLE)

    def get_token(self, cpf: str):
        try:
            response = self.table.get_item(Key={'cpf': cpf})
            item = response.get('Item')
            
            if item:
                now_ts = int(datetime.now(timezone.utc).timestamp())
                if item.get('expires_at') > now_ts:
                    return item
            return None
        except Exception as e:
            print(f"Erro ao buscar no DynamoDB: {e}")
            return None

    def save_token(self, cpf: str, token: str, expires_at: int):
        try:
            self.table.put_item(
                Item={
                    'cpf': cpf,
                    'token': token,
                    'expires_at': expires_at
                }
            )
        except Exception as e:
            print(f"Erro ao salvar no DynamoDB: {e}")