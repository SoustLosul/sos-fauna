from datetime import datetime
from model.cidadao import Cidadao


class SolicitacaoResgate:
    def __init__(self, id_solicitacao, data_hora: datetime, descricao, status,
                 cidadao: Cidadao, rua=None, bairro=None, cidade=None, cep=None, referencia=None):
        self.id_solicitacao = id_solicitacao
        self.data_hora = data_hora
        self.descricao = descricao
        self.status = status
        self.cidadao = cidadao  # realiza (1,1)
        self.equipe = None      # atende (0,1)
        self.especie = None     # envolve (0,1)

        # localizacao
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep
        self.referencia = referencia

    def __str__(self):
        return f"SolicitacaoResgate({self.id_solicitacao}, status={self.status})"
