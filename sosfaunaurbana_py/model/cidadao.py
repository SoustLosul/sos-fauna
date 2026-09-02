from datetime import date
from model.usuario import Usuario


class Cidadao(Usuario):
    def __init__(self, id_usuario, nome, email, senha, data_cadastro: date,
                 rua, numero, bairro, cidade, cep, telefone=None):
        super().__init__(id_usuario, nome, email, senha, data_cadastro, telefone)
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep

    def __str__(self):
        return f"Cidadao({self.nome}, {self.rua}, {self.numero} - {self.bairro}, {self.cidade})"
