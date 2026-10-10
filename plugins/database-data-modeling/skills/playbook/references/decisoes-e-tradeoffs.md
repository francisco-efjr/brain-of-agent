# Decisões e trade-offs

Sumário: 1 Como decidir · 2 Engine · 3 Normalizar ou desnormalizar · 4 Embutir ou referenciar · 5 Nível de isolamento · 6 Modelo de tenancy · 7 Particionar? · 8 Algoritmo de DDL no MySQL · 9 RDB, AOF ou ambos · 10 RLS: sim ou não · 11 Migração por ferramenta ou manual · 12 Registrar a decisão

Uma decisão material vira ADR (`adr-de-dados.md`) com alternativas, consequências, reversibilidade e gatilho de revisão. Decisão trivial não gera documento (proporcionalidade). Rótulos: V-nn = fonte validada; Inferido = leitura minha.

## 1. Como decidir

Engine + padrão de acesso + invariantes + volume + equipe decidem. Prefira a tecnologia que a equipe já opera, salvo requisito que ela não atenda. Registre a versão alvo: regras mudam por versão.

## 2. Engine

| Se o requisito dominante é… | Considere | Cuidado |
| --- | --- | --- |
| Invariantes entre entidades, consultas ad hoc, transações multi-linha | PostgreSQL (ou MySQL/SQL Server se já operados) | modelagem relacional sem fonte A (L-01): Inferido |
| Agregado lido/escrito inteiro, schema variável | MongoDB | documentos ilimitados; 16 MB |
| Poucos padrões de acesso conhecidos, escala altíssima, operação gerenciada | DynamoDB | perguntas antes do schema; hot partition |
| Cache, contadores, ranking, fila leve | Redis | persistência e backup definidos; não é fonte de verdade por padrão |
| App local/embarcado, um escritor | SQLite | WAL/pragmas sem fonte (L-08) |
| Warehouse, BI, ETL | fora daqui: `/data-engineering:playbook` | |

O modelo do Claude escolhe PostgreSQL por padrão em 58,4% dos casos de banco medidos em V-39 (sinal): declare a escolha no CLAUDE.md em vez de deixar implícita.

## 3. Normalizar ou desnormalizar

Relacional começa normalizado até 3FN com constraints; desnormalize apenas com medição (plano, p95) e com plano de manter a cópia consistente (trigger, job, view materializada). NoSQL começa nas perguntas. Fonte: V-32 (B, convenção, Inferido), V-26, V-25. Gatilho para desnormalizar: join comprovadamente caro no plano, leitura muito mais frequente que escrita, cópia tolerante a obsolescência.

## 4. Embutir ou referenciar (MongoDB, V-25)

Embutir: "contém", consultado junto, cardinalidade baixa e limitada. Referenciar: alta cardinalidade, crescimento sem limite, existência própria. Pergunta decisiva: qual a cardinalidade e o crescimento do filho? Duplicação aceitável conforme sensibilidade a obsolescência (imutável e tolerante: duplicar; sensível: referenciar).

## 5. Nível de isolamento

| Necessidade | Escolha | Custo |
| --- | --- | --- |
| Ler-validar-gravar de uma linha | UPDATE condicional em RC | nenhum extra |
| Regra entre várias linhas (write skew) | SERIALIZABLE (PG: SSI) com retry de 40001 | abortos e retries; custo é Suposição a medir |
| Relatório consistente em várias consultas | REPEATABLE READ/snapshot, READ ONLY | PG: pode falhar com 40001 ao escrever |
| MySQL com muitos deadlocks por gap lock | considerar READ COMMITTED (binlog row-based) | phantoms (V-09) |
| SQL Server com leitores bloqueando escritores | avaliar `READ_COMMITTED_SNAPSHOT` | versões de linha; exige janela para ligar (V-09) |

Nunca extrapole entre engines (`transacoes-e-isolamento.md`).

## 6. Modelo de tenancy (V-33)

Poucos tenants grandes com exigências próprias (chaves, região, backup): banco por tenant. Muitos tenants pequenos: banco compartilhado com `tenant_id`. Meio-termo: sharding por grupos. Complexidade de migrar N bancos é custo real. Decida pelo menor modelo que atende ao isolamento exigido; RLS soma defesa, não substitui a escolha. Handoff de produto (billing, SSO, exclusão de tenant): `/saas-multitenant:playbook`.

## 7. Particionar? (PostgreSQL, V-13)

Particione quando a retenção por `DROP/DETACH` ou a poda por chave traz ganho medido ou operacional claro (apagar partições antigas sem `DELETE` em massa). Chave pelo `WHERE` e pela retenção; PK e UNIQUE incluem a chave. Não particione por reflexo: "nunca assuma que mais partições é melhor"; cada consulta sem a chave varre todas as partições. Alternativas primeiro: índice melhor, arquivamento, tabela de resumo.

## 8. Algoritmo de DDL no MySQL (V-16)

Prefira `INSTANT`, depois `INPLACE`; `COPY` só com janela ou ferramenta online. Declare `ALGORITHM` e `LOCK` para falhar cedo. Confira a versão (8.4 lida).

## 9. RDB, AOF ou ambos (Redis, V-27)

RDB sozinho se alguns minutos de perda são aceitáveis; RDB + AOF para durabilidade comparável ao PostgreSQL; AOF sozinho é desencorajado. Se Redis é só cache, a decisão é a ausência de persistência com a fonte de verdade em outro banco.

## 10. RLS: sim ou não (V-12, V-33)

Sim quando: banco compartilhado no PG, vários caminhos de acesso (serviços, BI) e o custo de teste/pool é aceito. Não necessariamente quando: um único serviço com camada de acesso disciplinada e testes, ou banco/schema por tenant. Se sim: role mínima, `FORCE`, `set_config` por transação, teste de dois tenants. Se não: o código inteiro é a fronteira; documente e teste.

## 11. Migração por ferramenta ou manual (V-30)

Use o migrador do projeto, mas o SQL gerado é rascunho que se revisa e ensaia. Escrever SQL manual versionado faz sentido para DDL online sensível (CONCURRENTLY, NOT VALID). Uma mudança por arquivo.

## 12. Registrar a decisão

Use `adr-de-dados.md`. Campos mínimos: contexto, opções (benefício, custo/risco, evidência), decisão, consequências, reversibilidade (o que reverte código, o que exige restauração), gatilho de revisão. Rótulo cada hipótese não confirmada como Suposição.
