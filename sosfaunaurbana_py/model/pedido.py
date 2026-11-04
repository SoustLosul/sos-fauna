from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, ClassVar

from exceptions.erros import StatusInvalidoError, ValidacaoError
from model.decoradores import requer_status_pedido
from model.item_pedido import ItemPedido

if TYPE_CHECKING:
    from model.cidadao import Cidadao


class Pedido:
    """Compra de produtos feita por um cidadao que aceitou o termo de responsabilidade."""
    STATUS_VALIDOS: ClassVar[tuple[str, ...]] = ("Pendente", "Confirmado", "Entregue", "Cancelado")

    def __init__(self, id_pedido: int, data_pedido: date, status_pedido: str,
                 aceite_termo_resp: bool, cidadao: Cidadao) -> None:
        if not aceite_termo_resp:
            raise ValidacaoError("E necessario aceitar o termo de responsabilidade.")
        self._id_pedido = id_pedido
        self._data_pedido = data_pedido
        self._aceite_termo_resp = aceite_termo_resp
        self._cidadao = cidadao                # faz (1,1)
        self._itens: list[ItemPedido] = []     # contem (1,N) - privada
        self.status_pedido = status_pedido     # passa pelo setter (valida o status)

    # ---------- encapsulamento ----------
    @property
    def id_pedido(self) -> int:
        return self._id_pedido

    @property
    def data_pedido(self) -> date:
        return self._data_pedido

    @property
    def aceite_termo_resp(self) -> bool:
        return self._aceite_termo_resp

    @property
    def cidadao(self) -> Cidadao:
        return self._cidadao

    @property
    def status_pedido(self) -> str:
        return self._status_pedido

    @status_pedido.setter
    def status_pedido(self, valor: str) -> None:
        if valor not in self.STATUS_VALIDOS:
            raise StatusInvalidoError(f"Status invalido: {valor!r}. Use um de {self.STATUS_VALIDOS}.")
        self._status_pedido = valor

    @property
    def itens(self) -> tuple[ItemPedido, ...]:
        return tuple(self._itens)  # de fora e so leitura

    @requer_status_pedido("Pendente")  # decorador com argumento: so mexe em pedido pendente
    def adicionar_item(self, item: ItemPedido) -> None:
        """Inclui um item no pedido. So funciona enquanto o status for Pendente."""
        self._itens.append(item)

    @property
    def valor_total(self) -> float:
        """Soma dos subtotais de todos os itens."""
        return sum(item.subtotal for item in self._itens)

    # ---------- sobrecarga de operadores ----------
    def __iadd__(self, item: ItemPedido) -> Pedido:
        """Permite `pedido += item`."""
        if not isinstance(item, ItemPedido):
            return NotImplemented
        self.adicionar_item(item)  # pedido += item
        return self

    def __len__(self) -> int:
        return len(self._itens)    # len(pedido) = quantidade de itens

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Pedido):
            return NotImplemented
        return self.id_pedido == outro.id_pedido

    def __hash__(self) -> int:
        return hash(self.id_pedido)

    def __lt__(self, outro: Pedido) -> bool:
        if not isinstance(outro, Pedido):
            return NotImplemented
        return self.valor_total < outro.valor_total

    def __str__(self) -> str:
        return f"Pedido({self.id_pedido}, total=R${self.valor_total:.2f})"

    def __repr__(self) -> str:
        return f"Pedido(id={self.id_pedido}, status={self.status_pedido!r}, itens={len(self)})"
