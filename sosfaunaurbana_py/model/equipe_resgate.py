from __future__ import annotations

from typing import TYPE_CHECKING

from model.decoradores import registrar
from model.validadores import exigir_texto

if TYPE_CHECKING:
    from model.agente_resgate import AgenteResgate


class EquipeResgate:
    """Grupo de agentes responsavel por atender solicitacoes."""
    def __init__(self, id_equipe: int, nome_equipe: str, area_atuacao: str) -> None:
        self._id_equipe = id_equipe
        self.nome_equipe = nome_equipe
        self.area_atuacao = area_atuacao
        self._agentes: list[AgenteResgate] = []  # pertence a (0,N) - privada

    @property
    def id_equipe(self) -> int:
        return self._id_equipe

    @property
    def nome_equipe(self) -> str:
        return self._nome_equipe

    @nome_equipe.setter
    def nome_equipe(self, valor: str) -> None:
        self._nome_equipe = exigir_texto(valor, "Nome da equipe")

    @property
    def agentes(self) -> tuple[AgenteResgate, ...]:
        # devolve uma tupla (copia imutavel): de fora so da para ler;
        # para incluir alguem e obrigatorio passar por adicionar_agente
        return tuple(self._agentes)

    @registrar
    def adicionar_agente(self, agente: AgenteResgate) -> None:
        """Inclui o agente na equipe (ignora repetidos) e vincula agente.equipe."""
        if agente in self._agentes:  # usa o __eq__ do Usuario
            return
        self._agentes.append(agente)
        agente.equipe = self

    # ---------- sobrecarga de operadores ----------
    def __iadd__(self, agente: AgenteResgate) -> EquipeResgate:
        """Permite `equipe += agente`."""
        self.adicionar_agente(agente)  # equipe += agente
        return self

    def __len__(self) -> int:
        return len(self._agentes)      # len(equipe)

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, EquipeResgate):
            return NotImplemented
        return self.id_equipe == outro.id_equipe

    def __hash__(self) -> int:
        return hash(self.id_equipe)

    def __str__(self) -> str:
        return f"EquipeResgate({self.nome_equipe}, {self.area_atuacao})"

    def __repr__(self) -> str:
        return f"EquipeResgate(id={self.id_equipe}, nome={self.nome_equipe!r})"
