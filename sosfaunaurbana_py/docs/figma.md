# Protótipos no Figma

**Link de visualização:** `COLE_AQUI_O_LINK_DO_FIGMA`  <!-- TODO: trocar pelo link real (Share > Anyone with the link can view) -->

## Telas que precisam estar no protótipo
Cada tela deve ter os estados **sucesso**, **erro** e **validação** (campo obrigatório vazio).

| Tela | Estados a prototipar |
|---|---|
| Janela principal com abas | navegação entre as abas |
| Cadastro de cidadão | sucesso · erro "nome e email obrigatórios" · erro "email já cadastrado" |
| Cadastro de agente | sucesso · erro "nome e matrícula obrigatórios" · erro "matrícula já cadastrada" |
| Cadastro de equipe | sucesso · erro "nome obrigatório" |
| Cadastro de espécie | sucesso · erro "nome popular obrigatório" |
| Cadastro de produto | sucesso · erro "nome e preço obrigatórios" · erro "preço negativo" |
| Abrir solicitação de resgate | sucesso · erro "selecione um cidadão" |
| Pedido de produtos | termo de responsabilidade · item adicionado · erro "quantidade inválida" · pedido finalizado |
| Detalhes / edição (janela ao dar duplo clique) | salvar com sucesso · erro de validação |

## Fluxo principal
`Cadastrar cidadão → Cadastrar produto → Fazer pedido (aceitar termo → escolher produto e quantidade → finalizar)`
`Cadastrar cidadão → Abrir solicitação de resgate`
