from model.produto import Produto


class ItemPedido:
    def __init__(self, produto: Produto, quantidade, preco_unitario):
        self.produto = produto  # refere-se a (1,1)
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"ItemPedido({self.produto.nome} x{self.quantidade})"
