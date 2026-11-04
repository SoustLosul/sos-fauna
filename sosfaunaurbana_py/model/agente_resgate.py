from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from model.usuario import Usuario
from model.validadores import exigir_texto

if TYPE_CHECKING:  # so para as anotacoes (evita import circular com EquipeResgate)
    from model.equipe_resgate import EquipeResgate


class AgenteResgate(Usuario):
    """Profissional que atende as solicitacoes. Herda de Usuario."""
    def __init__(self, id_usuario: int, nome: str, email: str, senha: str,
                 data_cadastro: date, matricula: str, cargo: str,
                 telefone: str | None = None) -> None:
        super().__init__(id_usuario, nome, email, senha, data_cadastro, telefone)
        self.matricula = matricula
        self.cargo = cargo
        self.equipe: EquipeResgate | None = None  # pertence a (0,N)

    @property
    def matricula(self) -> str:
        return self._matricula

    @matricula.setter
    def matricula(self, valor: str) -> None:
        self._matricula = exigir_texto(valor, "Matricula")

    def descrever(self) -> str:
        """Sobrescreve Usuario.descrever mostrando matricula e cargo (polimorfismo)."""
        return f"AgenteResgate({self.nome}, matricula={self.matricula}, cargo={self.cargo})"
