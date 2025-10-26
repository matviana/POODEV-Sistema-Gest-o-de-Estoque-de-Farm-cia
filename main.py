
from database import criar_tabelas
from medicamentos import Medicamento
from farmacia import Farmacia  

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
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

       
        if opcao == "1":
            nome = input("Nome: ")
            lote = input("Lote: ")
            validade = input("Validade (AAAA-MM-DD): ")
            quantidade_minima = int(input("Quantidade mínima: "))
            codigo_barras = input("Código de barras: ")
            quantidade_estoque = int(input("Quantidade em estoque (opcional, 0): ") or 0)

            m = Medicamento(nome, lote, validade, quantidade_minima, codigo_barras, quantidade_estoque)
            m.cadastrar()

        elif opcao == "2":
            todos = Medicamento.consultar_todos()
            if not todos:
                print("Nenhum medicamento cadastrado.")
            else:
                for m in todos:
                    print(f"ID:{m[0]} | Nome:{m[1]} | Lote:{m[2]} | Val:{m[3]} | Min:{m[4]} | Cod:{m[5]} | Qtd:{m[6]}")

        elif opcao == "3":
            codigo = input("Código de barras: ")
            m = Medicamento.consultar_por_codigo(codigo)
            if not m:
                print("Não encontrado.")
            else:
                print(f"ID:{m[0]} | Nome:{m[1]} | Lote:{m[2]} | Val:{m[3]} | Min:{m[4]} | Cod:{m[5]} | Qtd:{m[6]}")

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
                    print(f"ID:{m[0]} | Nome:{m[1]} | Lote:{m[2]} | Val:{m[3]} | Min:{m[4]} | Cod:{m[5]} | Qtd:{m[6]}")

       
        elif opcao == "6":
            nome = input("Nome da Farmácia: ")
            endereco = input("Endereço: ")
            telefone = input("Telefone: ")

            f = Farmacia(nome, endereco, telefone)
            f.cadastrar()

        elif opcao == "7":
            todas = Farmacia.consultar_todas()
            if not todas:
                print("Nenhuma farmácia cadastrada.")
            else:
                print("\n=== Farmácias Cadastradas ===")
                for f in todas:
                    print(f"ID:{f[0]} | Nome:{f[1]} | Endereço:{f[2]} | Telefone:{f[3]}")

        
        elif opcao == "0":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    criar_tabelas() 
    menu()
