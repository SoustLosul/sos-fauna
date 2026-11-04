"""Camada de persistencia (repositorio) do SOS Fauna Urbana.

Guarda os dados em arquivos .txt dentro da pasta "dados": cada linha e um registro
e os campos sao separados por "|". As listas em memoria (cidadaos, produtos...) sao
reconstruidas a partir dos arquivos quando o programa abre (carregar_dados).

Como a interface so usa as funcoes deste modulo, trocar .txt por JSON ou banco de
dados nao exige mexer nas classes do modelo (regras de negocio).
"""
import os
from datetime import date, datetime
from typing import Callable

from exceptions.erros import PersistenciaError, RegistroDuplicadoError
from model.agente_resgate import AgenteResgate
from model.cidadao import Cidadao
from model.decoradores import ContarChamadas, cronometrar
from model.equipe_resgate import EquipeResgate
from model.especie import Especie
from model.item_pedido import ItemPedido
from model.pedido import Pedido
from model.produto import Produto
from model.solicitacao_resgate import SolicitacaoResgate

# ==========================================================
# "Banco de dados" em memoria
# ==========================================================
cidadaos: list[Cidadao] = []
agentes: list[AgenteResgate] = []
equipes: list[EquipeResgate] = []
especies: list[Especie] = []
solicitacoes: list[SolicitacaoResgate] = []
produtos: list[Produto] = []
pedidos: list[Pedido] = []

proximo_id: int = 1


@ContarChamadas  # decorador feito com classe: conta quantos IDs foram gerados
def gerar_id() -> int:
    """Devolve um ID novo e unico (compartilhado por todas as entidades)."""
    global proximo_id
    id_atual = proximo_id
    proximo_id += 1
    return id_atual


# ==========================================================
# Acesso aos arquivos (com tratamento de erros)
# ==========================================================
# Pasta "dados" ao lado do main.py, independente de onde o programa foi aberto.
PASTA_DADOS: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados")


def caminho_arquivo(nome_arquivo: str) -> str:
    """Caminho completo de um arquivo dentro da pasta de dados."""
    return os.path.join(PASTA_DADOS, nome_arquivo)


def salvar_linha(nome_arquivo: str, campos: list[object]) -> None:
    """Acrescenta uma linha no arquivo (sem apagar o que ja existe)."""
    linha = "|".join(str(campo) for campo in campos)
    try:
        os.makedirs(PASTA_DADOS, exist_ok=True)
        with open(caminho_arquivo(nome_arquivo), "a", encoding="utf-8") as arquivo:
            arquivo.write(linha + "\n")
    except OSError as erro:
        raise PersistenciaError(f"Nao foi possivel gravar em '{nome_arquivo}': {erro}") from erro


def ler_linhas(nome_arquivo: str) -> list[list[str]]:
    """Le o arquivo e devolve uma lista de registros (cada um e uma lista de campos).
    Se o arquivo ainda nao existe, devolve lista vazia."""
    caminho = caminho_arquivo(nome_arquivo)
    if not os.path.exists(caminho):
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]
    except (OSError, UnicodeDecodeError) as erro:
        raise PersistenciaError(f"Nao foi possivel ler '{nome_arquivo}': {erro}") from erro
    return [linha.split("|") for linha in linhas]


def regravar_arquivo(nome_arquivo: str, linhas: list[list[object]]) -> None:
    """Reescreve o arquivo inteiro (usado quando um registro existente e editado).
    Grava primeiro num arquivo temporario para nao perder dados se der erro no meio."""
    caminho = caminho_arquivo(nome_arquivo)
    temporario = caminho + ".tmp"
    try:
        os.makedirs(PASTA_DADOS, exist_ok=True)
        with open(temporario, "w", encoding="utf-8") as arquivo:
            for campos in linhas:
                arquivo.write("|".join(str(campo) for campo in campos) + "\n")
        os.replace(temporario, caminho)
    except OSError as erro:
        raise PersistenciaError(f"Nao foi possivel regravar '{nome_arquivo}': {erro}") from erro


def _carregar(nome_arquivo: str, construir: Callable[[list[str]], None]) -> None:
    """Percorre o arquivo e chama `construir` para cada registro.
    Linha corrompida (campos faltando, numero invalido, dado que o modelo recusa)
    e ignorada com um aviso, em vez de derrubar o programa inteiro."""
    for numero, campos in enumerate(ler_linhas(nome_arquivo), start=1):
        try:
            construir(campos)
        except ValueError as erro:  # inclui ValidacaoError e erros de conversao/desempacotamento
            print(f"[AVISO] {nome_arquivo}, linha {numero} ignorada (dados invalidos): {erro}")


