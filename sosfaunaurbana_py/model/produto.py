class Produto:
    def __init__(self, id_produto, nome, descricao, preco, categoria):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria

    def __str__(self):
        return f"Produto({self.nome}, R${self.preco:.2f})"
