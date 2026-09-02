from datetime import date


class Usuario:
    def __init__(self, id_usuario, nome, email, senha, data_cadastro: date, telefone=None):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.data_cadastro = data_cadastro

    def __str__(self):
        return f"Usuario({self.id_usuario}, {self.nome}, {self.email})"
