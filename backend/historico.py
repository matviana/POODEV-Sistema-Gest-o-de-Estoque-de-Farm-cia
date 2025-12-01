
from backend.database import conectar_banco
from datetime import datetime
from typing import List, Tuple, Optional


def registrar_movimentacao(
    id_medicamento: int,
    tipo: str,
    quantidade: int,
    estoque_antes: Optional[int] = None,
    estoque_depois: Optional[int] = None,
    observacao: Optional[str] = None,
    caminho_receita: Optional[str] = None
) -> bool:
    """
    Registra uma movimentação no histórico, agora com suporte a estoque antes/depois.
    """
    sql = """
        INSERT INTO historico_movimentacoes
        (id_medicamento, tipo, quantidade, estoque_antes, estoque_depois, observacao, caminho_receita)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """

    conn = conectar_banco()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (
                id_medicamento,
                tipo,
                quantidade,
                estoque_antes,
                estoque_depois,
                observacao,
                caminho_receita
            ))
            cur.fetchone()
        conn.commit()  # garante que o registro seja salvo
        return True

    except Exception as e:
        print("ERRO registrar_movimentacao:", e)
        conn.rollback()
        return False

    finally:
        conn.close()


def consultar_todas(limit: int = 200) -> List[Tuple]:
    """
    Retorna todas as movimentações do histórico, incluindo nome e código de barras do medicamento.
    """
    sql = """
        SELECT
            h.id,
            m.codigo_barras,
            m.nome,
            h.tipo,
            h.quantidade,
            h.estoque_antes,
            h.estoque_depois,
            h.data_movimento,
            h.observacao
        FROM historico_movimentacoes h
        JOIN medicamentos m ON m.id = h.id_medicamento
        ORDER BY h.data_movimento DESC
        LIMIT %s;
    """

    conn = conectar_banco()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()
    except Exception as e:
        print("ERRO consultar_todas:", e)
        return []
    finally:
        conn.close()


def consultar_por_medicamento(codigo_barras: str, limit: int = 100) -> List[Tuple]:
    sql = """
        SELECT
            h.id,
            m.codigo_barras,
            m.nome,
            h.tipo,
            h.quantidade,
            h.estoque_antes,
            h.estoque_depois,
            h.data_movimento,
            h.observacao
        FROM historico_movimentacoes h
        JOIN medicamentos m ON m.id = h.id_medicamento
        WHERE m.codigo_barras = %s
        ORDER BY h.data_movimento DESC
        LIMIT %s;
    """

    conn = conectar_banco()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (codigo_barras, limit))
            return cur.fetchall()
    except Exception as e:
        print("ERRO consultar_por_medicamento:", e)
        return []
    finally:
        conn.close()


def consultar_por_tipo(tipo: str, limit: int = 100) -> List[Tuple]:
    sql = """
        SELECT
            h.id,
            m.codigo_barras,
            m.nome,
            h.tipo,
            h.quantidade,
            h.estoque_antes,
            h.estoque_depois,
            h.data_movimento,
            h.observacao
        FROM historico_movimentacoes h
        JOIN medicamentos m ON m.id = h.id_medicamento
        WHERE h.tipo = %s
        ORDER BY h.data_movimento DESC
        LIMIT %s;
    """

    conn = conectar_banco()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (tipo, limit))
            return cur.fetchall()
    except Exception as e:
        print("ERRO consultar_por_tipo:", e)
        return []
    finally:
        conn.close()


def consultar_mais_vendidos_mes(mes=None, ano=None):
    if mes is None:
        mes = datetime.today().month
    if ano is None:
        ano = datetime.today().year

    sql = """
        SELECT 
            m.nome,
            SUM(h.quantidade) AS total_vendido
        FROM historico_movimentacoes h
        JOIN medicamentos m ON m.id = h.id_medicamento
        WHERE h.tipo = 'saida'
          AND EXTRACT(MONTH FROM h.data_movimento) = %s
          AND EXTRACT(YEAR FROM h.data_movimento) = %s
        GROUP BY m.nome
        ORDER BY total_vendido DESC;
    """

    conn = conectar_banco()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (mes, ano))
            return cur.fetchall()
    finally:
        conn.close()
