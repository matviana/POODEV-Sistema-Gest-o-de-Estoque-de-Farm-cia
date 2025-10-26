from database import conectar_banco

class Farmacia:
    def __init__(self, nome, endereco, telefone, cnpj, id_farmacia=None):
        self.id_farmacia = id_farmacia
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.cnpj = cnpj

    def cadastrar(self):
        sql = """
        INSERT INTO farmacias (nome, endereco, telefone, cnpj)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        conn = None
        try:
            conn = conectar_banco()
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (self.nome, self.endereco, self.telefone, self.cnpj))
                    self.id_farmacia = cur.fetchone()[0]
            print(f"Farmácia '{self.nome}' cadastrada com id {self.id_farmacia}.")
        except Exception as e:
            print("Erro ao cadastrar farmácia:", e)
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    @staticmethod
    def consultar_todas():
        sql = "SELECT id, nome, endereco, telefone, cnpj FROM farmacias ORDER BY nome;"
        conn = None
        try:
            conn = conectar_banco()
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
        finally:
            if conn:
                conn.close()