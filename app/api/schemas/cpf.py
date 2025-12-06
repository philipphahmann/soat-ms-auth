from pydantic import BaseModel


class CpfRequest(BaseModel):
    cpf: str
