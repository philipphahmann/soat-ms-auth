from datetime import datetime, timezone

class CPF:
    def __init__(self, value: str):
        # Regra de validação de CPF movida para cá
        import re
        clean_value = re.sub(r"\D", "", value)
        if len(clean_value) != 11 or not clean_value.isdigit():
            raise ValueError("CPF inválido")
        self.value = clean_value

class Token:
    def __init__(self, cpf: str, access_token: str, expires_at: int, source: str = "generated"):
        self.cpf = cpf
        self.access_token = access_token
        self.expires_at = expires_at
        self.source = source

    def is_expired(self) -> bool:
        now_ts = int(datetime.now(timezone.utc).timestamp())
        return self.expires_at <= now_ts