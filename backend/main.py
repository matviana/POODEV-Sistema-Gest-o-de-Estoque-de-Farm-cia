from backend.database import criar_tabelas
from backend.medicamentos import Medicamento
from backend.farmacia import Farmacia
from backend.estoque import Estoque
from backend.historico import consultar_todas
from backend.redeneural import RedeNeuralDemanda

from datetime import date
import os

from fastapi import FastAPI

# Routers
from backend.routers.medicamentos_router import router as medicamentos_router
from backend.routers.estoque_router import router as estoque_router
from backend.routers.historico_router import router as historico_router
from backend.routers.farmacias_router import router as farmacias_router
from backend.routers.ia_router import router as ia_router



app = FastAPI(title="Sistema de Farmácia - API")

# Registrar rotas
app.include_router(medicamentos_router)
app.include_router(estoque_router)
app.include_router(historico_router)
app.include_router(farmacias_router)
app.include_router(ia_router)



@app.get("/")
def root():
    return {"mensagem": "API funcionando!"}


# -------------------------------
#  FUNÇÕES DO SISTEMA ANTIGO (MENU)
# -------------------------------

def mostrar_alertas():
    """Exibe alertas de medicamentos vencidos ou próximos do vencimento."""
    vencidos = Medicamento.consultar_vencidos()
    proximos = Medicamento.consultar_proximos_vencimento(30)

    if vencidos:
        print("\n  ALERTA: Medicamentos VENCIDOS encontrados:")
        for m in vencidos:
            dias_atraso = (date.today() - m[3]).days
            print(f" {m[1]} | Lote:{m[2]} | Venceu há {dias_atraso} dias (Val:{m[3]})")
    else:
        print("\n Nenhum medicamento vencido.")

    if proximos:
        print("\n ALERTA: Medicamentos próximos do vencimento (até 30 dias):")
        for m in proximos:
            dias_faltando = (m[3] - date.today()).days
            print(f" {m[1]} | Lote:{m[2]} | Faltam {dias_faltando} dias (Val:{m[3]})")
    else:
        print("\n Nenhum medicamento prestes a vencer.")


