# Contrato de dados (rascunho ODCS 3.2.0): [DATASET]

Uso: skill `data-contracts-quality`. Base: V-23 (Open Data Contract Standard, Bitol, v3.2.0, Apache-2.0), V-22.
Status: NÃO VALIDADO. O esqueleto abaixo segue a estrutura geral do padrão (13 seções: fundamentals, schema, references, data quality, support, pricing, team, roles, SLA, infrastructures e servers, authoritative definitions, tags, custom properties), mas os nomes exatos das chaves são Suposição até a validação contra o JSON Schema oficial do repositório `bitol-io/open-data-contract-standard` (ação do usuário). Não publique antes disso.
Campos que a equipe precisa decidir ficam como `[A DEFINIR PELA EQUIPE]`; o agente não preenche dono, SLA nem valores aceitos por palpite.

```yaml
# Fundamentals
apiVersion: v3.2.0            # Suposição: conferir o valor aceito pelo JSON Schema
kind: DataContract
id: [IDENTIFICADOR ÚNICO]
name: [NOME DO DATASET]
version: 0.1.0
status: draft
description:
  purpose: [PARA QUE O DATASET EXISTE]
  limitations: [O QUE ELE NÃO REPRESENTA]
  usage: [COMO CONSUMIR]

# Time e suporte
team:
  - username: [A DEFINIR PELA EQUIPE]
    role: owner
support:
  - channel: [CANAL]
    url: [A DEFINIR PELA EQUIPE]

# Schema (com chave)
schema:
  - name: [TABELA]
    physicalType: table
    description: [GRAIN: uma linha por ...]
    properties:
      - name: [COLUNA_CHAVE]
        logicalType: string
        primaryKey: true
        required: true
        unique: true
        description: [SIGNIFICADO]
      - name: [COLUNA_DE_VALOR]
        logicalType: number
        required: false
        description: [UNIDADE E REGRA]
      - name: [COLUNA_TIMESTAMP]
        logicalType: timestamp
        required: true
        description: [EVENTO; UTC]
    # Qualidade: cada regra tem ação e reporta contagem (ver seção "Regras" abaixo)
    quality:
      - description: [chave de negócio nunca nula nem duplicada]
        # Suposição: formato exato da regra (biblioteca ou SQL) a validar no JSON Schema
      - description: [valor dentro da faixa [MIN] a [MAX]]

# SLA
slaProperties:
  - property: freshness
    value: [A DEFINIR PELA EQUIPE]
    unit: [h|d]
    description: [DESDE O EVENTO ATÉ A DISPONIBILIDADE NA TABELA]

# Servidores
servers:
  - server: [NOME]
    type: [bigquery|snowflake|databricks|...]
    environment: [dev|prod]
    # [PROJETO/DATASET/SCHEMA conforme o tipo]

# Definições autoritativas, tags, propriedades customizadas
tags: [LISTA]
```

## Regras de qualidade e ação (V-22)
| Regra | Ação (`fail`, `drop`, `warn`) | Contagem reportada em | Destino do descartado |
| --- | --- | --- | --- |
| [REGRA] | [AÇÃO] | [ONDE] | [QUARENTENA OU N/A] |
Padrão: chave de negócio nula ou duplicada = `fail`; faixa conhecida = `drop` com contagem e quarentena; enriquecimento opcional = `warn` com número.

## Validação (ação do usuário)
1. Baixar o JSON Schema da versão 3.2.0 do repositório oficial e validar este YAML com um validador de sua confiança. O plugin não executa nem instala validador.
2. Registrar abaixo o resultado: [VALIDADO em DATA com FERRAMENTA/VERSÃO | NÃO VALIDADO].

## Pendências
- Dono: [A DEFINIR PELA EQUIPE]
- SLA de frescor: [A DEFINIR PELA EQUIPE]
- Valores aceitos de campos categóricos: confirmar com o dono do dado.
