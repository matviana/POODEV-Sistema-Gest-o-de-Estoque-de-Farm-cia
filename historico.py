
"""
historico.py

Responsabilidades:
- criar a tabela de histórico de movimentações de estoque
- registrar movimentações (entrada, saída, reposição automática, compra, venda, ...)
- consultar histórico (todas, por medicamento, por período, por tipo)

Depende de: database.conectar_banco()
"""

from database import conectar_banco
from datetime import datetime
from typing import List, Tuple, Optional


def criar_tabela_historico():
    """
    Cria a tabela historico_estoque caso não exista.
    Chame essa função a partir de criar_tabelas() em database.py.
    """
    sql = """
    CREATE TABLE IF NOT EXISTS historico_estoque (
        idh SERIAL PRIMARY KEY,
        codigo_barras VARCHAR(50),
        nome_medicamento VARCHAR(200),
        tipo_movimentacao VARCHAR(50), -- e.g. 'ENTRADA','SAIDA','REPOSICAO_AUTOMATICA','COMPRA','VENDA'
        quantidade INT,
        estoque_antes INT,
        estoque_depois INT,
        data_hora TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
        observacao TEXT
    );
    """
    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
        print("Tabela 'historico_estoque' criada/verificada com sucesso.")
    except Exception as e:
        print("Erro ao criar tabela historico_estoque:", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def registrar_movimentacao(
    codigo_barras: Optional[str],
    nome_medicamento: str,
    tipo_movimentacao: str,
    quantidade: int,
    estoque_antes: Optional[int],
    estoque_depois: Optional[int],
    observacao: Optional[str] = None
) -> bool:
    """
    Registra uma movimentação no histórico.
    Retorna True se gravou com sucesso, False caso contrário.

    Parâmetros:
    - codigo_barras: código do produto (pode ser None)
    - nome_medicamento: nome (para facilitar relatórios)
    - tipo_movimentacao: string curta indicando o tipo (ENTRADA, SAIDA, REPOSICAO_AUTOMATICA, COMPRA, VENDA)
    - quantidade: quantidade movimentada (positivo)
    - estoque_antes: quantidade antes da movimentação (pode ser None)
    - estoque_depois: quantidade depois da movimentação (pode ser None)
    - observacao: texto adicional opcional
    """
    sql = """
    INSERT INTO historico_estoque (
        codigo_barras, nome_medicamento, tipo_movimentacao,
        quantidade, estoque_antes, estoque_depois, data_hora, observacao
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                now = datetime.utcnow()
                cur.execute(sql, (
                    codigo_barras,
                    nome_medicamento,
                    tipo_movimentacao,
                    quantidade,
                    estoque_antes,
                    estoque_depois,
                    now,
                    observacao
                ))
                newid = cur.fetchone()
        return bool(newid)
    except Exception as e:
        print("Erro ao registrar movimentação no histórico:", e)
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()


def consultar_todas(limit: int = 100) -> List[Tuple]:
    """
    Retorna as últimas 'limit' entradas do histórico (ordenadas por data desc).
    """
    sql = "SELECT id, codigo_barras, nome_medicamento, tipo_movimentacao, quantidade, estoque_antes, estoque_depois, data_hora, observacao FROM historico_estoque ORDER BY data_hora DESC LIMIT %s;"
    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (limit,))
                rows = cur.fetchall()
        return rows
    except Exception as e:
        print("Erro ao consultar histórico completo:", e)
        return []
    finally:
        if conn:
            conn.close()


def consultar_por_medicamento(codigo_barras: str, limit: int = 100) -> List[Tuple]:
    """
    Retorna histórico filtrado por código de barras (mais recentes primeiro).
    """
    sql = """
    SELECT id, codigo_barras, nome_medicamento, tipo_movimentacao, quantidade,
           estoque_antes, estoque_depois, data_hora, observacao
    FROM historico_estoque
    WHERE codigo_barras = %s
    ORDER BY data_hora DESC
    LIMIT %s;
    """
    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (codigo_barras, limit))
                rows = cur.fetchall()
        return rows
    except Exception as e:
        print("Erro ao consultar histórico por medicamento:", e)
        return []
    finally:
        if conn:
            conn.close()


def consultar_por_periodo(data_inicio: datetime, data_fim: datetime, limit: int = 1000) -> List[Tuple]:
    """
    Retorna histórico entre data_inicio e data_fim (inclusive).
    data_inicio e data_fim devem ser objetos datetime (UTC recomendado).
    """
    sql = """
    SELECT id, codigo_barras, nome_medicamento, tipo_movimentacao, quantidade,
           estoque_antes, estoque_depois, data_hora, observacao
    FROM historico_estoque
    WHERE data_hora BETWEEN %s AND %s
    ORDER BY data_hora DESC
    LIMIT %s;
    """
    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data_inicio, data_fim, limit))
                rows = cur.fetchall()
        return rows
    except Exception as e:
        print("Erro ao consultar histórico por período:", e)
        return []
    finally:
        if conn:
            conn.close()


def consultar_por_tipo(tipo_movimentacao: str, limit: int = 100) -> List[Tuple]:
    """
    Retorna histórico filtrado por tipo de movimentação (ENTRADA, SAIDA, REPOSICAO_AUTOMATICA, COMPRA, VENDA).
    """
    sql = """
    SELECT id, codigo_barras, nome_medicamento, tipo_movimentacao, quantidade,
           estoque_antes, estoque_depois, data_hora, observacao
    FROM historico_estoque
    WHERE tipo_movimentacao = %s
    ORDER BY data_hora DESC
    LIMIT %s;
    """
    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (tipo_movimentacao, limit))
                rows = cur.fetchall()
        return rows
    except Exception as e:
        print("Erro ao consultar histórico por tipo:", e)
        return []
    finally:
        if conn:
            conn.close()
