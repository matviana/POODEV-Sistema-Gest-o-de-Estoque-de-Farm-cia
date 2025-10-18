from medicamento import Medicamento
from estoque import Estoque
from database import  criar_tabelas



def menu():
    while True:
        print("\n=== SISTEMA DE FARMÁCIA ===")
        print("1 - Cadastrar Medicamento")
        print("2 - Consultar Medicamentos")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            lote = input("Lote: ")
            validade = input("Validade (AAAA-MM-DD): ")
            quantidade_minima = int(input("Quantidade mínima: "))
            codigo_barras = input("Código de barras: ")

            m = Medicamento(nome, lote, validade, quantidade_minima, codigo_barras)
            m.cadastrar()

        elif opcao == "2":
            Medicamento.consultar_todos()

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    criar_tabelas()
    menu()