def _achar_cidadao(id_cidadao: str) -> Cidadao | None:
    return next((c for c in cidadaos if c.id_usuario == int(id_cidadao)), None)


# ==========================================================
# Salvar (acrescenta uma linha) e carregar, por entidade
# ==========================================================
def salvar_cidadao(cidadao: Cidadao) -> None:
    salvar_linha("cidadaos.txt", [
        cidadao.id_usuario, cidadao.nome, cidadao.email, cidadao.senha,
        cidadao.data_cadastro.isoformat(), cidadao.rua, cidadao.numero,
        cidadao.bairro, cidadao.cidade, cidadao.cep,
    ])


def carregar_cidadaos() -> None:
    def construir(campos: list[str]) -> None:
        id_usuario, nome, email, senha, data_cadastro, rua, numero, bairro, cidade, cep = campos
        cidadaos.append(Cidadao(int(id_usuario), nome, email, senha,
                                date.fromisoformat(data_cadastro), rua, numero, bairro, cidade, cep))
    _carregar("cidadaos.txt", construir)


def salvar_agente(agente: AgenteResgate) -> None:
    salvar_linha("agentes.txt", [
        agente.id_usuario, agente.nome, agente.email, agente.senha,
        agente.data_cadastro.isoformat(), agente.matricula, agente.cargo,
    ])


def carregar_agentes() -> None:
    def construir(campos: list[str]) -> None:
        id_usuario, nome, email, senha, data_cadastro, matricula, cargo = campos
        agentes.append(AgenteResgate(int(id_usuario), nome, email, senha,
                                     date.fromisoformat(data_cadastro), matricula, cargo))
    _carregar("agentes.txt", construir)


def salvar_equipe(equipe: EquipeResgate) -> None:
    salvar_linha("equipes.txt", [equipe.id_equipe, equipe.nome_equipe, equipe.area_atuacao])


def carregar_equipes() -> None:
    def construir(campos: list[str]) -> None:
        id_equipe, nome_equipe, area_atuacao = campos
        equipes.append(EquipeResgate(int(id_equipe), nome_equipe, area_atuacao))
    _carregar("equipes.txt", construir)


def salvar_especie(especie: Especie) -> None:
    salvar_linha("especies.txt", [
        especie.id_especie, especie.nome_popular, especie.nome_cientifico,
        especie.nivel_risco, especie.orientacoes_captura,
    ])


def carregar_especies() -> None:
    def construir(campos: list[str]) -> None:
        id_especie, nome_popular, nome_cientifico, nivel_risco, orientacoes = campos
        especies.append(Especie(int(id_especie), nome_popular, nome_cientifico, nivel_risco, orientacoes))
    _carregar("especies.txt", construir)


def salvar_produto(produto: Produto) -> None:
    salvar_linha("produtos.txt", [
        produto.id_produto, produto.nome, produto.descricao, produto.preco, produto.categoria,
    ])


def carregar_produtos() -> None:
    def construir(campos: list[str]) -> None:
        id_produto, nome, descricao, preco, categoria = campos
        produtos.append(Produto(int(id_produto), nome, descricao, float(preco), categoria))
    _carregar("produtos.txt", construir)


def salvar_solicitacao(solicitacao: SolicitacaoResgate) -> None:
    salvar_linha("solicitacoes.txt", [
        solicitacao.id_solicitacao, solicitacao.data_hora.isoformat(),
        solicitacao.descricao, solicitacao.status, solicitacao.cidadao.id_usuario,
    ])


def carregar_solicitacoes() -> None:
    def construir(campos: list[str]) -> None:
        id_solicitacao, data_hora, descricao, status, id_cidadao = campos
        cidadao = _achar_cidadao(id_cidadao)
        if cidadao is None:
            return
        solicitacoes.append(SolicitacaoResgate(int(id_solicitacao), datetime.fromisoformat(data_hora),
                                               descricao, status, cidadao))
    _carregar("solicitacoes.txt", construir)


def _itens_para_texto(pedido: Pedido) -> str:
    return ";".join(f"{i.produto.id_produto}:{i.quantidade}:{i.preco_unitario}" for i in pedido.itens)


def salvar_pedido(pedido: Pedido) -> None:
    salvar_linha("pedidos.txt", [
        pedido.id_pedido, pedido.data_pedido.isoformat(), pedido.status_pedido,
        pedido.aceite_termo_resp, pedido.cidadao.id_usuario, _itens_para_texto(pedido),
    ])


