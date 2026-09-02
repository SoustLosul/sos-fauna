class EquipeResgate:
    def __init__(self, id_equipe, nome_equipe, area_atuacao):
        self.id_equipe = id_equipe
        self.nome_equipe = nome_equipe
        self.area_atuacao = area_atuacao
        self.agentes = []  # pertence a (0,N)

    def adicionar_agente(self, agente):
        self.agentes.append(agente)
        agente.equipe = self

    def __str__(self):
        return f"EquipeResgate({self.nome_equipe}, {self.area_atuacao})"
