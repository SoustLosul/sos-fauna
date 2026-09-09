import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from model.cidadao import Cidadao
from model.agente_resgate import AgenteResgate
from model.equipe_resgate import EquipeResgate
from model.especie import Especie
from model.solicitacao_resgate import SolicitacaoResgate
from model.produto import Produto
from model.item_pedido import ItemPedido
from model.pedido import Pedido


# "banco de dados" em memória
cidadaos = []
agentes = []
equipes = []
especies = []
solicitacoes = []
produtos = []
pedidos = []

proximo_id = 1


def gerar_id():
    global proximo_id
    id_atual = proximo_id
    proximo_id += 1
    return id_atual


# ==========================================================
# Persistencia txt
# ==========================================================
# Cada tipo de cadastro fica salvo em um arquivo .txt dentro da
# pasta "dados". Cada linha do arquivo representa um registro,
# com os campos separados por "|".

PASTA_DADOS = "dados"


def caminho_arquivo(nome_arquivo):
    return os.path.join(PASTA_DADOS, nome_arquivo)


def salvar_linha(nome_arquivo, campos):
    """Acrescenta uma linha no arquivo (sem apagar o que ja existe)."""
    os.makedirs(PASTA_DADOS, exist_ok=True)
    linha = "|".join(str(campo) for campo in campos)
    with open(caminho_arquivo(nome_arquivo), "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")


def ler_linhas(nome_arquivo):
    """Le todas as linhas do arquivo e devolve uma lista de listas de campos."""
    caminho = caminho_arquivo(nome_arquivo)
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]
    return [linha.split("|") for linha in linhas]


def salvar_cidadao(cidadao):
    salvar_linha("cidadaos.txt", [
        cidadao.id_usuario, cidadao.nome, cidadao.email, cidadao.senha,
        cidadao.data_cadastro.isoformat(), cidadao.rua, cidadao.numero,
        cidadao.bairro, cidadao.cidade, cidadao.cep,
    ])


def carregar_cidadaos():
    for campos in ler_linhas("cidadaos.txt"):
        id_usuario, nome, email, senha, data_cadastro, rua, numero, bairro, cidade, cep = campos
        cidadao = Cidadao(int(id_usuario), nome, email, senha,
                           date.fromisoformat(data_cadastro), rua, numero, bairro, cidade, cep)
        cidadaos.append(cidadao)


def salvar_agente(agente):
    salvar_linha("agentes.txt", [
        agente.id_usuario, agente.nome, agente.email, agente.senha,
        agente.data_cadastro.isoformat(), agente.matricula, agente.cargo,
    ])


def carregar_agentes():
    for campos in ler_linhas("agentes.txt"):
        id_usuario, nome, email, senha, data_cadastro, matricula, cargo = campos
        agente = AgenteResgate(int(id_usuario), nome, email, senha,
                                date.fromisoformat(data_cadastro), matricula, cargo)
        agentes.append(agente)


def salvar_equipe(equipe):
    salvar_linha("equipes.txt", [equipe.id_equipe, equipe.nome_equipe, equipe.area_atuacao])


def carregar_equipes():
    for campos in ler_linhas("equipes.txt"):
        id_equipe, nome_equipe, area_atuacao = campos
        equipe = EquipeResgate(int(id_equipe), nome_equipe, area_atuacao)
        equipes.append(equipe)


def salvar_especie(especie):
    salvar_linha("especies.txt", [
        especie.id_especie, especie.nome_popular, especie.nome_cientifico,
        especie.nivel_risco, especie.orientacoes_captura,
    ])


def carregar_especies():
    for campos in ler_linhas("especies.txt"):
        id_especie, nome_popular, nome_cientifico, nivel_risco, orientacoes = campos
        especie = Especie(int(id_especie), nome_popular, nome_cientifico, nivel_risco, orientacoes)
        especies.append(especie)


def salvar_produto(produto):
    salvar_linha("produtos.txt", [
        produto.id_produto, produto.nome, produto.descricao, produto.preco, produto.categoria,
    ])


def carregar_produtos():
    for campos in ler_linhas("produtos.txt"):
        id_produto, nome, descricao, preco, categoria = campos
        produto = Produto(int(id_produto), nome, descricao, float(preco), categoria)
        produtos.append(produto)


def salvar_solicitacao(solicitacao):
    salvar_linha("solicitacoes.txt", [
        solicitacao.id_solicitacao, solicitacao.data_hora.isoformat(),
        solicitacao.descricao, solicitacao.status, solicitacao.cidadao.id_usuario,
    ])


