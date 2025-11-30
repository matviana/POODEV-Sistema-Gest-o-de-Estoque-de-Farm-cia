import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import shutil

load_dotenv()

DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = int(os.getenv("PG_PORT", 5432))
DB_NAME = os.getenv("PG_DB", "farmacia_db")
DB_USER = os.getenv("PG_USER", "postgres")
DB_PASS = os.getenv("PG_PASS", "matale123")

def conectar_banco():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )




def criar_tabelas():
    create_medicamentos = """
    CREATE TABLE IF NOT EXISTS medicamentos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        lote VARCHAR(50),
        validade DATE,
        quantidade_minima INT DEFAULT 0,
        codigo_barras VARCHAR(50) UNIQUE,
        quantidade_estoque INT DEFAULT 0,
        receita_obrigatoria BOOLEAN DEFAULT FALSE
    );
    """

    create_farmacias = """
    CREATE TABLE IF NOT EXISTS farmacias (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        endereco VARCHAR(200),
        telefone VARCHAR(20),
        cnpj VARCHAR(20) UNIQUE NOT NULL
    );
    """

    create_historico = """
    CREATE TABLE IF NOT EXISTS historico_movimentacoes (
        id SERIAL PRIMARY KEY,
        id_medicamento INT NOT NULL REFERENCES medicamentos(id) ON DELETE CASCADE,
        tipo VARCHAR(20) NOT NULL,
        quantidade INT NOT NULL,
        estoque_antes INT,
        estoque_depois INT,
        data_movimento TIMESTAMP DEFAULT NOW(),
        observacao TEXT,
        caminho_receita TEXT
    );
"""




    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(create_medicamentos)
                cur.execute(create_farmacias)
                cur.execute(create_historico)
        print("Tabelas criadas/verificadas com sucesso.")
    except Exception as e:
        print("Erro ao criar tabelas:", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def registrar_historico(id_medicamento, tipo, quantidade, observacao=None, caminho_receita=None):
    query = """
        INSERT INTO historico_movimentacoes
        (id_medicamento, tipo, quantidade, observacao, caminho_receita)
        VALUES (%s, %s, %s, %s, %s);
    """

    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    id_medicamento,
                    tipo,
                    quantidade,
                    observacao,
                    caminho_receita
                ))
    except Exception as e:
        print("Erro ao registrar histórico:", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def salvar_receita_medicamento(caminho_origem, caminho_destino):
    try:
        shutil.copy(caminho_origem, caminho_destino)
        return True
    except Exception as e:
        print("Erro ao salvar arquivo da receita:", e)
        return False
    
    
def get_db_connection():
    return conectar_banco()


