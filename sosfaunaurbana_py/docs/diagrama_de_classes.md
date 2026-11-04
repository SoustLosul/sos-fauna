# Diagrama de Classes UML

O diagrama abaixo está em Mermaid e **aparece desenhado automaticamente no GitHub**.

Legenda de visibilidade: `+` público, `#` protegido (`_atributo`), `-` privado (`__atributo`).

```mermaid
classDiagram
    class Usuario {
        #int _id_usuario
        #date _data_cadastro
        #str _nome
        #str _email
        -str __senha
        +str telefone
        +id_usuario() int
        +nome() str
        +email() str
        +senha() str
        +verificar_senha(str tentativa) bool
        +descrever() str
    }
    class Cidadao {
        +str rua
        +str numero
        +str bairro
        +str cidade
        +str cep
        +endereco() str
        +descrever() str
    }
    class AgenteResgate {
        #str _matricula
        +str cargo
        +EquipeResgate equipe
        +matricula() str
        +descrever() str
    }
    class EquipeResgate {
        #int _id_equipe
        #str _nome_equipe
        +str area_atuacao
        -list _agentes
        +agentes() tuple
        +adicionar_agente(AgenteResgate agente)
    }
    class Especie {
        #int _id_especie
        #str _nome_popular
        +str nome_cientifico
        +str nivel_risco
        +str orientacoes_captura
        -list _materiais
        +materiais() tuple
        +adicionar_material(MaterialEducativo material)
    }
    class MaterialEducativo {
        #int _id_material
        #str _titulo
        +str conteudo
        +str tipo_midia
    }
    class SolicitacaoResgate {
        #int _id_solicitacao
        #datetime _data_hora
        #str _status
        +str descricao
        +str rua
        +str bairro
        +str cidade
        +str cep
        +str referencia
        +status() str
    }
    class Produto {
        #int _id_produto
        #str _nome
        #float _preco
        +str descricao
        +str categoria
        +__mul__(int quantidade) ItemPedido
    }
    class ItemPedido {
        #Produto _produto
        #int _quantidade
        #float _preco_unitario
        +subtotal() float
        +__add__(ItemPedido outro) ItemPedido
    }
    class Pedido {
        #int _id_pedido
        #date _data_pedido
        #str _status_pedido
        #bool _aceite_termo_resp
        -list _itens
        +itens() tuple
        +valor_total() float
        +adicionar_item(ItemPedido item)
        +__iadd__(ItemPedido item) Pedido
        +__len__() int
    }

    Usuario <|-- Cidadao : herança
    Usuario <|-- AgenteResgate : herança
    EquipeResgate "0..1" o-- "0..*" AgenteResgate : pertence a
    Cidadao "1" --> "0..*" SolicitacaoResgate : realiza
    SolicitacaoResgate "0..*" --> "0..1" EquipeResgate : atendida por
    SolicitacaoResgate "0..*" --> "0..1" Especie : envolve
    Especie "1" o-- "0..*" MaterialEducativo : aborda
    Cidadao "1" --> "0..*" Pedido : faz
    Pedido "1" *-- "1..*" ItemPedido : contém
    ItemPedido "0..*" --> "1" Produto : refere-se a
```

## Observações
- **Herança:** `Cidadao` e `AgenteResgate` especializam `Usuario`.
- **Agregação** (losango vazado): uma equipe agrega agentes, que existem independentemente dela.
- **Composição** (losango cheio): os itens só existem dentro de um pedido.
- As multiplicidades seguem os comentários do código (`# realiza (1,1)`, `# atende (0,1)` etc.).
- A multiplicidade entre `Especie` e `MaterialEducativo` é uma suposição (o código só guarda a lista dentro da espécie).