def carregar_solicitacoes():
    for campos in ler_linhas("solicitacoes.txt"):
        id_solicitacao, data_hora, descricao, status, id_cidadao = campos
        cidadao = next((c for c in cidadaos if c.id_usuario == int(id_cidadao)), None)
        if cidadao is None:
            continue
        solicitacao = SolicitacaoResgate(int(id_solicitacao), datetime.fromisoformat(data_hora),
                                          descricao, status, cidadao)
        solicitacoes.append(solicitacao)


def salvar_pedido(pedido):
    itens_texto = ";".join(
        f"{item.produto.id_produto}:{item.quantidade}:{item.preco_unitario}"
        for item in pedido.itens
    )
    salvar_linha("pedidos.txt", [
        pedido.id_pedido, pedido.data_pedido.isoformat(), pedido.status_pedido,
        pedido.aceite_termo_resp, pedido.cidadao.id_usuario, itens_texto,
    ])


def carregar_pedidos():
    for campos in ler_linhas("pedidos.txt"):
        id_pedido, data_pedido, status_pedido, aceite_termo_resp, id_cidadao, itens_texto = campos
        cidadao = next((c for c in cidadaos if c.id_usuario == int(id_cidadao)), None)
        if cidadao is None:
            continue
        pedido = Pedido(int(id_pedido), date.fromisoformat(data_pedido), status_pedido,
                         aceite_termo_resp == "True", cidadao)
        if itens_texto:
            for item_texto in itens_texto.split(";"):
                id_produto, quantidade, preco_unitario = item_texto.split(":")
                produto = next((p for p in produtos if p.id_produto == int(id_produto)), None)
                if produto is None:
                    continue
                pedido.adicionar_item(ItemPedido(produto, int(quantidade), float(preco_unitario)))
        pedidos.append(pedido)


# ----------------------------------------------------------------
# Reescrita completa dos arquivos (usada quando um registro existente
# e editado, ja que "salvar_x" so acrescenta uma linha nova)
# ----------------------------------------------------------------

def regravar_arquivo(nome_arquivo, linhas):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    with open(caminho_arquivo(nome_arquivo), "w", encoding="utf-8") as arquivo:
        for campos in linhas:
            arquivo.write("|".join(str(campo) for campo in campos) + "\n")


def regravar_cidadaos():
    regravar_arquivo("cidadaos.txt", [
        [c.id_usuario, c.nome, c.email, c.senha, c.data_cadastro.isoformat(),
         c.rua, c.numero, c.bairro, c.cidade, c.cep]
        for c in cidadaos
    ])


def regravar_agentes():
    regravar_arquivo("agentes.txt", [
        [a.id_usuario, a.nome, a.email, a.senha, a.data_cadastro.isoformat(), a.matricula, a.cargo]
        for a in agentes
    ])


def regravar_equipes():
    regravar_arquivo("equipes.txt", [[e.id_equipe, e.nome_equipe, e.area_atuacao] for e in equipes])


def regravar_especies():
    regravar_arquivo("especies.txt", [
        [e.id_especie, e.nome_popular, e.nome_cientifico, e.nivel_risco, e.orientacoes_captura]
        for e in especies
    ])


def regravar_produtos():
    regravar_arquivo("produtos.txt", [
        [p.id_produto, p.nome, p.descricao, p.preco, p.categoria] for p in produtos
    ])


def regravar_solicitacoes():
    regravar_arquivo("solicitacoes.txt", [
        [s.id_solicitacao, s.data_hora.isoformat(), s.descricao, s.status, s.cidadao.id_usuario]
        for s in solicitacoes
    ])


def regravar_pedidos():
    linhas = []
    for p in pedidos:
        itens_texto = ";".join(
            f"{item.produto.id_produto}:{item.quantidade}:{item.preco_unitario}"
            for item in p.itens
        )
        linhas.append([p.id_pedido, p.data_pedido.isoformat(), p.status_pedido,
                        p.aceite_termo_resp, p.cidadao.id_usuario, itens_texto])
    regravar_arquivo("pedidos.txt", linhas)


