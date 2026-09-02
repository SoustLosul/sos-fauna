from datetime import date, datetime

from model.cidadao import Cidadao
from model.agente_resgate import AgenteResgate
from model.equipe_resgate import EquipeResgate
from model.especie import Especie
from model.material_educativo import MaterialEducativo
from model.solicitacao_resgate import SolicitacaoResgate
from model.produto import Produto
from model.item_pedido import ItemPedido
from model.pedido import Pedido


# "Banco de dados" em memória, só para o menu funcionar
cidadaos = []
agentes = []
equipes = []
especies = []
materiais = []
solicitacoes = []
produtos = []
pedidos = []

proximo_id = 1


def gerar_id():
    global proximo_id
    id_atual = proximo_id
    proximo_id += 1
    return id_atual


def cadastrar_cidadao():
    print("\n--- Cadastro de Cidadao ---")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    rua = input("Rua: ")
    numero = input("Numero: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    cep = input("CEP: ")

    cidadao = Cidadao(gerar_id(), nome, email, senha, date.today(),
                       rua, numero, bairro, cidade, cep)
    cidadaos.append(cidadao)
    print(f"Cidadao cadastrado com sucesso! ID: {cidadao.id_usuario}")


def cadastrar_agente():
    print("\n--- Cadastro de Agente de Resgate ---")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    matricula = input("Matricula: ")
    cargo = input("Cargo: ")

    agente = AgenteResgate(gerar_id(), nome, email, senha, date.today(), matricula, cargo)
    agentes.append(agente)
    print(f"Agente cadastrado com sucesso! ID: {agente.id_usuario}")


def cadastrar_equipe():
    print("\n--- Cadastro de Equipe de Resgate ---")
    nome_equipe = input("Nome da equipe: ")
    area_atuacao = input("Area de atuacao: ")

    equipe = EquipeResgate(gerar_id(), nome_equipe, area_atuacao)
    equipes.append(equipe)
    print(f"Equipe cadastrada com sucesso! ID: {equipe.id_equipe}")


def cadastrar_especie():
    print("\n--- Cadastro de Especie ---")
    nome_popular = input("Nome popular: ")
    nome_cientifico = input("Nome cientifico: ")
    nivel_risco = input("Nivel de risco: ")
    orientacoes = input("Orientacoes de captura: ")

    especie = Especie(gerar_id(), nome_popular, nome_cientifico, nivel_risco, orientacoes)
    especies.append(especie)
    print(f"Especie cadastrada com sucesso! ID: {especie.id_especie}")


def cadastrar_produto():
    print("\n--- Cadastro de Produto ---")
    nome = input("Nome: ")
    descricao = input("Descricao: ")
    preco = float(input("Preco: "))
    categoria = input("Categoria: ")

    produto = Produto(gerar_id(), nome, descricao, preco, categoria)
    produtos.append(produto)
    print(f"Produto cadastrado com sucesso! ID: {produto.id_produto}")


def abrir_solicitacao():
    print("\n--- Abrir Solicitacao de Resgate ---")
    if not cidadaos:
        print("Cadastre um cidadao antes de abrir uma solicitacao.")
        return

    listar_cidadaos()
    id_cidadao = int(input("ID do cidadao solicitante: "))
    cidadao = next((c for c in cidadaos if c.id_usuario == id_cidadao), None)
    if not cidadao:
        print("Cidadao nao encontrado.")
        return

    descricao = input("Descricao da ocorrencia: ")

    solicitacao = SolicitacaoResgate(gerar_id(), datetime.now(), descricao,
                                      "Aberta", cidadao)
    solicitacoes.append(solicitacao)
    print(f"Solicitacao aberta com sucesso! ID: {solicitacao.id_solicitacao}")


def fazer_pedido():
    print("\n--- Fazer Pedido de Equipamentos ---")
    if not cidadaos or not produtos:
        print("Cadastre um cidadao e ao menos um produto antes de fazer um pedido.")
        return

    listar_cidadaos()
    id_cidadao = int(input("ID do cidadao: "))
    cidadao = next((c for c in cidadaos if c.id_usuario == id_cidadao), None)
    if not cidadao:
        print("Cidadao nao encontrado.")
        return

    aceite = input("Aceita o termo de responsabilidade? (s/n): ").lower() == "s"
    if not aceite:
        print("E necessario aceitar o termo para prosseguir.")
        return

    pedido = Pedido(gerar_id(), date.today(), "Pendente", aceite, cidadao)

    while True:
        listar_produtos()
        id_produto = int(input("ID do produto (0 para finalizar): "))
        if id_produto == 0:
            break
        produto = next((p for p in produtos if p.id_produto == id_produto), None)
        if not produto:
            print("Produto nao encontrado.")
            continue
        quantidade = int(input("Quantidade: "))
        pedido.adicionar_item(ItemPedido(produto, quantidade, produto.preco))

    pedidos.append(pedido)
    print(f"Pedido criado com sucesso! ID: {pedido.id_pedido} | Total: R${pedido.valor_total:.2f}")


def listar_cidadaos():
    print("\n--- Cidadaos ---")
    for c in cidadaos:
        print(f"{c.id_usuario} - {c}")


def listar_agentes():
    print("\n--- Agentes de Resgate ---")
    for a in agentes:
        print(f"{a.id_usuario} - {a}")


def listar_equipes():
    print("\n--- Equipes de Resgate ---")
    for e in equipes:
        print(f"{e.id_equipe} - {e}")


def listar_especies():
    print("\n--- Especies ---")
    for e in especies:
        print(f"{e.id_especie} - {e}")


def listar_produtos():
    print("\n--- Produtos ---")
    for p in produtos:
        print(f"{p.id_produto} - {p}")


def listar_solicitacoes():
    print("\n--- Solicitacoes de Resgate ---")
    for s in solicitacoes:
        print(f"{s.id_solicitacao} - {s} - Cidadao: {s.cidadao.nome}")


def listar_pedidos():
    print("\n--- Pedidos ---")
    for p in pedidos:
        print(f"{p.id_pedido} - {p} - Cidadao: {p.cidadao.nome}")


def menu_cadastros():
    while True:
        print("\n===== CADASTROS =====")
        print("1 - Cadastrar Cidadao")
        print("2 - Cadastrar Agente de Resgate")
        print("3 - Cadastrar Equipe de Resgate")
        print("4 - Cadastrar Especie")
        print("5 - Cadastrar Produto")
        print("0 - Voltar")
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            cadastrar_cidadao()
        elif opcao == "2":
            cadastrar_agente()
        elif opcao == "3":
            cadastrar_equipe()
        elif opcao == "4":
            cadastrar_especie()
        elif opcao == "5":
            cadastrar_produto()
        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


def menu_listagens():
    while True:
        print("\n===== LISTAGENS =====")
        print("1 - Listar Cidadaos")
        print("2 - Listar Agentes de Resgate")
        print("3 - Listar Equipes de Resgate")
        print("4 - Listar Especies")
        print("5 - Listar Produtos")
        print("6 - Listar Solicitacoes de Resgate")
        print("7 - Listar Pedidos")
        print("0 - Voltar")
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            listar_cidadaos()
        elif opcao == "2":
            listar_agentes()
        elif opcao == "3":
            listar_equipes()
        elif opcao == "4":
            listar_especies()
        elif opcao == "5":
            listar_produtos()
        elif opcao == "6":
            listar_solicitacoes()
        elif opcao == "7":
            listar_pedidos()
        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


def menu_principal():
    while True:
        print("\n===== SOS FAUNA URBANA =====")
        print("1 - Cadastros")
        print("2 - Abrir Solicitacao de Resgate")
        print("3 - Fazer Pedido de Equipamentos")
        print("4 - Listagens")
        print("0 - Sair")
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            menu_cadastros()
        elif opcao == "2":
            abrir_solicitacao()
        elif opcao == "3":
            fazer_pedido()
        elif opcao == "4":
            menu_listagens()
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    menu_principal()
