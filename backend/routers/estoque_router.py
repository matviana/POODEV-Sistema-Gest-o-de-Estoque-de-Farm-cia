from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from backend.database import get_db_connection
from backend.historico import registrar_movimentacao   

router = APIRouter(prefix="/estoque", tags=["Estoque"])


class MovimentacaoIn(BaseModel):
    codigo_barras: str
    quantidade: int
    observacao: str | None = None
    caminho_receita: str | None = None



# Entrada de estoque(+)

@router.post("/entrada")
def entrada_estoque(payload: MovimentacaoIn):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, quantidade_estoque FROM medicamentos WHERE codigo_barras = %s;",
            (payload.codigo_barras,)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Medicamento não encontrado")

        id_med, estoque_atual = row
        novo_estoque = estoque_atual + payload.quantidade

        cur.execute(
            "UPDATE medicamentos SET quantidade_estoque = %s WHERE id = %s;",
            (novo_estoque, id_med)
        )
        conn.commit()

        #  REGISTRO DE HISTÓRICO 
        registrar_movimentacao(
            id_medicamento=id_med,
            tipo="entrada",
            quantidade=payload.quantidade,
            estoque_antes=estoque_atual,
            estoque_depois=novo_estoque,
            observacao=payload.observacao
        )

        return {"mensagem": "Entrada registrada", "id": id_med, "novo_estoque": novo_estoque}
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()



# saída de estoque

@router.post("/saida")
def saida_estoque(payload: MovimentacaoIn):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, quantidade_estoque, receita_obrigatoria FROM medicamentos WHERE codigo_barras = %s;",
            (payload.codigo_barras,)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Medicamento não encontrado")

        id_med, estoque_atual, exige_receita = row

        if exige_receita and not payload.caminho_receita:
            raise HTTPException(status_code=400, detail="Receita obrigatória para este medicamento")

        if payload.quantidade > estoque_atual:
            raise HTTPException(status_code=400, detail="Quantidade solicitada maior que o estoque atual")

        novo_estoque = estoque_atual - payload.quantidade

        cur.execute(
            "UPDATE medicamentos SET quantidade_estoque = %s WHERE id = %s;",
            (novo_estoque, id_med)
        )
        conn.commit()

        #  registro de historico 
        registrar_movimentacao(
            id_medicamento=id_med,
            tipo="saida",
            quantidade=payload.quantidade,
            estoque_antes=estoque_atual,
            estoque_depois=novo_estoque,
            observacao=payload.observacao
        )

        return {"mensagem": "Saída registrada", "id": id_med, "novo_estoque": novo_estoque}
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()



# Alertas

@router.get("/alertas")
def alertas_reposicao():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, nome, codigo_barras, quantidade_estoque, quantidade_minima
            FROM medicamentos
            WHERE quantidade_estoque <= quantidade_minima
            ORDER BY nome;
        """)
        rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "nome": r[1],
                "codigo_barras": r[2],
                "quantidade_estoque": r[3],
                "quantidade_minima": r[4],
            } for r in rows
        ]
    finally:
        conn.close()



# Estoque baixo

@router.get("/baixo")
def verificar_estoque_baixo(
    threshold: int | None = Query(None),
    porcentagem: float | None = Query(None)
):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, nome, codigo_barras, quantidade_estoque, quantidade_minima
            FROM medicamentos
            ORDER BY nome;
        """)
        rows = cur.fetchall()
        resultados = []

        for r in rows:
            id_med, nome, cod, estoque, qtd_min = r
            limite = (
                threshold if threshold is not None else
                int(qtd_min * porcentagem / 100) if porcentagem is not None else
                qtd_min
            )

            if estoque <= limite:
                resultados.append({
                    "id": id_med,
                    "nome": nome,
                    "codigo_barras": cod,
                    "quantidade_estoque": estoque,
                    "quantidade_minima": qtd_min,
                    "limite_usado": limite
                })

        return resultados
    finally:
        conn.close()



# Reposição automática

@router.post("/repor_automatico")
def repor_automatico():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, quantidade_estoque, quantidade_minima
            FROM medicamentos
            WHERE quantidade_estoque <= quantidade_minima;
        """)
        rows = cur.fetchall()
        if not rows:
            return {"mensagem": "Nenhum medicamento precisa repor agora.", "repostos": 0}

        repostos = []
        for id_med, estoque_atual, qtd_min in rows:
            nova_qtd = max(qtd_min * 2, estoque_atual + qtd_min)

            cur.execute("UPDATE medicamentos SET quantidade_estoque = %s WHERE id = %s;", (nova_qtd, id_med))

            registrar_movimentacao(
                id_medicamento=id_med,
                tipo="repor",
                quantidade=nova_qtd - estoque_atual,
                estoque_antes=estoque_atual,
                estoque_depois=nova_qtd,
                observacao="Reposição automática"
            )

            repostos.append({"id": id_med, "novo_estoque": nova_qtd})

        conn.commit()
        return {"mensagem": "Reposição automática realizada", "repostos": repostos}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