def carregar_dados():
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


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SOS Fauna Urbana")
        self.geometry("800x550")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_cidadao = AbaCidadao(notebook)
        self.aba_agente = AbaAgente(notebook)
        self.aba_equipe = AbaEquipe(notebook)
        self.aba_especie = AbaEspecie(notebook)
        self.aba_produto = AbaProduto(notebook)
        self.aba_solicitacao = AbaSolicitacao(notebook)
        self.aba_pedido = AbaPedido(notebook)

        notebook.add(self.aba_cidadao, text="Cidadaos")
        notebook.add(self.aba_agente, text="Agentes")
        notebook.add(self.aba_equipe, text="Equipes")
        notebook.add(self.aba_especie, text="Especies")
        notebook.add(self.aba_produto, text="Produtos")
        notebook.add(self.aba_solicitacao, text="Solicitacoes")
        notebook.add(self.aba_pedido, text="Pedidos")

        # Mostra na tela os dados que ja foram carregados dos arquivos .txt
        self.aba_cidadao.atualizar_lista()
        self.aba_agente.atualizar_lista()
        self.aba_equipe.atualizar_lista()
        self.aba_especie.atualizar_lista()
        self.aba_produto.atualizar_lista()
        self.aba_solicitacao.atualizar_lista()
        self.aba_pedido.atualizar_lista_pedidos()


# ---------- cidadao ----------
class AbaCidadao(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        campos = ["Nome", "Email", "Senha", "Rua", "Numero", "Bairro", "Cidade", "CEP"]
        self.entradas = {}

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)
        for i, campo in enumerate(campos):
            ttk.Label(form, text=campo + ":").grid(row=i, column=0, sticky="w", pady=2)
            entrada = ttk.Entry(form, width=40)
            entrada.grid(row=i, column=1, pady=2, padx=5)
            self.entradas[campo] = entrada

        ttk.Button(self, text="Cadastrar", command=self.cadastrar).pack(pady=5)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        self.lista.bind("<Double-Button-1>", self.abrir_detalhes)

    def cadastrar(self):
        nome = self.entradas["Nome"].get()
        email = self.entradas["Email"].get()
        senha = self.entradas["Senha"].get()
        rua = self.entradas["Rua"].get()
        numero = self.entradas["Numero"].get()
        bairro = self.entradas["Bairro"].get()
        cidade = self.entradas["Cidade"].get()
        cep = self.entradas["CEP"].get()

        if not nome or not email:
            messagebox.showwarning("Atencao", "Preencha ao menos Nome e Email.")
            return

        cidadao = Cidadao(gerar_id(), nome, email, senha, date.today(),
                           rua, numero, bairro, cidade, cep)
        cidadaos.append(cidadao)
        salvar_cidadao(cidadao)

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Cidadao cadastrado! ID: {cidadao.id_usuario}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for c in cidadaos:
            self.lista.insert(tk.END, f"{c.id_usuario} - {c}")

    def abrir_detalhes(self, event=None):
        selecionado = self.lista.curselection()
        if not selecionado:
            return
        cidadao = cidadaos[selecionado[0]]

        janela = tk.Toplevel(self)
        janela.title(f"Cidadao #{cidadao.id_usuario}")
        janela.geometry("340x430")

        campos = {
            "Nome": cidadao.nome, "Email": cidadao.email, "Senha": cidadao.senha,
            "Rua": cidadao.rua, "Numero": cidadao.numero, "Bairro": cidadao.bairro,
            "Cidade": cidadao.cidade, "CEP": cidadao.cep,
        }
        entradas = {}
        for i, (rotulo, valor) in enumerate(campos.items()):
            ttk.Label(janela, text=rotulo + ":").grid(row=i, column=0, sticky="w", padx=10, pady=4)
            entrada = ttk.Entry(janela, width=28)
            entrada.insert(0, valor)
            entrada.grid(row=i, column=1, padx=10, pady=4)
            entradas[rotulo] = entrada

        ttk.Label(janela, text=f"Cadastrado em: {cidadao.data_cadastro}").grid(
            row=len(campos), column=0, columnspan=2, sticky="w", padx=10, pady=8)

        def salvar_alteracoes():
            cidadao.nome = entradas["Nome"].get()
            cidadao.email = entradas["Email"].get()
            cidadao.senha = entradas["Senha"].get()
            cidadao.rua = entradas["Rua"].get()
            cidadao.numero = entradas["Numero"].get()
            cidadao.bairro = entradas["Bairro"].get()
            cidadao.cidade = entradas["Cidade"].get()
            cidadao.cep = entradas["CEP"].get()
            regravar_cidadaos()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Dados do cidadao atualizados!")
            janela.destroy()

        ttk.Button(janela, text="Salvar alteracoes", command=salvar_alteracoes).grid(
            row=len(campos) + 1, column=0, columnspan=2, pady=15)


