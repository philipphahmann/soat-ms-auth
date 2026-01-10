from pydantic import BaseModel

class CpfRequest(BaseModel):
    cpf: str

class TokenValidationRequest(BaseModel):
    token: str