from pydantic import BaseModel

class FarmaciaCreate(BaseModel):
    nome: str
    endereco: str
    telefone: str
    cnpj: str
