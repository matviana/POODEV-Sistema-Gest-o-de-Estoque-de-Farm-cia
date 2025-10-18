from database import conectar_banco

class Medicamento:
    def __init__(self, id_medicamento, nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque):
        self.id_medicamento = id_medicamento
        self.nome = nome
        self.lote = lote
        self.validade = validade
        self.quantidade_minima = quantidade_minima
        self.codigo_barras = codigo_barras
        self.quantidade_estoque = quantidade_estoque
        
        
    def cadastrar(self):
        conn = conectar_banco()
        cur = conn.cursor()

        sql = """
        INSERT INTO medicamentos (nome, lote, validade, quantidade_minima, codigo_barras)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (self.nome, self.lote, self.validade, self.quantidade_minima, self.codigo_barras)
        cur.execute(sql, valores)
        conn.commit()

        cur.close()
        conn.close()
        print(f" Medicamento '{self.nome}' cadastrado com sucesso!")

    @staticmethod
    def consultar_todos():
        conn = conectar_banco()
        cur = conn.cursor()

        cur.execute("SELECT * FROM medicamentos;")
        dados = cur.fetchall()

        cur.close()
        conn.close()

        if not dados:
            print(" Nenhum medicamento cadastrado.")
        else:
            print("\n Lista de Medicamentos:")
            for m in dados:
                 print(f"ID: {m[0]} | Nome: {m[1]} | Lote: {m[2]} | Validade: {m[3]} | Quantidade mínima: {m[4]} | Código de barras: {m[5]}")

    def verificar_validade(self):
        from datetime import date
        return (self.validade - date.today()).days

    def precisa_repor(self):
        return self.quantidade_estoque <= self.quantidade_minima


class MedicamentoControlado(Medicamento):
    def __init__(self, id_medicamento, nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque, receita_obrigatoria):
        super().__init__(id_medicamento, nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque)
        self.receita_obrigatoria = receita_obrigatoria