# ---------- agente ----------
class AbaAgente(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        campos = ["Nome", "Email", "Senha", "Matricula", "Cargo"]
        self.entradas = {}

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)
        for i, campo in enumerate(campos):
            ttk.Label(form, text=campo + ":").grid(row=i, column=0, sticky="w", pady=2)
            entrada = ttk.Entry(form, width=40)
            entrada.grid(row=i, column=1, pady=2, padx=5)
            self.entradas[campo] = entrada

        ttk.Button(self, text="Cadastrar", command=self.cadastrar).pack(pady=5)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        self.lista.bind("<Double-Button-1>", self.abrir_detalhes)

    def cadastrar(self):
        nome = self.entradas["Nome"].get()
        email = self.entradas["Email"].get()
        senha = self.entradas["Senha"].get()
        matricula = self.entradas["Matricula"].get()
        cargo = self.entradas["Cargo"].get()

        if not nome or not matricula:
            messagebox.showwarning("Atencao", "Preencha ao menos Nome e Matricula.")
            return

        agente = AgenteResgate(gerar_id(), nome, email, senha, date.today(), matricula, cargo)
        agentes.append(agente)
        salvar_agente(agente)

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Agente cadastrado! ID: {agente.id_usuario}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for a in agentes:
            self.lista.insert(tk.END, f"{a.id_usuario} - {a}")

    def abrir_detalhes(self, event=None):
        selecionado = self.lista.curselection()
        if not selecionado:
            return
        agente = agentes[selecionado[0]]

        janela = tk.Toplevel(self)
        janela.title(f"Agente #{agente.id_usuario}")
        janela.geometry("340x300")

        campos = {
            "Nome": agente.nome, "Email": agente.email, "Senha": agente.senha,
            "Matricula": agente.matricula, "Cargo": agente.cargo,
        }
        entradas = {}
        for i, (rotulo, valor) in enumerate(campos.items()):
            ttk.Label(janela, text=rotulo + ":").grid(row=i, column=0, sticky="w", padx=10, pady=4)
            entrada = ttk.Entry(janela, width=28)
            entrada.insert(0, valor)
            entrada.grid(row=i, column=1, padx=10, pady=4)
            entradas[rotulo] = entrada

        ttk.Label(janela, text=f"Cadastrado em: {agente.data_cadastro}").grid(
            row=len(campos), column=0, columnspan=2, sticky="w", padx=10, pady=8)

        def salvar_alteracoes():
            agente.nome = entradas["Nome"].get()
            agente.email = entradas["Email"].get()
            agente.senha = entradas["Senha"].get()
            agente.matricula = entradas["Matricula"].get()
            agente.cargo = entradas["Cargo"].get()
            regravar_agentes()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Dados do agente atualizados!")
            janela.destroy()

        ttk.Button(janela, text="Salvar alteracoes", command=salvar_alteracoes).grid(
            row=len(campos) + 1, column=0, columnspan=2, pady=15)


