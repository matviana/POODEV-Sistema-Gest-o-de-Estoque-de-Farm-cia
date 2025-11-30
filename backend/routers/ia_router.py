from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from backend.redeneural import RedeNeuralDemanda

router = APIRouter(prefix="/ia", tags=["Inteligência Artificial"])

class PrevisaoDemandaIn(BaseModel):
    ultimos_3_meses: List[float]  # validação manual depois
    mes_atual: int  # 1 a 12
    intensidade_evento: float  # 0 a 1

@router.post("/prever_demanda")
def prever_demanda(payload: PrevisaoDemandaIn):
    """
    Previsão de demanda futura considerando:
    - últimos 3 meses de vendas
    - mês atual (sazonalidade)
    - intensidade de evento epidemiológico
    """

    # Validações manuais
    if len(payload.ultimos_3_meses) != 3:
        raise HTTPException(status_code=400, detail="ultimos_3_meses deve conter exatamente 3 valores")
    if payload.mes_atual < 1 or payload.mes_atual > 12:
        raise HTTPException(status_code=400, detail="mes_atual deve estar entre 1 e 12")
    if payload.intensidade_evento < 0 or payload.intensidade_evento > 1:
        raise HTTPException(status_code=400, detail="intensidade_evento deve estar entre 0 e 1")

    try:
        ia = RedeNeuralDemanda()
        previsao = ia.prever_proximo_mes_eventos(
            ultimos_3_meses=payload.ultimos_3_meses,
            mes_atual=payload.mes_atual,
            intensidade_evento=payload.intensidade_evento
        )
        return {"previsao_demanda": round(previsao, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
