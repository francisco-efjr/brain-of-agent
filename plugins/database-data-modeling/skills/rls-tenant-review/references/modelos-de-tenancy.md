# Modelos de tenancy: matriz de decisão

Conferido em 2026-10-10 contra V-33 (Microsoft Learn, "approaches to storage and data for multitenant solutions", atualizada em 2026-10-08, Verificado no cabeçalho; orientado a Azure) e V-12. A página compara por escala, previsibilidade de desempenho, isolamento, complexidade e custo; os padrões listados são banco compartilhado, sharding, banco por tenant e stamps. "Schema por tenant" não foi tratado como padrão próprio pela página: as linhas correspondentes são Inferido. Texto aqui é destilação com redação própria.

Sumário
1. Matriz
2. Antipadrões
3. Como decidir (perguntas)
4. Compatibilidade de versões de schema
5. RLS dentro de cada modelo
6. Registro da decisão

## 1. Matriz

Legenda: favorável / neutro / desfavorável é leitura do autor (Inferido) a partir dos critérios de V-33; ajuste ao seu contexto.

| Modelo | Escala (nº de tenants) | Isolamento | Noisy neighbor | Operação e migração de schema | Custo por tenant | Backup/restore por tenant | Quando escolher |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Banco compartilhado, tabelas com `tenant_id`** | muito alta | lógico (aplicação + RLS opcional) | exposto: um tenant pesado afeta todos | uma migração para todos; simples | menor | difícil (precisa extrair por `tenant_id`) | muitos tenants pequenos, custo baixo, equipe pequena |
| **Schema por tenant** (mesmo banco) | média | lógico mais forte (privilégios por schema) | exposto (mesmo servidor) | migração roda N vezes; catálogo cresce com N | médio | melhor que compartilhado (dump por schema, Inferido) | dezenas a poucas centenas de tenants com necessidade de separação lógica |
| **Banco por tenant** | baixa a média | forte (chaves, backup, região por tenant, V-33) | isolado por banco; recursos ainda do servidor se compartilhado | N bancos para migrar e monitorar | maior | simples por tenant | exigência contratual/compliance, tenants grandes |
| **Sharding** (grupos de tenants por instância) | muito alta | lógico dentro do shard | contido por shard | roteamento + migração por shard; complexidade alta | médio | por shard | crescimento além de uma instância |
| **Stamps** (implantações completas replicadas) | alta | forte por stamp | contido | operação de várias implantações | alto | por stamp | requisitos regionais/isolamento total; escala por replicação |

## 2. Antipadrões (V-33)

- **Tabela por tenant** e **coluna por tenant** (relacional): explodem objetos e tornam consultas e migrações ingerenciáveis.
- **Mudança manual de schema** em cada tenant: divergência silenciosa; automatize com ferramenta de migração e registre a versão por tenant.
- **Depender de uma única versão do schema**: a implantação precisa conviver com ao menos uma versão anterior (coexistência durante deploy) — ligação direta com `safe-migrations` (expand/contract).
- Escolher RLS **antes** de escolher o modelo: muitas soluções multi-tenant não usam RLS pela complexidade de propagar identidade (V-33).

## 3. Como decidir (perguntas, uma por vez, só as que mudam a decisão)

1. Quantos tenants em 12 meses e qual o maior em volume de dados e tráfego?
2. Algum tenant exige isolamento contratual (chave própria, região, backup separado, exclusão garantida)?
3. O desempenho de um tenant pode degradar outro sem aviso? Há SLA por tenant?
4. Qual a capacidade da equipe de operar N bancos/schemas e migrá-los?
5. Existem consultas entre tenants (analytics global)? Isso favorece o compartilhado.
6. Como o tenant é identificado em cada requisição e como essa identidade chega ao banco (pool, ORM)?

Sem resposta a 1 e 2, a recomendação é condicional ("se até X tenants e sem exigência de isolamento: compartilhado com `tenant_id`; se houver exigência: banco por tenant para esses clientes") e rotulada Suposição.

## 4. Compatibilidade de versões de schema

- Mantenha migrações compatíveis com a versão anterior da aplicação (expand/contract). Em schema/banco por tenant, a migração de N unidades roda em ondas; durante a onda coexistem tenants em versões diferentes: a aplicação deve suportar ambas até o fim.
- Registre uma tabela de controle (tenant, versão de schema, data) quando houver N schemas/bancos (Inferido).
- Falha numa unidade não deve parar as demais: política de retry e de quarentena do tenant.

## 5. RLS dentro de cada modelo

| Modelo | Papel do RLS |
| --- | --- |
| Compartilhado | Defesa em profundidade contra falha da aplicação (esquecer o `WHERE tenant_id`); custo de contexto por transação e testes |
| Schema por tenant | Geralmente desnecessário; o isolamento vem de privilégios por schema e `search_path` controlado (Inferido) |
| Banco por tenant | Desnecessário; o isolamento é a fronteira do banco |
| Sharding | Dentro do shard, como no compartilhado |

## 6. Registro da decisão

Registre em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/adr-de-dados.md`: contexto (respostas da seção 3), decisão, alternativas descartadas e por quê, consequências (operação, custo, migração), reversibilidade (custo de trocar de modelo depois é alto: estimar), gatilho de revisão (ex.: "mais de 1.000 tenants" ou "primeiro cliente com exigência de região própria").
