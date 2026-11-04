# Documento de Visão — SOS Fauna Urbana

## 1. Nome do sistema
**SOS Fauna Urbana**

## 2. Descrição do problema
Em áreas urbanas, é comum que moradores encontrem animais silvestres ou feridos (gambás, cobras, aves, saguis etc.)
dentro de casa, em quintais ou nas ruas. Hoje não há um canal simples para pedir ajuda informando qual é o animal e onde
ele está, e as pessoas acabam tentando remover o bicho por conta própria, sem orientação e sem equipamento, o que coloca
em risco tanto o animal quanto a pessoa.

## 3. Justificativa
Centralizar os pedidos de resgate melhora a organização do atendimento (quem pediu, onde, qual animal, qual equipe atende)
e reduz acidentes. Para os casos em que o próprio cidadão pode agir com segurança, o sistema também oferece **produtos de
apoio** (luvas, redes, caixas de transporte) e **orientações de captura** por espécie.

## 4. Objetivo geral
Melhorar o resgate de animais em regiões urbanas, permitindo que cidadãos solicitem resgates, que equipes e agentes sejam
organizados para o atendimento e que produtos de remoção segura possam ser pedidos.

## 5. Público-alvo
- **Cidadãos** que encontram um animal e precisam de ajuda ou de equipamento.
- **Agentes de resgate** e **equipes** (órgãos ambientais, ONGs, bombeiros) que atendem as ocorrências.

## 6. Funcionalidades
1. Cadastrar e editar **cidadãos** (nome, email, senha e endereço).
2. Cadastrar e editar **agentes de resgate** (nome, matrícula, email, senha, cargo).
3. Cadastrar **equipes** com nome e área de atuação.
4. Cadastrar **espécies** (nome popular, nome científico, nível de risco, orientações de captura).
5. Cadastrar **produtos** (nome, descrição, preço, categoria).
6. Abrir **solicitações de resgate** vinculadas a um cidadão, com descrição e status.
7. Fazer **pedidos** de produtos: aceitar o termo, escolher produto e quantidade, adicionar itens e finalizar.
8. **Salvar e recuperar** todos os dados entre execuções (arquivos `.txt` na pasta `dados/`).

## 7. Escopo
**Dentro do escopo (versão 1):** cadastros, abertura de solicitações, pedidos de produtos, persistência em arquivos,
interface gráfica (Tkinter) e versão de terminal.

**Fora do escopo (por enquanto):** pagamento real, geolocalização/mapa, autenticação com login, envio de notificações,
atribuição automática de equipe à solicitação.

## 8. Regras de negócio
| Código | Regra | Onde é aplicada |
|---|---|---|
| RN01 | Cidadão não pode ser cadastrado sem **nome** e **email**. | `Usuario` / `Cidadao` (setters) |
| RN02 | Agente não pode ser cadastrado sem **nome** e **matrícula**. | `Usuario` / `AgenteResgate` |
| RN03 | Equipe precisa de **nome**. | `EquipeResgate` |
| RN04 | Espécie precisa de **nome popular**. | `Especie` |
| RN05 | Produto precisa de **nome** e o **preço não pode ser negativo**. | `Produto` |
| RN06 | A **quantidade** de um item deve ser maior que zero. | `ItemPedido` |
| RN07 | O pedido só é criado se o cidadão **aceitar o termo de responsabilidade**. | `Pedido` |
| RN08 | O pedido precisa de um **cidadão** e de **pelo menos um item** para ser finalizado. | Interface (`AbaPedido`) / console |
| RN09 | Só é possível **adicionar itens a pedidos "Pendente"**. | decorador `@requer_status_pedido` |
| RN10 | O **status** só pode ser um dos valores válidos (pedido: Pendente, Confirmado, Entregue, Cancelado; solicitação: Aberta, Em atendimento, Concluida, Cancelada). | `Pedido`, `SolicitacaoResgate` |
| RN11 | Para abrir uma solicitação é preciso **selecionar um cidadão** e informar a **descrição**. | Interface (`AbaSolicitacao`) |
| RN12 | **Email de cidadão** e **matrícula de agente** devem ser **únicos**. | `repositorio.garantir_*` |
| RN13 | **IDs** são gerados automaticamente e **não podem ser alterados**. | `gerar_id()` e propriedades somente leitura |
| RN14 | Linhas corrompidas nos arquivos de dados são **ignoradas com aviso**, sem derrubar o programa. | `repositorio._carregar` |

## 9. Persistência de dados — escolha
Foi escolhida a **Opção A (arquivos)**, com arquivos `.txt` (campos separados por `|`) na pasta `dados/`.
Motivos: não exige instalar nada, os dados ficam legíveis para conferência e o volume do projeto é pequeno.
Todo o acesso aos arquivos fica na camada `repository/`, então trocar por JSON ou banco de dados não exige alterar
as classes do modelo.

## 10. Tecnologias
Python 3.10+, Tkinter (interface), `unittest` (testes). Nenhuma biblioteca externa.
