from estoque import Estoque

class Farmacia:
    def __init__(self, id_farmacia, nome, cidade):
        self.id_farmacia = id_farmacia
        self.nome = nome
        self.cidade = cidade
        self.estoque = Estoque()
