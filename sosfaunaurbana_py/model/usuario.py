from __future__ import annotations

from datetime import date
from typing import ClassVar

from exceptions.erros import ValidacaoError
from model.validadores import exigir_texto


class Usuario:
    """Pessoa cadastrada no sistema. E a classe base (heranca) de Cidadao e AgenteResgate."""
    # Atributo de CLASSE: as subclasses podem mudar essa regra (ex.: Cidadao exige email)
    EMAIL_OBRIGATORIO: ClassVar[bool] = False

    def __init__(self, id_usuario: int, nome: str, email: str, senha: str,
                 data_cadastro: date, telefone: str | None = None) -> None:
        self._id_usuario = id_usuario          # protegido: so leitura (sem setter)
        self._data_cadastro = data_cadastro    # protegido: so leitura (sem setter)
        self.nome = nome                       # passam pelos setters (com validacao)
        self.email = email
        self.senha = senha
        self.telefone = telefone

    # ---------- encapsulamento ----------
    @property
    def id_usuario(self) -> int:
        return self._id_usuario

    @property
    def data_cadastro(self) -> date:
        return self._data_cadastro

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome = exigir_texto(valor, "Nome")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        valor = str(valor).strip()
        if self.EMAIL_OBRIGATORIO and not valor:
            raise ValidacaoError("Email e obrigatorio.")
        self._email = valor

    @property
    def senha(self) -> str:
        return self.__senha

    @senha.setter
    def senha(self, valor: str) -> None:
        # __senha (dois underlines) sofre "name mangling": vira _Usuario__senha,
        # entao nao e acessivel por engano de fora da classe.
        self.__senha = valor

    def verificar_senha(self, tentativa: str) -> bool:
        """Confere a tentativa com a senha guardada, sem expor a senha."""
        return self.__senha == tentativa

    # ---------- sobrecarga de operadores ----------
    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Usuario):
            return NotImplemented
        return self.id_usuario == outro.id_usuario

    def __hash__(self) -> int:
        return hash(self.id_usuario)

    def __lt__(self, outro: Usuario) -> bool:
        if not isinstance(outro, Usuario):
            return NotImplemented
        return self.nome.casefold() < outro.nome.casefold()  # sorted(usuarios) ordena por nome

    def descrever(self) -> str:
        """Resumo do usuario. As subclasses SOBRESCREVEM este metodo (polimorfismo)."""
        return f"Usuario({self.id_usuario}, {self.nome}, {self.email})"

    def __str__(self) -> str:
        return self.descrever()

    def __repr__(self) -> str:
        # de proposito NAO mostra a senha
        return f"{type(self).__name__}(id={self.id_usuario}, nome={self.nome!r})"
