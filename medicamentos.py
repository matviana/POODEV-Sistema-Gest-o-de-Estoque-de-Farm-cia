
from database import conectar_banco
from datetime import date, datetime

class Medicamento:
    def __init__(
        self, nome, lote, validade, quantidade_minima,
        codigo_barras, quantidade_estoque=0,
        id_medicamento=None, receita_obrigatoria=False
    ):
        """
        validade: pode ser datetime.date ou string 'AAAA-MM-DD'
        receita_obrigatoria: apenas usado por medicamentos controlados.
        """

        
        if isinstance(validade, str):
            try:
                self.validade = datetime.strptime(validade, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Formato de validade inválido. Use AAAA-MM-DD")
        else:
            self.validade = validade

        self.id_medicamento = id_medicamento
        self.nome = nome
        self.lote = lote
        self.quantidade_minima = int(quantidade_minima)
        self.codigo_barras = codigo_barras
        self.quantidade_estoque = int(quantidade_estoque)

         #medicamentos normais usam sempre False
        self.receita_obrigatoria = bool(receita_obrigatoria)


    def cadastrar(self):
        sql = """
        INSERT INTO medicamentos 
        (nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque, receita_obrigatoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        conn = None
        try:
            conn = conectar_banco()
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (
                        self.nome, self.lote, self.validade,
                        self.quantidade_minima, self.codigo_barras,
                        self.quantidade_estoque, self.receita_obrigatoria
                    ))
                    self.id_medicamento = cur.fetchone()[0]

            print(f" Medicamento '{self.nome}' cadastrado com id {self.id_medicamento}.")
        except Exception as e:
            print(" Erro ao cadastrar medicamento:", e)
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()


    @staticmethod
    def consultar_todos():
        sql = """
        SELECT id, nome, lote, validade, quantidade_minima,
               codigo_barras, quantidade_estoque, receita_obrigatoria
        FROM medicamentos
        ORDER BY nome;
        """
        conn = None
        try:
            conn = conectar_banco()
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
        finally:
            if conn:
                conn.close()


    @staticmethod
    def consultar_por_codigo(codigo_barras):
        sql = """
        SELECT id, nome, lote, validade, quantidade_minima,
               codigo_barras, quantidade_estoque, receita_obrigatoria
        FROM medicamentos
        WHERE codigo_barras = %s;
        """
        conn = None
        try:
            conn = conectar_banco()
            with conn.cursor() as cur:
                cur.execute(sql, (codigo_barras,))
                return cur.fetchone()
        finally:
            if conn:
                conn.close()


    @staticmethod
    def consultar_por_nome(nome):
        sql = """
        SELECT id, nome, lote, validade, quantidade_minima,
               codigo_barras, quantidade_estoque, receita_obrigatoria
        FROM medicamentos
        WHERE nome ILIKE %s
        ORDER BY nome;
        """
        conn = None
        try:
            conn = conectar_banco()
            with conn.cursor() as cur:
                cur.execute(sql, (f"%{nome}%",))
                return cur.fetchall()
        finally:
            if conn:
                conn.close()


    def atualizar(self):
        if not self.id_medicamento:
            raise ValueError("Medicamento sem id definido para atualização.")

        sql = """
        UPDATE medicamentos
        SET nome=%s, lote=%s, validade=%s, quantidade_minima=%s,
            codigo_barras=%s, quantidade_estoque=%s, receita_obrigatoria=%s
        WHERE id=%s;
        """

        conn = None
        try:
            conn = conectar_banco()
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (
                        self.nome, self.lote, self.validade,
                        self.quantidade_minima, self.codigo_barras,
                        self.quantidade_estoque, self.receita_obrigatoria,
                        self.id_medicamento
                    ))
            print(f" Medicamento id {self.id_medicamento} atualizado.")
        except Exception as e:
            print(" Erro ao atualizar medicamento:", e)
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()


    @staticmethod
    def deletar_por_codigo(codigo_barras):
        sql = "DELETE FROM medicamentos WHERE codigo_barras = %s RETURNING id;"
        conn = None
        try:
            conn = conectar_banco()
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (codigo_barras,))
                    deleted = cur.fetchone()
            return deleted is not None
        except Exception as e:
            print(" Erro ao deletar medicamento:", e)
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()


    # ===== Funções relacionadas à validade =====
    def esta_vencido(self):
        return date.today() > self.validade

    def dias_para_vencer(self):
        return (self.validade - date.today()).days

    @staticmethod
    def consultar_vencidos():
        sql = """
        SELECT id, nome, lote, validade, quantidade_minima,
               codigo_barras, quantidade_estoque, receita_obrigatoria
        FROM medicamentos
        WHERE validade < CURRENT_DATE
        ORDER BY validade;
        """
        conn = None
        try:
            conn = conectar_banco()
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
        finally:
            if conn:
                conn.close()

    @staticmethod
    def consultar_proximos_vencimento(dias=30):
        sql = """
        SELECT id, nome, lote, validade, quantidade_minima,
               codigo_barras, quantidade_estoque, receita_obrigatoria
        FROM medicamentos
        WHERE validade BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '%s days'
        ORDER BY validade;
        """
        conn = None
        try:
            conn = conectar_banco()
            with conn.cursor() as cur:
                cur.execute(sql, (dias,))
                return cur.fetchall()
        finally:
            if conn:
                conn.close()


    def verificar_validade(self):
        return (self.validade - date.today()).days

    def precisa_repor(self):
        return self.quantidade_estoque <= self.quantidade_minima




                # relação de herança de métodos e atributos da superclasse Medicamento , medicamento controlado precisa de receita para ser vendido
class MedicamentoControlado(Medicamento):
    def __init__(
        self, nome, lote, validade, quantidade_minima,
        codigo_barras, quantidade_estoque=0,
        receita_obrigatoria=True, id_medicamento=None
    ):
        super().__init__(
            nome, lote, validade, quantidade_minima,
            codigo_barras, quantidade_estoque,
            id_medicamento=id_medicamento,
            receita_obrigatoria=True
        )
