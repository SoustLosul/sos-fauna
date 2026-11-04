from __future__ import annotations

from datetime import date

from model.usuario import Usuario


class Cidadao(Usuario):
    """Pessoa que solicita resgates e compra produtos. Herda de Usuario."""
    EMAIL_OBRIGATORIO = True  # regra do README: cidadao nao cadastra sem email

    def __init__(self, id_usuario: int, nome: str, email: str, senha: str,
                 data_cadastro: date, rua: str, numero: str, bairro: str,
                 cidade: str, cep: str, telefone: str | None = None) -> None:
        super().__init__(id_usuario, nome, email, senha, data_cadastro, telefone)
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep

    @property
    def endereco(self) -> str:
        """Endereco completo em uma unica linha."""
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}"

    def descrever(self) -> str:
        """Sobrescreve Usuario.descrever mostrando o endereco (polimorfismo)."""
        return f"Cidadao({self.nome}, {self.endereco})"
