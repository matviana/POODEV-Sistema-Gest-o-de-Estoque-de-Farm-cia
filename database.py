
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from dotenv import load_dotenv


load_dotenv() 


DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = int(os.getenv("PG_PORT", 5432))
DB_NAME = os.getenv("PG_DB", "farmacia_db")
DB_USER = os.getenv("PG_USER", "postgres")
DB_PASS = os.getenv("PG_PASS", "matale123")

def conectar_banco():
    """Retorna uma conexão psycopg2. Chame close() depois."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def criar_tabelas():
    """
    Cria tabelas essenciais: medicamentos e farmacias.
    """
    create_medicamentos = """
    CREATE TABLE IF NOT EXISTS medicamentos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        lote VARCHAR(50),
        validade DATE,
        quantidade_minima INT DEFAULT 0,
        codigo_barras VARCHAR(50) UNIQUE,
        quantidade_estoque INT DEFAULT 0
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

    conn = None
    try:
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(create_medicamentos)
                cur.execute(create_farmacias)
        print("Tabelas 'medicamentos' e 'farmacias' criadas/verificadas com sucesso.")
    except Exception as e:
        print(" Erro ao criar tabelas:", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

