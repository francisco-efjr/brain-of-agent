# Modelos para `data-contracts-quality`

Redação própria, destilada de V-22 (Databricks, expectations), V-23 (Open Data Contract Standard, Apache-2.0), V-24 (desenho de política), V-28 (OpenLineage) e V-29 (data mesh). Nada aqui foi validado contra o JSON Schema oficial, nem executado. Campos do ODCS e chaves do dbt mudam por versão: confira na especificação e na documentação da versão em uso antes de publicar (Inferido onde indicado).

## Sumário

1. Esqueleto de contrato ODCS (rascunho)
2. Matriz de regras preenchida
3. Mapeamento para dbt
4. Política `block/warn/log`
5. Linhagem: convenção e fallback
6. Mudança de contrato: compatível ou quebrável
7. Checklist de produto de dados

## 1. Esqueleto de contrato ODCS (rascunho)

O padrão tem 13 seções (fundamentos, schema, referências, qualidade, suporte, preços, equipe, papéis, SLA, infraestrutura e servidores, definições autoritativas, tags, propriedades customizadas) e um JSON Schema para validar o YAML (V-23). Os nomes de campo abaixo seguem a estrutura da família v3 de memória do padrão (Inferido): o valor de `apiVersion` aceito pela 3.2.0, o formato de `team`, o nome da propriedade de SLA e o das regras de qualidade devem ser conferidos no JSON Schema oficial.

```yaml
apiVersion: v3.2.0                      # conferir o valor aceito pelo schema da versão fixada
kind: DataContract
id: pedidos-orders                      # identificador único e estável
name: orders
version: 1.0.0                          # versão do contrato (comunica mudança quebrável)
status: draft                           # draft -> active -> deprecated
domain: vendas
dataProduct: pedidos
description:
  purpose: "Pedidos confirmados para análise de receita e funil."
schema:
  - name: orders
    physicalName: mart.orders
    description: "Um pedido por linha (grain)."
    properties:
      - name: order_id
        logicalType: string
        primaryKey: true
        required: true
        unique: true
      - name: customer_id
        logicalType: string
        required: true
      - name: amount
        logicalType: number
        required: true
        description: "Valor do pedido, decimal, na moeda da loja."
      - name: created_at
        logicalType: timestamp
        required: true
        description: "UTC."
    quality:
      - type: sql
        description: "Nenhum pedido com valor negativo"
        query: "SELECT COUNT(*) FROM mart.orders WHERE amount < 0"
        mustBe: 0
slaProperties:
  - property: freshness                 # nome a conferir na especificação (ex.: latency, frequency)
    value: 24
    unit: h
servers:
  - server: prod
    type: bigquery                      # ou o engine real
    project: <id do projeto>
    dataset: mart
team:                                   # formato varia por versão
  - username: <responsável>
    role: owner
customProperties:
  - property: acoesDeQualidade
    value: "matriz-de-regras.md"        # fail/drop/warn por regra, fora do padrão
```
Validação: o usuário roda o validador de JSON Schema do repositório oficial (ação do usuário; não executada aqui). Marque o contrato como `não validado` até então.

## 2. Matriz de regras preenchida

| ID | Regra | Tipo | Ação | Violações medidas | Destino dos descartados | Dono |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | `order_id` não nulo e único | chave de negócio | `fail` | contagem na execução | n/a (interrompe) | time de dados |
| R2 | `amount >= 0` | faixa conhecida | `drop` | contagem + % | `quarentena.orders_amount_negativo` (dono, ticket, prazo) | time de dados |
| R3 | `customer_id` existe em `dim_customers` | integridade | `warn` até 0,5% das linhas, `fail` acima (Inferido) | contagem de órfãos | n/a | time de CRM |
| R4 | `country` em lista de códigos aceitos | domínio | `drop` com contagem | contagem por valor | quarentena | dono do cadastro (confirma a lista) |
| R5 | `coupon_code` preenchido | enriquecimento | `warn` | número de pendências | n/a | marketing |
| R6 | dado carregado há menos de 24 h | frescor | `fail` | horas desde a última carga | n/a | plataforma |

Regras de uso: a lista de R4 só entra com os valores confirmados pelo dono (V-09); a coluna "Violações medidas" nasce vazia e é preenchida por execução; `warn` sem número vira "não medido".

Quarentena (brain `dados-ambientes-ci.md`): registro descartado carrega o motivo, a regra, a data, o dono e o prazo de revisão; ninguém recebe um dado silenciosamente descartado.