# ---------- equipe ----------
class AbaEquipe(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        campos = ["Nome da equipe", "Area de atuacao"]
        self.entradas = {}

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)
        for i, campo in enumerate(campos):
            ttk.Label(form, text=campo + ":").grid(row=i, column=0, sticky="w", pady=2)
            entrada = ttk.Entry(form, width=40)
            entrada.grid(row=i, column=1, pady=2, padx=5)
            self.entradas[campo] = entrada

        ttk.Button(self, text="Cadastrar", command=self.cadastrar).pack(pady=5)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        self.lista.bind("<Double-Button-1>", self.abrir_detalhes)

    def cadastrar(self):
        nome_equipe = self.entradas["Nome da equipe"].get()
        area_atuacao = self.entradas["Area de atuacao"].get()

        if not nome_equipe:
            messagebox.showwarning("Atencao", "Preencha o nome da equipe.")
            return

        equipe = EquipeResgate(gerar_id(), nome_equipe, area_atuacao)
        equipes.append(equipe)
        salvar_equipe(equipe)

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Equipe cadastrada! ID: {equipe.id_equipe}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for e in equipes:
            self.lista.insert(tk.END, f"{e.id_equipe} - {e}")

    def abrir_detalhes(self, event=None):
        selecionado = self.lista.curselection()
        if not selecionado:
            return
        equipe = equipes[selecionado[0]]

        janela = tk.Toplevel(self)
        janela.title(f"Equipe #{equipe.id_equipe}")
        janela.geometry("340x220")

        campos = {"Nome da equipe": equipe.nome_equipe, "Area de atuacao": equipe.area_atuacao}
        entradas = {}
        for i, (rotulo, valor) in enumerate(campos.items()):
            ttk.Label(janela, text=rotulo + ":").grid(row=i, column=0, sticky="w", padx=10, pady=4)
            entrada = ttk.Entry(janela, width=28)
            entrada.insert(0, valor)
            entrada.grid(row=i, column=1, padx=10, pady=4)
            entradas[rotulo] = entrada

        integrantes = ", ".join(a.nome for a in equipe.agentes) or "Nenhum"
        ttk.Label(janela, text=f"Agentes na equipe: {integrantes}").grid(
            row=len(campos), column=0, columnspan=2, sticky="w", padx=10, pady=8)

        def salvar_alteracoes():
            equipe.nome_equipe = entradas["Nome da equipe"].get()
            equipe.area_atuacao = entradas["Area de atuacao"].get()
            regravar_equipes()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Dados da equipe atualizados!")
            janela.destroy()

        ttk.Button(janela, text="Salvar alteracoes", command=salvar_alteracoes).grid(
            row=len(campos) + 1, column=0, columnspan=2, pady=15)


# ---------- especie ----------
class AbaEspecie(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        campos = ["Nome popular", "Nome cientifico", "Nivel de risco", "Orientacoes de captura"]
        self.entradas = {}

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)
        for i, campo in enumerate(campos):
            ttk.Label(form, text=campo + ":").grid(row=i, column=0, sticky="w", pady=2)
            entrada = ttk.Entry(form, width=40)
            entrada.grid(row=i, column=1, pady=2, padx=5)
            self.entradas[campo] = entrada

        ttk.Button(self, text="Cadastrar", command=self.cadastrar).pack(pady=5)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        self.lista.bind("<Double-Button-1>", self.abrir_detalhes)

    def cadastrar(self):
        nome_popular = self.entradas["Nome popular"].get()
        nome_cientifico = self.entradas["Nome cientifico"].get()
        nivel_risco = self.entradas["Nivel de risco"].get()
        orientacoes = self.entradas["Orientacoes de captura"].get()

        if not nome_popular:
            messagebox.showwarning("Atencao", "Preencha o nome popular.")
            return

        especie = Especie(gerar_id(), nome_popular, nome_cientifico, nivel_risco, orientacoes)
        especies.append(especie)
        salvar_especie(especie)

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Especie cadastrada! ID: {especie.id_especie}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for e in especies:
            self.lista.insert(tk.END, f"{e.id_especie} - {e}")

    def abrir_detalhes(self, event=None):
        selecionado = self.lista.curselection()
        if not selecionado:
            return
        especie = especies[selecionado[0]]

        janela = tk.Toplevel(self)
        janela.title(f"Especie #{especie.id_especie}")
        janela.geometry("360x260")

        campos = {
            "Nome popular": especie.nome_popular, "Nome cientifico": especie.nome_cientifico,
            "Nivel de risco": especie.nivel_risco, "Orientacoes de captura": especie.orientacoes_captura,
        }
        entradas = {}
        for i, (rotulo, valor) in enumerate(campos.items()):
            ttk.Label(janela, text=rotulo + ":").grid(row=i, column=0, sticky="w", padx=10, pady=4)
            entrada = ttk.Entry(janela, width=28)
            entrada.insert(0, valor)
            entrada.grid(row=i, column=1, padx=10, pady=4)
            entradas[rotulo] = entrada

        def salvar_alteracoes():
            especie.nome_popular = entradas["Nome popular"].get()
            especie.nome_cientifico = entradas["Nome cientifico"].get()
            especie.nivel_risco = entradas["Nivel de risco"].get()
            especie.orientacoes_captura = entradas["Orientacoes de captura"].get()
            regravar_especies()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Dados da especie atualizados!")
            janela.destroy()

        ttk.Button(janela, text="Salvar alteracoes", command=salvar_alteracoes).grid(
            row=len(campos) + 1, column=0, columnspan=2, pady=15)


