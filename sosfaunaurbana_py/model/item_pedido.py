from __future__ import annotations

from typing import TYPE_CHECKING

from exceptions.erros import ValidacaoError
from model.validadores import exigir_preco, exigir_quantidade

if TYPE_CHECKING:
    from model.produto import Produto


class ItemPedido:
    """Linha de um pedido: um produto, a quantidade e o preco unitario na compra."""
    def __init__(self, produto: Produto, quantidade: int, preco_unitario: float) -> None:
        self._produto = produto  # refere-se a (1,1) - so leitura
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    @property
    def produto(self) -> Produto:
        return self._produto

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor: int) -> None:
        self._quantidade = exigir_quantidade(valor)

    @property
    def preco_unitario(self) -> float:
        return self._preco_unitario

    @preco_unitario.setter
    def preco_unitario(self, valor: float) -> None:
        self._preco_unitario = exigir_preco(valor)

    @property
    def subtotal(self) -> float:
        """Quantidade vezes preco unitario."""
        return self.quantidade * self.preco_unitario

    # ---------- sobrecarga de operadores ----------
    def __add__(self, outro: ItemPedido) -> ItemPedido:
        """`item + item` soma as quantidades (so para o mesmo produto)."""
        # item + item (do MESMO produto) -> soma as quantidades
        if not isinstance(outro, ItemPedido):
            return NotImplemented
        if self.produto != outro.produto:
            raise ValidacaoError("So e possivel somar itens do mesmo produto.")
        return ItemPedido(self.produto, self.quantidade + outro.quantidade, self.preco_unitario)

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, ItemPedido):
            return NotImplemented
        return (self.produto == outro.produto and self.quantidade == outro.quantidade
                and self.preco_unitario == outro.preco_unitario)

    def __lt__(self, outro: ItemPedido) -> bool:
        if not isinstance(outro, ItemPedido):
            return NotImplemented
        return self.subtotal < outro.subtotal

    def __str__(self) -> str:
        return f"ItemPedido({self.produto.nome} x{self.quantidade})"

    def __repr__(self) -> str:
        return f"ItemPedido(produto={self.produto.id_produto}, qtd={self.quantidade})"
