from fastapi import APIRouter, Query
from backend.historico import (
    consultar_todas,
    consultar_por_medicamento,
    consultar_por_tipo,
    consultar_mais_vendidos_mes
)

router = APIRouter(prefix="/historico", tags=["Histórico"])


@router.get("/movimentacoes")
def listar_historico(
    tipo: str | None = Query(default=None, description="Filtrar por tipo de movimentação"),
    codigo_barras: str | None = Query(default=None, description="Filtrar por código de barras do medicamento"),
    limite: int = Query(default=200, gt=0, le=1000, description="Número máximo de registros retornados")
):
    """
    Retorna todas as movimentações registradas no sistema.
    Pode filtrar por tipo ou código de barras do medicamento.
    """
    if tipo:
        registros = consultar_por_tipo(tipo, limit=limite)
    elif codigo_barras:
        registros = consultar_por_medicamento(codigo_barras, limit=limite)
    else:
        registros = consultar_todas(limit=limite)

    resultado = []
    for mov in registros:
        idh, codigo, nome, tipo_mov, quantidade, estoque_antes, estoque_depois, datahora, obs = mov

        resultado.append({
            "id": idh,
            "codigo_barras": codigo,
            "nome": nome,
            "tipo": tipo_mov,
            "quantidade": quantidade,
            "estoque_antes": estoque_antes,
            "estoque_depois": estoque_depois,
            "datahora": str(datahora),
            "observacao": obs
        })

    return {"total": len(resultado), "movimentacoes": resultado}


@router.get("/mais_vendidos")
def mais_vendidos(
    mes: int | None = Query(None, ge=1, le=12, description="Mês desejado (1-12)"),
    ano: int | None = Query(None, ge=2000, description="Ano desejado (ex: 2025)")
):
    """
    Retorna os medicamentos mais vendidos no mês/ano especificado.
    Se não informado, utiliza o mês e ano atual.
    """
    registros = consultar_mais_vendidos_mes(mes, ano)
    resultado = [{"nome": nome, "total_vendido": total} for nome, total in registros]

    return {"total": len(resultado), "mais_vendidos": resultado}
