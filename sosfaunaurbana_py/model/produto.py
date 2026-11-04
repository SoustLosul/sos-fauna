from __future__ import annotations

from model.item_pedido import ItemPedido
from model.validadores import exigir_preco, exigir_texto


class Produto:
    """Item vendido para o cidadao remover animais com seguranca."""
    def __init__(self, id_produto: int, nome: str, descricao: str, preco: float,
                 categoria: str) -> None:
        self._id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria

    @property
    def id_produto(self) -> int:
        return self._id_produto

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome = exigir_texto(valor, "Nome do produto")

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, valor: float) -> None:
        self._preco = exigir_preco(valor)

    # ---------- sobrecarga de operadores ----------
    def __mul__(self, quantidade: int) -> ItemPedido:
        """`produto * quantidade` devolve um ItemPedido com o preco atual do produto."""
        # produto * 3  ->  um ItemPedido com 3 unidades ao preco atual
        if not isinstance(quantidade, int):
            return NotImplemented
        return ItemPedido(self, quantidade, self.preco)

    def __rmul__(self, quantidade: int) -> ItemPedido:
        return self.__mul__(quantidade)  # 3 * produto tambem funciona

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Produto):
            return NotImplemented
        return self.id_produto == outro.id_produto

    def __hash__(self) -> int:
        return hash(self.id_produto)

    def __lt__(self, outro: Produto) -> bool:
        if not isinstance(outro, Produto):
            return NotImplemented
        return self.preco < outro.preco  # sorted(produtos) ordena do mais barato ao mais caro

    def __str__(self) -> str:
        return f"Produto({self.nome}, R${self.preco:.2f})"

    def __repr__(self) -> str:
        return f"Produto(id={self.id_produto}, nome={self.nome!r}, preco={self.preco})"
