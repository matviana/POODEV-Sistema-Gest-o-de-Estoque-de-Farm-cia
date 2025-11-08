
from database import conectar_banco
from datetime import date, datetime

class Medicamento:
    def __init__(self, nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque=0, id_medicamento=None):
        """
        validade: pode ser datetime.date ou string 'AAAA-MM-DD'
        """
        # parse validade se string
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

    
    def cadastrar(self):
        sql = """
        INSERT INTO medicamentos (nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque)
        VALUES (%s, %s, %s, %s, %s, %s)
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
                        self.quantidade_estoque
                    ))
                    newid = cur.fetchone()[0]
                    self.id_medicamento = newid
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
        SELECT id, nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque
        FROM medicamentos
        ORDER BY nome;
        """
        conn = None
        try:
            conn = conectar_banco()
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
            return rows  
        finally:
            if conn:
                conn.close()

    @staticmethod
    def consultar_por_codigo(codigo_barras):
        sql = """
        SELECT id, nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque
        FROM medicamentos
        WHERE codigo_barras = %s;
        """
        conn = None
        try:
            conn = conectar_banco()
            with conn.cursor() as cur:
                cur.execute(sql, (codigo_barras,))
                row = cur.fetchone()
            return row
        finally:
            if conn:
                conn.close()

    @staticmethod
    def consultar_por_nome(nome):
        """
        Consulta medicamentos pelo nome (parcial ou completo).
        Usa ILIKE para não diferenciar maiúsculas/minúsculas.
        """
        sql = """
        SELECT id, nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque
        FROM medicamentos
        WHERE nome ILIKE %s
        ORDER BY nome;
        """
        conn = None
        try:
            conn = conectar_banco()
            with conn.cursor() as cur:
                cur.execute(sql, (f"%{nome}%",))
                rows = cur.fetchall()
            return rows
        finally:
            if conn:
                conn.close()

    def atualizar(self):
        if not self.id_medicamento:
            raise ValueError("Medicamento sem id. Use consultar_por_codigo ou informe id antes de atualizar.")
        sql = """
        UPDATE medicamentos
        SET nome=%s, lote=%s, validade=%s, quantidade_minima=%s, codigo_barras=%s, quantidade_estoque=%s
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
                        self.quantidade_estoque, self.id_medicamento
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
                
                
    def esta_vencido(self):
        """Retorna True se o medicamento já passou da validade."""
        return date.today() > self.validade

    def dias_para_vencer(self):
        """Retorna quantos dias faltam para o vencimento (negativo se já venceu)."""
        return (self.validade - date.today()).days

    @staticmethod
    def consultar_vencidos():
        """Retorna todos os medicamentos cuja validade já passou."""
        sql = """
        SELECT id, nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque
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
        """Retorna medicamentos que vencem nos próximos 'dias' dias."""
        sql = """
        SELECT id, nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque
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
        """Retorna o número de dias até o vencimento."""
        return (self.validade - date.today()).days

    def precisa_repor(self):
        """Retorna True se o estoque está abaixo ou igual ao mínimo."""
        return self.quantidade_estoque <= self.quantidade_minima




class MedicamentoControlado(Medicamento):
    def __init__(
        self, nome, lote, validade, quantidade_minima,
        codigo_barras, quantidade_estoque=0,
        receita_obrigatoria=True, id_medicamento=None
    ):
        super().__init__(nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque, id_medicamento)
        self.receita_obrigatoria = bool(receita_obrigatoria)
