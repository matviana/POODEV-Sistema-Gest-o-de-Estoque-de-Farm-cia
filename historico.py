
from database import conectar_banco
from datetime import datetime
from typing import List, Tuple, Optional

"""
historico.py
Compatível com a tabela historico_movimentacoes criada em database.py
"""


def registrar_movimentacao(
    id_medicamento: int,
    tipo: str,
    quantidade: int,
    observacao: Optional[str] = None
) -> bool:
    """
    Registra uma movimentação no histórico.
    Tabela utilizada: historico_movimentacoes

    Campos disponíveis:
    - id_medicamento  (INT, FK)
    - tipo            (entrada/saida)
    - quantidade
    - data_movimento
    - observacao
    """

    sql = """
        INSERT INTO historico_movimentacoes
        (id_medicamento, tipo, quantidade, observacao)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """

    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (id_medicamento, tipo, quantidade, observacao))
                cur.fetchone()
        return True

    except Exception as e:
        print("Erro ao registrar movimentação no histórico:", e)
        if conn:
            conn.rollback()
        return False

    finally:
        if conn:
            conn.close()


def consultar_todas(limit: int = 200) -> List[Tuple]:
    """
    Retorna todas as movimentações do histórico.
    Junta a tabela medicamentos para buscar nome e código de barras.
    """

    sql = """
        SELECT
            h.id,
            m.codigo_barras,
            m.nome,
            h.tipo,
            h.quantidade,
            NULL AS estoque_antes,
            NULL AS estoque_depois,
            h.data_movimento,
            h.observacao
        FROM historico_movimentacoes h
        JOIN medicamentos m ON m.id = h.id_medicamento
        ORDER BY h.data_movimento DESC
        LIMIT %s;
    """

    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (limit,))
                return cur.fetchall()

    except Exception as e:
        print("Erro ao consultar histórico completo:", e)
        return []

    finally:
        if conn:
            conn.close()


def consultar_por_medicamento(codigo_barras: str, limit: int = 100) -> List[Tuple]:
    """
    Histórico filtrado por código de barras.
    """

    sql = """
        SELECT
            h.id,
            m.codigo_barras,
            m.nome,
            h.tipo,
            h.quantidade,
            NULL AS estoque_antes,
            NULL AS estoque_depois,
            h.data_movimento,
            h.observacao
        FROM historico_movimentacoes h
        JOIN medicamentos m ON m.id = h.id_medicamento
        WHERE m.codigo_barras = %s
        ORDER BY h.data_movimento DESC
        LIMIT %s;
    """

    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (codigo_barras, limit))
                return cur.fetchall()

    except Exception as e:
        print("Erro ao consultar histórico por medicamento:", e)
        return []

    finally:
        if conn:
            conn.close()


def consultar_por_tipo(tipo: str, limit: int = 100) -> List[Tuple]:
    """
    Histórico filtrado por tipo (entrada ou saída).
    """

    sql = """
        SELECT
            h.id,
            m.codigo_barras,
            m.nome,
            h.tipo,
            h.quantidade,
            NULL AS estoque_antes,
            NULL AS estoque_depois,
            h.data_movimento,
            h.observacao
        FROM historico_movimentacoes h
        JOIN medicamentos m ON m.id = h.id_medicamento
        WHERE h.tipo = %s
        ORDER BY h.data_movimento DESC
        LIMIT %s;
    """

    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (tipo, limit))
                return cur.fetchall()

    except Exception as e:
        print("Erro ao consultar histórico por tipo:", e)
        return []

    finally:
        if conn:
            conn.close()
