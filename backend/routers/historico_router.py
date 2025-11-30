from fastapi import APIRouter
from backend.historico import consultar_todas

router = APIRouter(prefix="/historico", tags=["Histórico"])

@router.get("/movimentacoes")
def listar_historico():
    """
    Retorna todas as movimentações registradas no sistema.
    """
    registros = consultar_todas()

    resultado = []
    for mov in registros:
        idh, codigo, nome, tipo, quantidade, antes, depois, datahora, obs = mov

        resultado.append({
            "id": idh,
            "codigo_barras": codigo,
            "nome": nome,
            "tipo": tipo,
            "quantidade": quantidade,
            "antes": antes,
            "depois": depois,
            "datahora": str(datahora),
            "observacao": obs
        })

    return {"total": len(resultado), "movimentacoes": resultado}
