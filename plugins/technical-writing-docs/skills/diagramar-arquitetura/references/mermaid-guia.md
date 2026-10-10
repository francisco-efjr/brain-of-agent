# Guia de Mermaid e C4 para documentação

Conteúdo: 1 necessidade → tipo · 2 esqueletos · 3 C4 em níveis · 4 teste de renderização · 5 exemplo completo com fallback · 6 versões e fontes.

Fontes: documentação do Mermaid (https://mermaid.js.org/intro/ e /syntax/c4.html), documentação do GitHub sobre diagramas, modelo C4 de Simon Brown (CC BY 4.0), skill `c4-architecture` do softaworks/agent-toolkit (MIT) como inspiração de níveis, regra de menos de 15 nós do exemplo de output style da Anthropic. Itens V-21, V-22, V-44, V-08. Rótulo: Verificado nas fontes citadas; os esqueletos abaixo são redação própria **não renderizada** na construção (sem Mermaid disponível); sintaxe de macros C4 conferida contra a documentação lida (macros `Person`, `System`, `System_Ext`, `Container`, `Component`, `Boundary`, `Rel`) e, para `ContainerDb`, `ContainerQueue` e `System_Boundary`, Inferida do conhecimento estável do Mermaid. Confirme em /syntax/c4.html.

## 1. Necessidade → tipo

| Necessidade | Tipo Mermaid | Observação |
| --- | --- | --- |
| Decisão, processo, dependências | `flowchart TD` ou `LR` | O mais portátil; use como fallback |
| Interação entre partes no tempo | `sequenceDiagram` | Um cenário por diagrama |
| Ciclo de vida de uma entidade | `stateDiagram-v2` | Estados e eventos |
| Cronograma | `gantt` | Datas ISO |
| Modelo de tipos | `classDiagram` | Só relações relevantes |
| Modelo de dados | `erDiagram` | **Experimental**; modelagem é de `database-data-modeling` |
| Contexto do sistema | `C4Context` | **Experimental** |
| Contêineres | `C4Container` | **Experimental** |
| Componentes | `C4Component` | **Experimental**, só quando agrega |

Limite: menos de 15 nós por diagrama (preferência do plugin; Suposição de que vale em geral).

## 2. Esqueletos

Fluxo:

```mermaid
flowchart LR
  cliente([Cliente]) --> web[Web app]
  web -->|HTTPS/JSON| api[API]
  api -->|SQL| db[(Banco)]
  api -->|publica job| fila[[Fila]]
```

Sequência:

```mermaid
sequenceDiagram
  actor Cliente
  participant Web
  participant API
  participant DB as Banco
  Cliente->>Web: Finaliza compra
  Web->>API: POST /pedidos
  API->>DB: grava pedido
  DB-->>API: ok
  API-->>Web: 201 Created
  Web-->>Cliente: Confirmação
```

Estados:

```mermaid
stateDiagram-v2
  [*] --> aguardando_pagamento
  aguardando_pagamento --> pago: pagamento confirmado
  aguardando_pagamento --> cancelado: prazo expirou
  pago --> [*]
  cancelado --> [*]
```

Regras: `flowchart` formas `[ ]` retângulo, `([ ])` estádio, `[( )]` cilindro (banco), `[[ ]]` sub-rotina (fila); rótulo de aresta `-->|texto|`. Aliases sem espaço. Aspas em rótulos com caracteres especiais (parênteses, dois-pontos).

## 3. C4 em níveis

Níveis (V-21): contexto · contêineres · componentes · código; complementares: dinâmico e implantação. Notação e ferramenta são independentes: escolha uma e mantenha. Palavras-chave do Mermaid: `C4Context`, `C4Container`, `C4Component`, `C4Dynamic`, `C4Deployment`.

Contexto:

```mermaid
C4Context
  title Contexto da Loja online
  Person(cliente, "Cliente", "Compra pelo site")
  System(loja, "Loja online", "Catálogo, carrinho e pedidos")
  System_Ext(pagamento, "Gateway de pagamento", "Processa cartões")
  Rel(cliente, loja, "Usa", "HTTPS")
  Rel(loja, pagamento, "Cobra", "HTTPS/JSON")
```

Contêineres:

```mermaid
C4Container
  title Contêineres da Loja online
  Person(cliente, "Cliente")
  System_Boundary(loja, "Loja online") {
    Container(web, "Web app", "React", "Interface do cliente")
    Container(api, "API", "Node.js", "Regras de negócio")
    ContainerDb(db, "Banco", "PostgreSQL", "Pedidos e clientes")
    ContainerQueue(fila, "Fila", "Redis", "Jobs assíncronos")
  }
  Rel(cliente, web, "Usa", "HTTPS")
  Rel(web, api, "Chama", "HTTPS/JSON")
  Rel(api, db, "Lê e grava", "SQL")
  Rel(api, fila, "Publica jobs")
```

Regras: um nível por figura; cada `Rel` com tecnologia ou intenção; pessoas e sistemas externos só no contexto e no que interage com o nível atual.

## 4. Teste de renderização

| Destino | Como testar | Resultado a registrar |
| --- | --- | --- |
| GitHub | Preview do arquivo (ou PR de teste); bloco com apenas `info` mostra a versão do Mermaid | "Verificado pelo usuário no GitHub, Mermaid <versão>, em <data>" |
| MkDocs, Docusaurus | Confirme o plugin de Mermaid no config e abra o preview local | idem, com o destino |
| Outro | Peça ao usuário o preview | "render não verificado" se não houver |

Bloco de versão (GitHub):

````markdown
```mermaid
info
```
````

C4 renderizado no GitHub: **Não verificado** (a página do GitHub lista fluxogramas, sequência e pizza "e mais", sem citar C4). Se falhar, use o fallback.

## 5. Exemplo completo (pedido: C4 de contêineres para o README do GitHub)

Arquivo `docs/architecture/containers-loja.md` (dados fictícios; no uso real, cada contêiner vem de arquivo lido):

````markdown
# Contêineres da Loja online

Público: desenvolvedores da equipe · Nível: contêineres (C4) · Data: 2026-10-10
Render: não verificado no GitHub (C4 do Mermaid é experimental; Mermaid <versão>)

**O que este diagrama mostra:** as quatro peças que a equipe opera e como falam entre si.
**O que não mostra:** pagamento externo, implantação e componentes internos da API.

(bloco C4Container da seção 3 aqui)

**Elementos Inferidos:** a fila Redis foi deduzida de `docker-compose.yml:14` (serviço `redis`)
e não há consumidor identificado no código lido.

## Alternativa (se o C4 não renderizar)

(bloco flowchart com os mesmos 5 elementos e as mesmas arestas)

Relacionados: `contexto-loja.md` (nível acima, quando existir)
````

Fallback com a mesma informação:

```mermaid
flowchart LR
  cliente([Cliente]) -->|HTTPS| web[Web app React]
  web -->|HTTPS/JSON| api[API Node.js]
  api -->|SQL| db[(PostgreSQL)]
  api -->|publica jobs| fila[[Fila Redis]]
```

Contagem: 5 nós, abaixo do limite de 15.

## 6. Versões e onde conferir

- Mermaid: releases em https://github.com/mermaid-js/mermaid/releases (a verificação deste plugin viu releases de 2026-10-02); sintaxe C4 em https://mermaid.js.org/syntax/c4.html.
- GitHub: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams.
- C4: https://c4model.com/.