def carregar_pedidos() -> None:
    def construir(campos: list[str]) -> None:
        id_pedido, data_pedido, status_pedido, aceite_termo_resp, id_cidadao, itens_texto = campos
        cidadao = _achar_cidadao(id_cidadao)
        if cidadao is None:
            return
        # O pedido nasce "Pendente" porque so pedidos pendentes aceitam novos itens
        # (regra do decorador @requer_status_pedido). O status salvo e restaurado no fim.
        pedido = Pedido(int(id_pedido), date.fromisoformat(data_pedido), "Pendente",
                        aceite_termo_resp == "True", cidadao)
        if itens_texto:
            for item_texto in itens_texto.split(";"):
                id_produto, quantidade, preco_unitario = item_texto.split(":")
                produto = next((p for p in produtos if p.id_produto == int(id_produto)), None)
                if produto is None:
                    continue
                pedido += ItemPedido(produto, int(quantidade), float(preco_unitario))
        pedido.status_pedido = status_pedido
        pedidos.append(pedido)
    _carregar("pedidos.txt", construir)


# ==========================================================
# Regravar (usado depois de editar um registro existente)
# ==========================================================
def regravar_cidadaos() -> None:
    regravar_arquivo("cidadaos.txt", [
        [c.id_usuario, c.nome, c.email, c.senha, c.data_cadastro.isoformat(),
         c.rua, c.numero, c.bairro, c.cidade, c.cep]
        for c in cidadaos
    ])


def regravar_agentes() -> None:
    regravar_arquivo("agentes.txt", [
        [a.id_usuario, a.nome, a.email, a.senha, a.data_cadastro.isoformat(), a.matricula, a.cargo]
        for a in agentes
    ])


def regravar_equipes() -> None:
    regravar_arquivo("equipes.txt", [[e.id_equipe, e.nome_equipe, e.area_atuacao] for e in equipes])


def regravar_especies() -> None:
    regravar_arquivo("especies.txt", [
        [e.id_especie, e.nome_popular, e.nome_cientifico, e.nivel_risco, e.orientacoes_captura]
        for e in especies
    ])


def regravar_produtos() -> None:
    regravar_arquivo("produtos.txt", [
        [p.id_produto, p.nome, p.descricao, p.preco, p.categoria] for p in produtos
    ])


def regravar_solicitacoes() -> None:
    regravar_arquivo("solicitacoes.txt", [
        [s.id_solicitacao, s.data_hora.isoformat(), s.descricao, s.status, s.cidadao.id_usuario]
        for s in solicitacoes
    ])


def regravar_pedidos() -> None:
    regravar_arquivo("pedidos.txt", [
        [p.id_pedido, p.data_pedido.isoformat(), p.status_pedido,
         p.aceite_termo_resp, p.cidadao.id_usuario, _itens_para_texto(p)]
        for p in pedidos
    ])


# ==========================================================
# Regras de unicidade
# ==========================================================
def garantir_email_cidadao_unico(email: str, ignorar: Cidadao | None = None) -> None:
    """Levanta RegistroDuplicadoError se outro cidadao ja usa este email.
    `ignorar` serve para a edicao: o proprio cidadao nao conta como duplicado."""
    email = email.strip().casefold()
    if not email:
        return
    for outro in cidadaos:
        if outro is not ignorar and outro.email.casefold() == email:
            raise RegistroDuplicadoError(f"Ja existe um cidadao com o email '{email}'.")


def garantir_matricula_unica(matricula: str, ignorar: AgenteResgate | None = None) -> None:
    """Levanta RegistroDuplicadoError se outro agente ja usa esta matricula."""
    matricula = matricula.strip().casefold()
    if not matricula:
        return
    for outro in agentes:
        if outro is not ignorar and outro.matricula.casefold() == matricula:
            raise RegistroDuplicadoError(f"Ja existe um agente com a matricula '{matricula}'.")


# ==========================================================
# Carga inicial
# ==========================================================
@cronometrar  # decorador: mostra no console quanto tempo a leitura dos .txt levou
def carregar_dados() -> None:
    """Le todos os arquivos .txt e reconstroi as listas em memoria."""
    global proximo_id
    carregar_cidadaos()
    carregar_agentes()
    carregar_equipes()
    carregar_especies()
    carregar_produtos()
    carregar_solicitacoes()  # depende dos cidadaos ja carregados
    carregar_pedidos()       # depende dos cidadaos e produtos ja carregados

    todos_ids = (
        [c.id_usuario for c in cidadaos] + [a.id_usuario for a in agentes]
        + [e.id_equipe for e in equipes] + [e.id_especie for e in especies]
        + [p.id_produto for p in produtos] + [s.id_solicitacao for s in solicitacoes]
        + [p.id_pedido for p in pedidos]
    )
    if todos_ids:
        proximo_id = max(todos_ids) + 1
