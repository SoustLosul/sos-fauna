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

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Cidadao cadastrado! ID: {cidadao.id_usuario}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for c in cidadaos:
            self.lista.insert(tk.END, f"{c.id_usuario} - {c}")


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

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Agente cadastrado! ID: {agente.id_usuario}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for a in agentes:
            self.lista.insert(tk.END, f"{a.id_usuario} - {a}")


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

    def cadastrar(self):
        nome_equipe = self.entradas["Nome da equipe"].get()
        area_atuacao = self.entradas["Area de atuacao"].get()

        if not nome_equipe:
            messagebox.showwarning("Atencao", "Preencha o nome da equipe.")
            return

        equipe = EquipeResgate(gerar_id(), nome_equipe, area_atuacao)
        equipes.append(equipe)

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Equipe cadastrada! ID: {equipe.id_equipe}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for e in equipes:
            self.lista.insert(tk.END, f"{e.id_equipe} - {e}")


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

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Especie cadastrada! ID: {especie.id_especie}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for e in especies:
            self.lista.insert(tk.END, f"{e.id_especie} - {e}")


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

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Produto cadastrado! ID: {produto.id_produto}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for p in produtos:
            self.lista.insert(tk.END, f"{p.id_produto} - {p}")


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

        self.entrada_descricao.delete(0, tk.END)
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Solicitacao aberta! ID: {solicitacao.id_solicitacao}")

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for s in solicitacoes:
            self.lista.insert(tk.END, f"{s.id_solicitacao} - {s} - Cidadao: {s.cidadao.nome}")


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

        self.lista_pedidos.insert(tk.END, f"{pedido.id_pedido} - {pedido} - Cidadao: {cidadao.nome}")
        messagebox.showinfo("Sucesso", f"Pedido criado! Total: R${pedido.valor_total:.2f}")

        self.itens_pedido = []
        self.lista_itens.delete(0, tk.END)
        self.var_termo.set(False)


if __name__ == "__main__":
    app = App()
    app.mainloop()
