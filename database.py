import psycopg2

def conectar_banco():
    return psycopg2.connect(
        host="localhost",
        database="farmacia_db",
        user="postgres",
        password="sua_senha",
        port=5432
    )

def criar_tabelas():
    conn = conectar_banco()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicamento (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            lote VARCHAR(50),
            validade DATE,
            quantidade_minima INT,
            codigo_barras VARCHAR(50) UNIQUE,
            quantidade_estoque INT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
