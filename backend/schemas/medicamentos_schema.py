from pydantic import BaseModel
from datetime import date

class MedicamentoBase(BaseModel):
    nome: str
    lote: str | None = None
    validade: date | None = None
    quantidade_minima: int = 0
    codigo_barras: str
    quantidade_estoque: int = 0
    receita_obrigatoria: bool = False

class MedicamentoCreate(MedicamentoBase):
    pass

class MedicamentoUpdate(BaseModel):
    nome: str | None = None
    lote: str | None = None
    validade: date | None = None
    quantidade_minima: int | None = None
    codigo_barras: str | None = None
    quantidade_estoque: int | None = None
    receita_obrigatoria: bool | None = None

class MedicamentoResponse(MedicamentoBase):
    id: int

    class Config:
        from_attributes = True   # substitui orm_mode
