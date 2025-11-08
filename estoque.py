from medicamentos import Medicamento
from database import conectar_banco


class Estoque:
    def __init__(self):
        self.medicamentos = []

    def adicionar_medicamento(self, medicamento: Medicamento):
        self.medicamentos.append(medicamento)

    def remover_medicamento(self, codigo_barras):
        self.medicamentos = [m for m in self.medicamentos if m.codigo_barras != codigo_barras]

    def listar_medicamentos(self):
        return [m.nome for m in self.medicamentos]

    def verificar_reposicao_local(self):
        """Verifica apenas os medicamentos carregados em memória."""
        return [m for m in self.medicamentos if m.precisa_repor()]

   

    @staticmethod
    def entrada(codigo_barras, quantidade):
        sql = """
        UPDATE medicamentos
        SET quantidade_estoque = quantidade_estoque + %s
        WHERE codigo_barras = %s
        RETURNING nome, quantidade_estoque;
        """
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (quantidade, codigo_barras))
                result = cur.fetchone()
        conn.close()

        if result:
            print(f" Entrada registrada: {quantidade} unidades adicionadas a '{result[0]}'. Estoque atual: {result[1]}")
        else:
            print(" Medicamento não encontrado.")

    @staticmethod
    def saida(codigo_barras, quantidade):
        sql = """
        UPDATE medicamentos
        SET quantidade_estoque = quantidade_estoque - %s
        WHERE codigo_barras = %s AND quantidade_estoque >= %s
        RETURNING nome, quantidade_estoque;
        """
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (quantidade, codigo_barras, quantidade))
                result = cur.fetchone()
        conn.close()

        if result:
            print(f" Saída registrada: {quantidade} unidades removidas de '{result[0]}'. Estoque atual: {result[1]}")
        else:
            print(" Estoque insuficiente ou medicamento não encontrado.")

    @staticmethod
    def verificar_reposicao():
        sql = """
        SELECT nome, quantidade_estoque, quantidade_minima
        FROM medicamentos
        WHERE quantidade_estoque <= quantidade_minima;
        """
        conn = conectar_banco()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
        return rows

@staticmethod
def mostrar_alertas_reposicao():
    """Mostra medicamentos com estoque abaixo do mínimo, com tratamento de erros."""
    try:
        reposicoes = Estoque.verificar_reposicao()

        if not reposicoes:
            print(" Todos os estoques estão adequados.")
        else:
            print("\n  ALERTA: Medicamentos com estoque baixo:")
            for nome, qtd, min_qtd in reposicoes:
                print(f" - {nome}: {qtd} unidades (mínimo {min_qtd})")

    except Exception as e:        
        print(" Erro ao verificar alertas de reposição:", e)

