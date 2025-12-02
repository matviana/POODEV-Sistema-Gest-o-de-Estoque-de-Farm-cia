class Usuario:
    def __init__(self, id_usuario, nome, email, senha):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha  

class Administrador(Usuario):
    def __init__(self, id_usuario, nome, email, senha):
        super().__init__(id_usuario, nome, email, senha)

    def cadastrar_medicamento(self, estoque, medicamento):
        estoque.adicionar_medicamento(medicamento)


