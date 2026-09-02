class Especie:
    def __init__(self, id_especie, nome_popular, nome_cientifico, nivel_risco, orientacoes_captura):
        self.id_especie = id_especie
        self.nome_popular = nome_popular
        self.nome_cientifico = nome_cientifico
        self.nivel_risco = nivel_risco
        self.orientacoes_captura = orientacoes_captura
        self.materiais = []  # aborda (0,N)

    def adicionar_material(self, material):
        self.materiais.append(material)

    def __str__(self):
        return f"Especie({self.nome_popular}, risco={self.nivel_risco})"
