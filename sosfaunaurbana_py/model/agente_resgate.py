from datetime import date
from model.usuario import Usuario


class AgenteResgate(Usuario):
    def __init__(self, id_usuario, nome, email, senha, data_cadastro: date,
                 matricula, cargo, telefone=None):
        super().__init__(id_usuario, nome, email, senha, data_cadastro, telefone)
        self.matricula = matricula
        self.cargo = cargo
        self.equipe = None  # pertence a (0,N)

    def __str__(self):
        return f"AgenteResgate({self.nome}, matricula={self.matricula}, cargo={self.cargo})"