# ---------- produto ----------
class AbaProduto(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        campos = ["Nome", "Descricao", "Preco", "Categoria"]
        self.entradas = {}

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)
        for i, campo in enumerate(campos):
            ttk.Label(form, text=campo + ":").grid(row=i, column=0, sticky="w", pady=2)
            entrada = ttk.Entry(form, width=40)
            entrada.grid(row=i, column=1, pady=2, padx=5)
            self.entradas[campo] = entrada

        ttk.Button(self, text="Cadastrar", command=self.cadastrar).pack(pady=5)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        self.lista.bind("<Double-Button-1>", self.abrir_detalhes)

    def cadastrar(self):
        nome = self.entradas["Nome"].get()
        descricao = self.entradas["Descricao"].get()
        categoria = self.entradas["Categoria"].get()

        try:
            preco = float(self.entradas["Preco"].get())
        except ValueError:
            messagebox.showerror("Erro", "Preco invalido.")
            return

        if not nome:
            messagebox.showwarning("Atencao", "Preencha o nome do produto.")
            return

        produto = Produto(gerar_id(), nome, descricao, preco, categoria)
        produtos.append(produto)
        salvar_produto(produto)

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Produto cadastrado! ID: {produto.id_produto}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for p in produtos:
            self.lista.insert(tk.END, f"{p.id_produto} - {p}")

    def abrir_detalhes(self, event=None):
        selecionado = self.lista.curselection()
        if not selecionado:
            return
        produto = produtos[selecionado[0]]

        janela = tk.Toplevel(self)
        janela.title(f"Produto #{produto.id_produto}")
        janela.geometry("340x220")

        campos_texto = {
            "Nome": produto.nome, "Descricao": produto.descricao, "Categoria": produto.categoria,
        }
        entradas = {}
        for i, (rotulo, valor) in enumerate(campos_texto.items()):
            ttk.Label(janela, text=rotulo + ":").grid(row=i, column=0, sticky="w", padx=10, pady=4)
            entrada = ttk.Entry(janela, width=28)
            entrada.insert(0, valor)
            entrada.grid(row=i, column=1, padx=10, pady=4)
            entradas[rotulo] = entrada

        ttk.Label(janela, text="Preco:").grid(row=len(campos_texto), column=0, sticky="w", padx=10, pady=4)
        entrada_preco = ttk.Entry(janela, width=28)
        entrada_preco.insert(0, f"{produto.preco:.2f}")
        entrada_preco.grid(row=len(campos_texto), column=1, padx=10, pady=4)

        def salvar_alteracoes():
            try:
                novo_preco = float(entrada_preco.get())
            except ValueError:
                messagebox.showerror("Erro", "Preco invalido.")
                return
            produto.nome = entradas["Nome"].get()
            produto.descricao = entradas["Descricao"].get()
            produto.categoria = entradas["Categoria"].get()
            produto.preco = novo_preco
            regravar_produtos()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Dados do produto atualizados!")
            janela.destroy()

        ttk.Button(janela, text="Salvar alteracoes", command=salvar_alteracoes).grid(
            row=len(campos_texto) + 1, column=0, columnspan=2, pady=15)


