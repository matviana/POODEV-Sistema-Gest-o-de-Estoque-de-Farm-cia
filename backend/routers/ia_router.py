from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from backend.redeneural import RedeNeuralDemanda

router = APIRouter(prefix="/ia", tags=["Inteligência Artificial"])


# ---------------- MODELOS ---------------- #

class TreinamentoIn(BaseModel):
    vendas_mensais: List[float]   # 12 valores
    eventos_mensais: List[float]  # 12 valores entre 0 e 1


class PrevisaoDemandaIn(BaseModel):
    ultimos_3_meses: List[float]  # 3 valores
    mes_atual: int
    intensidade_evento: float


class TreinarMedicamentoIn(BaseModel):
    nome_medicamento: str
    vendas_mensais: List[float]     # 12 valores
    eventos_mensais: List[float]    # 12 valores entre 0 e 1


class PreverMedicamentoIn(BaseModel):
    nome_medicamento: str
    ultimos_3_meses: List[float]
    mes_atual: int
    intensidade_evento: float


# ---------------- ROTAS GERAIS ---------------- #

@router.post("/treinar")
def treinar_modelo(payload: TreinamentoIn):
    if len(payload.vendas_mensais) != 12:
        raise HTTPException(status_code=400, detail="vendas_mensais deve conter 12 valores")

    if len(payload.eventos_mensais) != 12:
        raise HTTPException(status_code=400, detail="eventos_mensais deve conter 12 valores")

    try:
        ia = RedeNeuralDemanda()
        ia.treinar_com_eventos(payload.vendas_mensais, payload.eventos_mensais)
        return {"status": "Modelo geral treinado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/prever_demanda")
def prever_demanda(payload: PrevisaoDemandaIn):
    try:
        ia = RedeNeuralDemanda()
        previsao = ia.prever_proximo_mes_eventos(
            payload.ultimos_3_meses,
            payload.mes_atual,
            payload.intensidade_evento
        )
        return {"previsao_demanda": round(previsao, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- ROTAS POR MEDICAMENTO ---------------- #

@router.post("/treinar_medicamento")
def treinar_medicamento(payload: TreinarMedicamentoIn):
    if len(payload.vendas_mensais) != 12:
        raise HTTPException(status_code=400, detail="vendas_mensais deve conter 12 valores")

    if len(payload.eventos_mensais) != 12:
        raise HTTPException(status_code=400, detail="eventos_mensais deve conter 12 valores")

    try:
        RedeNeuralDemanda.treinar_medicamento(
            payload.nome_medicamento,
            payload.vendas_mensais,
            payload.eventos_mensais
        )
        return {"status": f"Modelo do medicamento '{payload.nome_medicamento}' treinado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/prever_medicamento")
def prever_medicamento(payload: PreverMedicamentoIn):
    if len(payload.ultimos_3_meses) != 3:
        raise HTTPException(status_code=400, detail="ultimos_3_meses precisa de 3 valores")

    try:
        previsao = RedeNeuralDemanda.prever_medicamento(
            payload.nome_medicamento,
            payload.ultimos_3_meses,
            payload.mes_atual,
            payload.intensidade_evento
        )
        return {
            "medicamento": payload.nome_medicamento,
            "previsao_demanda": round(previsao, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
