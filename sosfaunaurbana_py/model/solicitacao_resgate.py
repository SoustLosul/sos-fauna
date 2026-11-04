from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, ClassVar

from exceptions.erros import StatusInvalidoError

if TYPE_CHECKING:
    from model.cidadao import Cidadao
    from model.equipe_resgate import EquipeResgate
    from model.especie import Especie


class SolicitacaoResgate:
    """Pedido de resgate de um animal aberto por um cidadao."""
    STATUS_VALIDOS: ClassVar[tuple[str, ...]] = ("Aberta", "Em atendimento", "Concluida", "Cancelada")

    def __init__(self, id_solicitacao: int, data_hora: datetime, descricao: str, status: str,
                 cidadao: Cidadao, rua: str | None = None, bairro: str | None = None,
                 cidade: str | None = None, cep: str | None = None,
                 referencia: str | None = None) -> None:
        self._id_solicitacao = id_solicitacao
        self._data_hora = data_hora
        self._cidadao = cidadao                 # realiza (1,1)
        self.descricao = descricao
        self.status = status                    # passa pelo setter (valida o status)
        self.equipe: EquipeResgate | None = None   # atende (0,1)
        self.especie: Especie | None = None        # envolve (0,1)

        # localizacao
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep
        self.referencia = referencia

    @property
    def id_solicitacao(self) -> int:
        return self._id_solicitacao

    @property
    def data_hora(self) -> datetime:
        return self._data_hora

    @property
    def cidadao(self) -> Cidadao:
        return self._cidadao

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, valor: str) -> None:
        if valor not in self.STATUS_VALIDOS:
            raise StatusInvalidoError(f"Status invalido: {valor!r}. Use um de {self.STATUS_VALIDOS}.")
        self._status = valor

    # ---------- sobrecarga de operadores ----------
    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, SolicitacaoResgate):
            return NotImplemented
        return self.id_solicitacao == outro.id_solicitacao

    def __hash__(self) -> int:
        return hash(self.id_solicitacao)

    def __lt__(self, outro: SolicitacaoResgate) -> bool:
        if not isinstance(outro, SolicitacaoResgate):
            return NotImplemented
        return self.data_hora < outro.data_hora  # mais antiga = "menor" (vem primeiro)

    def __str__(self) -> str:
        return f"SolicitacaoResgate({self.id_solicitacao}, status={self.status})"

    def __repr__(self) -> str:
        return f"SolicitacaoResgate(id={self.id_solicitacao}, status={self.status!r})"
