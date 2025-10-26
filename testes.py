from estoque import Estoque
from medicamentos import Medicamento
from datetime import date

estoque = Estoque()
m1 = Medicamento("Dipirona", "L123", date(2025, 12, 31), 10, "789456123")
estoque.adicionar_medicamento(m1)

print("Medicamentos no estoque:", estoque.listar_medicamentos())
print("Reposições necessárias:", [m.nome for m in estoque.verificar_reposicao()])
