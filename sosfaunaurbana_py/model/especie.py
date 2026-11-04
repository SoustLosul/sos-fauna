from __future__ import annotations

from typing import TYPE_CHECKING

from model.validadores import exigir_texto

if TYPE_CHECKING:
    from model.material_educativo import MaterialEducativo


class Especie:
    """Animal que pode estar envolvido em uma solicitacao de resgate."""
    def __init__(self, id_especie: int, nome_popular: str, nome_cientifico: str,
                 nivel_risco: str, orientacoes_captura: str) -> None:
        self._id_especie = id_especie
        self.nome_popular = nome_popular
        self.nome_cientifico = nome_cientifico
        self.nivel_risco = nivel_risco
        self.orientacoes_captura = orientacoes_captura
        self._materiais: list[MaterialEducativo] = []  # aborda (0,N) - privada

    @property
    def id_especie(self) -> int:
        return self._id_especie

    @property
    def nome_popular(self) -> str:
        return self._nome_popular

    @nome_popular.setter
    def nome_popular(self, valor: str) -> None:
        self._nome_popular = exigir_texto(valor, "Nome popular")

    @property
    def materiais(self) -> tuple[MaterialEducativo, ...]:
        return tuple(self._materiais)

    def adicionar_material(self, material: MaterialEducativo) -> None:
        """Associa um material educativo a esta especie."""
        self._materiais.append(material)

    # ---------- sobrecarga de operadores ----------
    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Especie):
            return NotImplemented
        return self.id_especie == outro.id_especie

    def __hash__(self) -> int:
        return hash(self.id_especie)

    def __lt__(self, outro: Especie) -> bool:
        if not isinstance(outro, Especie):
            return NotImplemented
        return self.nome_popular.casefold() < outro.nome_popular.casefold()

    def __str__(self) -> str:
        return f"Especie({self.nome_popular}, risco={self.nivel_risco})"

    def __repr__(self) -> str:
        return f"Especie(id={self.id_especie}, nome={self.nome_popular!r})"