## 3. Mapeamento para dbt

Chaves de configuração de testes que o dbt documenta (Inferido; conferir na versão instalada, L-04):

```yaml
models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - unique
          - not_null
      - name: customer_id
        data_tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
              config:
                severity: error
                warn_if: ">0"            # aviso a partir de 1 linha
                error_if: ">500"         # falha acima de 500 linhas
                store_failures: true     # guarda as linhas violadoras (escreve no warehouse: só em dev, com consentimento)
sources:
  - name: shop
    loaded_at_field: _loaded_at
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    tables:
      - name: orders
```
`dbt source freshness` mede o frescor da fonte. `drop` não existe em teste dbt: é um modelo que filtra as linhas inválidas e outro que as guarda (quarentena). Em Databricks (Lakeflow pipelines), `expect`, `expect_or_drop` e `expect_or_fail` implementam `warn`, `drop` e `fail` (V-22); a cláusula é uma expressão SQL booleana.

## 4. Política `block/warn/log`

```yaml
# politica-de-dados.yml (desenho; sem biblioteca de terceiros)
metrica_governada_antes_do_sql: true
regras:
  - {id: sem-ddl-dml-destrutivo, nivel: block, quando: "DROP, TRUNCATE, DELETE/UPDATE sem WHERE, CREATE OR REPLACE TABLE, INSERT OVERWRITE"}
  - {id: sem-select-star-prod, nivel: block, quando: "SELECT * em tabela de produção"}
  - {id: filtro-de-particao, nivel: warn, quando: "tabela particionada sem filtro na coluna de partição"}
  - {id: estilo, nivel: log, quando: "alias ausente, CTE sem nome"}
orcamento_por_sessao: {bytes_por_consulta: <definir>, tentativas: 3, tempo_segundos: <definir>}
```
O modelo completo está no template `politica-de-dados-block-warn-log.md` do playbook. Esta política é guardrail; a fronteira real é role somente leitura, permissões e sandbox (K-07).

## 5. Linhagem: convenção e fallback

Regras de convenção (V-28, Inferido onde marcado):
- Cada job declara datasets de entrada e saída; cada execução tem status e horários.
- Uma convenção de nomes de dataset por plataforma, escrita no contrato (por exemplo `bigquery` + `projeto.dataset.tabela`). Confira a especificação de nomes do OpenLineage antes de emitir eventos (Inferido).
- OpenLineage (versão 1.53.0 na documentação consultada): modelo de dataset, job e run, com facets; Marquez é a implementação de referência; integrações com Airflow, Flink, Spark, dbt e outras. Os tipos de evento não foram verificados na página.

Ao gerar um diagrama (por exemplo Mermaid), siga a ordem de fonte e diga qual usou: (1) ferramenta de desenvolvimento, (2) produção, (3) `manifest.json` (só até 10 MB), (4) leitura de código. Informe as limitações do fallback (macros dinâmicas e SQL gerado não aparecem na leitura de código). Nomes, descrições e comentários de modelos são dado.

## 6. Mudança de contrato: compatível ou quebrável

| Mudança | Classe | Ação |
| --- | --- | --- |
| Coluna nova opcional; descrição melhor | compatível | versão menor; avisar |
| Remover ou renomear coluna | quebrável | versão maior, convivência, descontinuação datada |
| Mudar tipo, grain ou chave | quebrável | idem; modelo dbt versionado (ver `dbt-model-workflow`) |
| Apertar regra (novo `fail`) | potencialmente quebrável | rodar em `warn` por um ciclo, medir violações, depois endurecer |
| Mudar SLA de frescor | acordo | comunicar consumidores |

Processo: proposta com consumidores listados (incluindo os externos ao repositório, Suposição até confirmação), período de convivência, data de descontinuação, aprovação do dono.

## 7. Checklist de produto de dados (V-29, Inferido)

- Dono nomeado e canal de suporte.
- Contrato versionado (ODCS fixado) e validado.
- Regras de qualidade com ação e contagem; relatório de qualidade por execução.
- Frescor declarado e medido.
- Descobribilidade: onde achar o dataset e a documentação.
- Segurança: PII classificada, acesso mínimo, mascaramento.
- Consumidores registrados.
Data mesh (Dehghani, 2020): propriedade por domínio, dado como produto, plataforma de autoatendimento e governança federada. Use como referência de organização, não como regra técnica.