def menu():
    while True:
        print("\n=== SISTEMA DE FARMÁCIA ===")
        print("1 - Cadastrar Medicamento")
        print("2 - Consultar todos os Medicamentos")
        print("3 - Consultar por código de barras")
        print("4 - Deletar por código de barras")
        print("5 - Consultar por nome de medicamento")
        print("6 - Cadastrar Farmácia")
        print("7 - Consultar todas as Farmácias")
        print("8 - Mostrar alertas de vencimento")
        print("9 - Entrada medicamento - estoque + ")
        print("10 - Saída Medicamento - estoque -")
        print("11 - Verificar medicamento com estoque baixo")
        print("12 - Deletar Farmácia por CNPJ")
        print("13 - Repor automaticamente estoque baixo")
        print("14 - Ver histórico das movimentações")
        print("15 - Relatório dos Medicamentos mais vendidos do mês")
        print("16 - Previsão demanda (IA)")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        # --- Aqui mantém toda a sua lógica original ---
        # (NÃO removi nada)
        # ------------------------------------------------
        
        if opcao == "1":
            nome = input("Nome: ")
            lote = input("Lote: ")
            validade = input("Validade (AAAA-MM-DD): ")
            quantidade_minima = int(input("Quantidade mínima: "))
            codigo_barras = input("Código de barras: ")
            quantidade_estoque = int(input("Quantidade em estoque : ") or 0)

            m = Medicamento(nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque)
            m.cadastrar()

        elif opcao == "2":
            todos = Medicamento.consultar_todos()
            if not todos:
                print("Nenhum medicamento cadastrado.")
            else:
                for m in todos:
                    print(
                        f"ID:{m[0]} | Nome:{m[1]} | Lote:{m[2]} | Val:{m[3]} | "
                        f"Min:{m[4]} | Cod:{m[5]} | Qtd:{m[6]} | Controlado:{m[7]}"
                    )

        elif opcao == "3":
            codigo = input("Código de barras: ")
            m = Medicamento.consultar_por_codigo(codigo)
            if not m:
                print("Não encontrado.")
            else:
                print(
                    f"ID:{m[0]} | Nome:{m[1]} | Lote:{m[2]} | Val:{m[3]} | "
                    f"Min:{m[4]} | Cod:{m[5]} | Qtd:{m[6]} | Controlado:{m[7]}"
                )

        elif opcao == "4":
            codigo = input("Código de barras: ")
            ok = Medicamento.deletar_por_codigo(codigo)
            print("Deletado." if ok else "Nada a deletar.")

        elif opcao == "5":
            nome = input("Digite parte ou o nome completo do medicamento: ")
            resultados = Medicamento.consultar_por_nome(nome)
            if not resultados:
                print("Nenhum medicamento encontrado com esse nome.")
            else:
                print("\nResultados da busca:")
                for m in resultados:
                    print(
                        f"ID:{m[0]} | Nome:{m[1]} | Lote:{m[2]} | Val:{m[3]} | "
                        f"Min:{m[4]} | Cod:{m[5]} | Qtd:{m[6]} | Controlado:{m[7]}"
                    )

        elif opcao == "6":
            nome = input("Nome da Farmácia: ")
            endereco = input("Endereço: ")
            telefone = input("Telefone: ")
            cnpj = input("CNPJ : ")

            f = Farmacia(nome, endereco, telefone, cnpj)
            f.cadastrar()

        elif opcao == "7":
            todas = Farmacia.consultar_todas()
            if not todas:
                print("Nenhuma farmácia cadastrada.")
            else:
                print("\n=== Farmácias Cadastradas ===")
                for f in todas:
                    print(f"ID:{f[0]} | Nome:{f[1]} | Endereço:{f[2]} | Telefone:{f[3]}")

        elif opcao == "8":
            mostrar_alertas()

        elif opcao == "9":
            codigo = input("Código de barras: ")
            qtd = int(input("Quantidade adicionada: "))
            Estoque.entrada(codigo, qtd)

        elif opcao == "10":
            codigo = input("Código de barras: ")
            qtd = int(input("Quantidade removida: "))

            m = Medicamento.consultar_por_codigo(codigo)

            if not m:
                print("Medicamento não encontrado.")
                continue

            eh_controlado = bool(m[7])
            caminho_receita = None

            if eh_controlado:
                print("\n Este medicamento é CONTROLADO e exige receita!")
                caminho_receita = input("Digite o caminho da imagem da receita: ").strip()

                if not os.path.exists(caminho_receita):
                    print("Arquivo não encontrado.")
                    continue

            Estoque.saida(codigo, qtd, caminho_receita)

        elif opcao == "11":
            Estoque.mostrar_alertas_reposicao()

        elif opcao == "12":
            cnpj = input("CNPJ: ")
            ok = Farmacia.deletar_por_cnpj(cnpj)
            print("Farmácia deletada." if ok else "Nenhuma encontrada.")

        elif opcao == "13":
            Estoque.repor_automaticamente()

        elif opcao == "14":
            print("\n=== HISTÓRICO ===")
            registros = consultar_todas()

            if not registros:
                print("Nenhuma movimentação.")
            else:
                for mov in registros:
                    print(mov)

        elif opcao == "15":
            print("\n=== MAIS VENDIDOS DO MÊS ===")
            try:
                from backend.historico import consultar_mais_vendidos_mes
                resultados = consultar_mais_vendidos_mes()
            except Exception as e:
                print("Erro:", e)
                continue

            if not resultados:
                print("Nenhuma venda.")
            else:
                for nome, total in resultados:
                    print(f"{nome} — {total} unidades")

        elif opcao == "16":
            print("\n=== PREVISÃO DE DEMANDA (IA) ===")

            try:
                v1 = float(input("Vendas mês -3: "))
                v2 = float(input("Vendas mês -2: "))
                v3 = float(input("Vendas mês -1: "))
                ultimos_3 = [v1, v2, v3]

                mes = int(input("Mês desejado (1-12): "))
                evento = float(input("Intensidade do evento (0 a 1): "))

                ia = RedeNeuralDemanda()
                pred = ia.prever_proximo_mes_eventos(
                    ultimos_3_meses=ultimos_3,
                    mes_atual=mes,
                    intensidade_evento=evento
                )

                print(f"\n📈 Previsão: {pred:.2f} unidades\n")

            except Exception as e:
                print("Erro:", e)

        elif opcao == "0":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


# ======================
#  EXECUÇÃO VIA TERMINAL
# ======================

if __name__ == "__main__":
    criar_tabelas()
    print("\n Verificando medicamentos vencidos:")
    mostrar_alertas()
    menu()
