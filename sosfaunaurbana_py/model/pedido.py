from datetime import date
from model.cidadao import Cidadao


class Pedido:
    def __init__(self, id_pedido, data_pedido: date, status_pedido,
                 aceite_termo_resp: bool, cidadao: Cidadao):
        self.id_pedido = id_pedido
        self.data_pedido = data_pedido
        self.status_pedido = status_pedido
        self.aceite_termo_resp = aceite_termo_resp
        self.cidadao = cidadao  # faz (1,1)
        self.itens = []         # contem (1,N)

    def adicionar_item(self, item):
        self.itens.append(item)

    @property
    def valor_total(self):
        return sum(item.subtotal for item in self.itens)

    def __str__(self):
        return f"Pedido({self.id_pedido}, total=R${self.valor_total:.2f})"
