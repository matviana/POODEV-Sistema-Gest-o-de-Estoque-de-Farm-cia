from medicamento import Medicamento

class Estoque:
    def __init__(self):
        self.medicamentos = []

    def adicionar_medicamento(self, medicamento: Medicamento):
        self.medicamentos.append(medicamento)

    def remover_medicamento(self, codigo_barras):
        self.medicamentos = [m for m in self.medicamentos if m.codigo_barras != codigo_barras]

    def listar_medicamentos(self):
        return [m.nome for m in self.medicamentos]

    def verificar_reposicao(self):
        return [m for m in self.medicamentos if m.precisa_repor()]
