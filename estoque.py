from medicamentos import Medicamento
from database import conectar_banco, registrar_historico, salvar_receita_medicamento
import os

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
    def _get_id_medicamento(codigo_barras):
        sql = "SELECT id FROM medicamentos WHERE codigo_barras = %s;"
        conn = None
        try:
            conn = conectar_banco()
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (codigo_barras,))
                    res = cur.fetchone()
            return res[0] if res else None
        except:
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def entrada(codigo_barras, quantidade):
        sql = """
        UPDATE medicamentos
        SET quantidade_estoque = quantidade_estoque + %s
        WHERE codigo_barras = %s
        RETURNING id, nome, quantidade_estoque;
        """

        try:
            conn = conectar_banco()
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (quantidade, codigo_barras))
                    result = cur.fetchone()
            conn.close()

            if result:
                id_medicamento, nome, qtd_atual = result

                registrar_historico(
                    id_medicamento, 
                    "entrada", 
                    quantidade, 
                    "Entrada manual de estoque"
                )

                print(f" Entrada registrada: +{quantidade} unidades de '{nome}'. Estoque atual: {qtd_atual}")
            else:
                print(" Medicamento não encontrado.")
        except Exception as e:
            print(" Erro ao registrar entrada:", e)

    @staticmethod
    def saida(codigo_barras, quantidade, caminho_receita=None):
        """
        Agora aceita caminho_receita para medicamentos controlados.
        Se for controlado, o main.py garante que o caminho é válido.
        """
        sql = """
        UPDATE medicamentos
        SET quantidade_estoque = quantidade_estoque - %s
        WHERE codigo_barras = %s AND quantidade_estoque >= %s
        RETURNING id, nome, quantidade_estoque;
        """

        try:
            # Atualizar estoque
            conn = conectar_banco()
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (quantidade, codigo_barras, quantidade))
                    result = cur.fetchone()
            conn.close()

            if not result:
                print(" Estoque insuficiente ou medicamento não encontrado.")
                return

            id_medicamento, nome, qtd_atual = result

            # ---- NOVO: salvar foto da receita no banco ----
            observacao = "Saída manual de estoque"

            if caminho_receita:
                try:
                    salvar_receita_medicamento(id_medicamento, caminho_receita)
                    observacao += f" | receita: {caminho_receita}"
                except Exception as e:
                    print(f" Erro ao salvar receita: {e}")

            # Registrar no histórico
            registrar_historico(
                id_medicamento,
                "saida",
                quantidade,
                observacao
            )

            print(f" Saída registrada: -{quantidade} unidades de '{nome}'. Estoque atual: {qtd_atual}")

        except Exception as e:
            print(" Erro ao registrar saída:", e)

    @staticmethod
    def verificar_reposicao():
        sql = """
        SELECT nome, quantidade_estoque, quantidade_minima
        FROM medicamentos
        WHERE quantidade_estoque <= quantidade_minima;
        """
        try:
            conn = conectar_banco()
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    rows = cur.fetchall()
            return rows
        except Exception as e:
            print(" Erro ao verificar reposição:", e)
            return []
        finally:
            if conn:
                conn.close()

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

    @staticmethod
    def repor_automaticamente():
        """
        Reposição automática de medicamentos com estoque baixo.
        Reabastece até o dobro da quantidade mínima.
        """
        try:
            reposicoes = Estoque.verificar_reposicao()
            if not reposicoes:
                print(" Nenhum medicamento precisa de reposição automática.")
                return

            conn = conectar_banco()
            with conn:
                with conn.cursor() as cur:
                    for nome, qtd, min_qtd in reposicoes:
                        nova_qtd = min_qtd * 2
                        adicionar = nova_qtd - qtd
                        if adicionar > 0:
                            cur.execute("""
                                UPDATE medicamentos
                                SET quantidade_estoque = %s
                                WHERE nome = %s
                                RETURNING id;
                            """, (nova_qtd, nome))

                            result = cur.fetchone()
                            id_medicamento = result[0] if result else None

                            if id_medicamento:
                                registrar_historico(
                                    id_medicamento,
                                    "entrada",
                                    adicionar,
                                    "Reposição automática"
                                )

                            print(f" Reposição automática: '{nome}' atualizado para {nova_qtd} unidades (+{adicionar}).")

            print("\n  Reposição automática concluída.")
        except Exception as e:
            print(" Erro durante a reposição automática:", e)
        finally:
            if 'conn' in locals() and conn:
                conn.close()