# ---------- solicitacao ----------
class AbaSolicitacao(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Cidadao:").grid(row=0, column=0, sticky="w", pady=2)
        self.combo_cidadao = ttk.Combobox(form, width=37, state="readonly")
        self.combo_cidadao.grid(row=0, column=1, pady=2, padx=5)

        ttk.Label(form, text="Descricao:").grid(row=1, column=0, sticky="w", pady=2)
        self.entrada_descricao = ttk.Entry(form, width=40)
        self.entrada_descricao.grid(row=1, column=1, pady=2, padx=5)

        botoes = ttk.Frame(self)
        botoes.pack(pady=5)
        ttk.Button(botoes, text="Atualizar cidadaos", command=self.atualizar_combo).pack(side="left", padx=5)
        ttk.Button(botoes, text="Abrir Solicitacao", command=self.abrir).pack(side="left", padx=5)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        self.lista.bind("<Double-Button-1>", self.abrir_detalhes)

    def atualizar_combo(self):
        valores = [f"{c.id_usuario} - {c.nome}" for c in cidadaos]
        self.combo_cidadao["values"] = valores
        if valores:
            self.combo_cidadao.current(0)

    def abrir(self):
        if not self.combo_cidadao.get():
            messagebox.showwarning("Atencao", "Selecione um cidadao (clique em 'Atualizar cidadaos').")
            return

        id_cidadao = int(self.combo_cidadao.get().split(" - ")[0])
        cidadao = next((c for c in cidadaos if c.id_usuario == id_cidadao), None)
        if not cidadao:
            messagebox.showerror("Erro", "Cidadao nao encontrado.")
            return

        descricao = self.entrada_descricao.get()
        if not descricao:
            messagebox.showwarning("Atencao", "Descreva a ocorrencia.")
            return

        solicitacao = SolicitacaoResgate(gerar_id(), datetime.now(), descricao, "Aberta", cidadao)
        solicitacoes.append(solicitacao)
        salvar_solicitacao(solicitacao)

        self.entrada_descricao.delete(0, tk.END)
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Solicitacao aberta! ID: {solicitacao.id_solicitacao}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for s in solicitacoes:
            self.lista.insert(tk.END, f"{s.id_solicitacao} - {s} - Cidadao: {s.cidadao.nome}")

    def abrir_detalhes(self, event=None):
        selecionado = self.lista.curselection()
        if not selecionado:
            return
        solicitacao = solicitacoes[selecionado[0]]

        janela = tk.Toplevel(self)
        janela.title(f"Solicitacao #{solicitacao.id_solicitacao}")
        janela.geometry("420x380")

        ttk.Label(janela, text=f"Cidadao: {solicitacao.cidadao.nome}").pack(anchor="w", padx=10, pady=4)
        ttk.Label(
            janela, text=f"Aberta em: {solicitacao.data_hora.strftime('%d/%m/%Y %H:%M')}"
        ).pack(anchor="w", padx=10)

        ttk.Label(janela, text="Descricao da ocorrencia:").pack(anchor="w", padx=10, pady=(12, 0))
        texto_descricao = tk.Text(janela, width=46, height=7, wrap="word")
        texto_descricao.insert("1.0", solicitacao.descricao)
        texto_descricao.pack(padx=10, pady=4)

        ttk.Label(janela, text="Status:").pack(anchor="w", padx=10, pady=(12, 0))
        combo_status = ttk.Combobox(
            janela, state="readonly",
            values=["Aberta", "Em atendimento", "Concluida", "Cancelada"],
        )
        combo_status.set(solicitacao.status)
        combo_status.pack(padx=10, pady=4, anchor="w")

        def salvar_alteracoes():
            solicitacao.descricao = texto_descricao.get("1.0", tk.END).strip()
            solicitacao.status = combo_status.get()
            regravar_solicitacoes()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Solicitacao atualizada!")
            janela.destroy()

        ttk.Button(janela, text="Salvar alteracoes", command=salvar_alteracoes).pack(pady=15)


# ---------- pedido ----------
class AbaPedido(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.itens_pedido = []

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Cidadao:").grid(row=0, column=0, sticky="w", pady=2)
        self.combo_cidadao = ttk.Combobox(form, width=30, state="readonly")
        self.combo_cidadao.grid(row=0, column=1, pady=2, padx=5)

        self.var_termo = tk.BooleanVar()
        ttk.Checkbutton(form, text="Aceita o termo de responsabilidade",
                         variable=self.var_termo).grid(row=1, column=0, columnspan=2, sticky="w")

        ttk.Label(form, text="Produto:").grid(row=2, column=0, sticky="w", pady=2)
        self.combo_produto = ttk.Combobox(form, width=30, state="readonly")
        self.combo_produto.grid(row=2, column=1, pady=2, padx=5)

        ttk.Label(form, text="Quantidade:").grid(row=3, column=0, sticky="w", pady=2)
        self.entrada_quantidade = ttk.Entry(form, width=10)
        self.entrada_quantidade.grid(row=3, column=1, sticky="w", pady=2, padx=5)

        botoes = ttk.Frame(self)
        botoes.pack(pady=5)
        ttk.Button(botoes, text="Atualizar listas", command=self.atualizar_combos).pack(side="left", padx=5)
        ttk.Button(botoes, text="Adicionar item", command=self.adicionar_item).pack(side="left", padx=5)
        ttk.Button(botoes, text="Finalizar Pedido", command=self.finalizar_pedido).pack(side="left", padx=5)

        ttk.Label(self, text="Itens do pedido atual:").pack(anchor="w", padx=10)
        self.lista_itens = tk.Listbox(self, height=6)
        self.lista_itens.pack(fill="x", padx=10, pady=5)

        ttk.Label(self, text="Pedidos finalizados:").pack(anchor="w", padx=10)
        self.lista_pedidos = tk.Listbox(self)
        self.lista_pedidos.pack(fill="both", expand=True, padx=10, pady=5)
        self.lista_pedidos.bind("<Double-Button-1>", self.abrir_detalhes)

    def atualizar_combos(self):
        self.combo_cidadao["values"] = [f"{c.id_usuario} - {c.nome}" for c in cidadaos]
        self.combo_produto["values"] = [f"{p.id_produto} - {p.nome} (R${p.preco:.2f})" for p in produtos]

    def adicionar_item(self):
        if not self.combo_produto.get():
            messagebox.showwarning("Atencao", "Selecione um produto (clique em 'Atualizar listas').")
            return

        id_produto = int(self.combo_produto.get().split(" - ")[0])
        produto = next((p for p in produtos if p.id_produto == id_produto), None)

        try:
            quantidade = int(self.entrada_quantidade.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade invalida.")
            return

        item = ItemPedido(produto, quantidade, produto.preco)
        self.itens_pedido.append(item)

        self.entrada_quantidade.delete(0, tk.END)
        self.lista_itens.insert(tk.END, f"{produto.nome} x{quantidade} - Subtotal: R${item.subtotal:.2f}")

    def finalizar_pedido(self):
        if not self.combo_cidadao.get():
            messagebox.showwarning("Atencao", "Selecione um cidadao.")
            return
        if not self.var_termo.get():
            messagebox.showwarning("Atencao", "E necessario aceitar o termo de responsabilidade.")
            return
        if not self.itens_pedido:
            messagebox.showwarning("Atencao", "Adicione ao menos um item ao pedido.")
            return

        id_cidadao = int(self.combo_cidadao.get().split(" - ")[0])
        cidadao = next((c for c in cidadaos if c.id_usuario == id_cidadao), None)

        pedido = Pedido(gerar_id(), date.today(), "Pendente", True, cidadao)
        for item in self.itens_pedido:
            pedido.adicionar_item(item)
        pedidos.append(pedido)
        salvar_pedido(pedido)

        self.atualizar_lista_pedidos()
        messagebox.showinfo("Sucesso", f"Pedido criado! Total: R${pedido.valor_total:.2f}")

        self.itens_pedido = []
        self.lista_itens.delete(0, tk.END)
        self.var_termo.set(False)

    def atualizar_lista_pedidos(self):
        self.lista_pedidos.delete(0, tk.END)
        for p in pedidos:
            self.lista_pedidos.insert(tk.END, f"{p.id_pedido} - {p} - Cidadao: {p.cidadao.nome}")

    def abrir_detalhes(self, event=None):
        selecionado = self.lista_pedidos.curselection()
        if not selecionado:
            return
        pedido = pedidos[selecionado[0]]

        janela = tk.Toplevel(self)
        janela.title(f"Pedido #{pedido.id_pedido}")
        janela.geometry("400x420")

        ttk.Label(janela, text=f"Cidadao: {pedido.cidadao.nome}").pack(anchor="w", padx=10, pady=4)
        ttk.Label(janela, text=f"Data: {pedido.data_pedido.strftime('%d/%m/%Y')}").pack(anchor="w", padx=10)

        ttk.Label(janela, text="Itens do pedido:").pack(anchor="w", padx=10, pady=(12, 0))
        lista_itens = tk.Listbox(janela, height=6)
        for item in pedido.itens:
            lista_itens.insert(tk.END, f"{item.produto.nome} x{item.quantidade} - R${item.subtotal:.2f}")
        lista_itens.pack(fill="x", padx=10, pady=4)

        ttk.Label(janela, text=f"Total: R${pedido.valor_total:.2f}").pack(anchor="w", padx=10, pady=4)

        ttk.Label(janela, text="Status do pedido:").pack(anchor="w", padx=10, pady=(12, 0))
        combo_status = ttk.Combobox(
            janela, state="readonly",
            values=["Pendente", "Confirmado", "Entregue", "Cancelado"],
        )
        combo_status.set(pedido.status_pedido)
        combo_status.pack(padx=10, pady=4, anchor="w")

        def salvar_alteracoes():
            pedido.status_pedido = combo_status.get()
            regravar_pedidos()
            self.atualizar_lista_pedidos()
            messagebox.showinfo("Sucesso", "Pedido atualizado!")
            janela.destroy()

        ttk.Button(janela, text="Salvar alteracoes", command=salvar_alteracoes).pack(pady=15)


if __name__ == "__main__":
    carregar_dados()
    app = App()
    app.mainloop()
