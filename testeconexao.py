from database import conectar_banco

def testar_conexao():
    conn = conectar_banco()
    if conn:
        print(" Conexão bem-sucedida com o banco de dados!")
        cur = conn.cursor()
        cur.execute("SELECT version();")
        versao = cur.fetchone()
        print("Versão do PostgreSQL:", versao[0])
        cur.close()
        conn.close()
    else:
        print(" Falha na conexão.")

if __name__ == "__main__":
    testar_conexao()
