from medicamentos import Medicamento

# ficticio pra tesrte
m = Medicamento(
    id_medicamento=None,
    nome="teste12 200mg",
    lote="L123",
    validade="2026-10-01",
    quantidade_minima=10,
    codigo_barras="7891011119390",
    quantidade_estoque=25
)


m.cadastrar()


medicamentos = Medicamento.consultar_todos()

if not medicamentos:
    print("Nenhum medicamento cadastrado.")
else:
    print("\n📋 Lista de Medicamentos:")
    for m in medicamentos:
        print(f"ID: {m[0]} | Nome: {m[1]} | Lote: {m[2]} | Validade: {m[3]} | Quantidade mínima: {m[4]} | Código de barras: {m[5]} | Estoque: {m[6]}")

