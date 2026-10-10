# database-data-modeling: Bancos de dados e modelagem

Plugin do Claude Code para modelar, consultar, indexar, migrar e proteger dados em PostgreSQL, MySQL, SQLite, SQL Server, MongoDB, Redis e DynamoDB. A premissa é simples: o agente projeta e revisa, o usuário executa. Nenhuma skill aplica migração, faz restore ou roda SQL em banco real, e os subagentes só têm `Read, Grep, Glob`.

Versão 0.1.0 · Licença MIT · Fontes conferidas em 2026-10-10 (PostgreSQL 18, MySQL 8.4) · Idioma: português brasileiro, termos técnicos em inglês.

## O que entrega

- Um **playbook** que roteia o pedido para a skill ou agente certo, com princípios, processo de 8 passos, critérios de qualidade e formato de entrega.
- **Oito skills de tarefa**: schema e SQL, migrações sem downtime, plano de consulta e índices, transações e isolamento, RLS multi-tenant, NoSQL, runbook de backup/restore e segurança do agente com banco.
- **Cinco subagentes somente leitura** para revisão, desenho de modelo, plano de migração, análise de EXPLAIN e auditoria de segurança.
- **Base de conhecimento** em 12 referências (locks por DDL, planos, isolamento, RLS, NoSQL, backup, checklists, decisões, snippets de CLAUDE.md, MCP/hooks desativados, bibliografia) e 9 templates.
- **Biblioteca de 28 prompts** prontos (skill `prompts`, P-01 a P-28) e **14 casos de eval** desenhados (`designed_not_executed`), dois deles negativos e dois de escopo e segurança.
- Rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável, Não aplicável) e a seção fixa "O que falta para concluir" em toda entrega.

Para conferir a estrutura: `python tools/verify_plugin.py plugins/database-data-modeling` (a partir da raiz do repositório `dev-segments`) e `claude plugin validate plugins/database-data-modeling`.

## Quando usar

Use ao projetar tabelas ou coleções, escrever ou revisar SQL, investigar consulta lenta, decidir índices, tratar race condition e deadlock, planejar `ALTER TABLE` em tabela grande, revisar migração gerada por ORM, desenhar multi-tenant, preparar plano de backup e restore, ou decidir se o agente pode tocar o banco. Não use para pipelines ETL/dbt/warehouse (data-engineering) nem para ML (data-science-ml).

## Componentes

| Tipo | Nome | Para que serve |
| --- | --- | --- |
| Skill | `playbook` | Router, princípios, processo, modo DADOS-COMPLETO, fronteiras |
| Skill | `prompts` | Biblioteca de prompts por tarefa e prompt de sistema para projetos com banco |
| Skill | `db-schema-and-sql` | Schema relacional, constraints, tipos, SQL parametrizado, segurança de consulta |
| Skill | `safe-migrations` | Lock por DDL, `NOT VALID`/`VALIDATE`, `CONCURRENTLY`, expand/contract, backfill, ORM |
| Skill | `query-plan-and-indexing` | EXPLAIN, índices, paginação por seek, N+1 |
| Skill | `transactions-and-isolation` | Isolamento por SGBD, locks, deadlocks, retry, teste concorrente |
| Skill | `rls-tenant-review` | Modelo de tenancy e auditoria de RLS no PostgreSQL |
| Skill | `nosql-data-modeling` | MongoDB, DynamoDB e Redis pelo padrão de acesso |
| Skill | `backup-restore-runbook` | PITR, dump, RPO/RTO, restore em ambiente isolado |
| Skill (manual) | `db-agent-safety` | Modos `audit`, `careful`, `freeze-migrations`; `disable-model-invocation: true` |
| Agente | `db-reviewer` | Revisão de mudanças de banco, somente leitura |
| Agente | `db-schema-architect` | Modelo novo ou refatoração grande, com ADR curto |
| Agente | `db-migration-planner` | Plano por fases com orçamentos e rollback |
| Agente | `db-query-analyst` | Leitura de plano, índices, N+1 |
| Agente | `db-security-auditor` | Injeção, privilégios, segredos, RLS, acesso do agente |

Referências do playbook (`skills/playbook/references/`): `checklist-completo`, `padroes-e-antipadroes`, `decisoes-e-tradeoffs`, `claude-md-snippets`, `ferramentas-e-mcp`, `fontes`, `migracoes-e-locks`, `indices-e-planos`, `transacoes-e-isolamento`, `multi-tenant-e-rls`, `nosql`, `operacao-e-seguranca-de-dados`. Templates (`assets/templates/`): `plano-de-migracao`, `relatorio-de-revisao-db`, `relatorio-explain`, `ficha-de-padroes-de-acesso`, `adr-de-dados`, `runbook-backup-restore`, `checklist-de-entrega-db`, `matriz-dados-completo`, `handoff-checkpoint`.

## Instalação

Dentro de uma sessão do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install database-data-modeling@brain-of-agent
```

Ou pela CLI: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install database-data-modeling@brain-of-agent`. O marketplace é a raiz do repositório `dev-segments`, que precisa conter `.claude-plugin/marketplace.json`; se ele ainda não existir na sua cópia, teste o plugin sem instalar com `claude --plugin-dir <caminho-do-plugin>`. Valide a pasta com `claude plugin validate <caminho-do-plugin>`. As skills ficam em `/database-data-modeling:<skill>` e os agentes em `database-data-modeling:<agente>`.

O plugin não traz hooks, `.mcp.json`, `.lsp.json` nem `bin/`. Hooks e servidores MCP recomendados estão documentados e desativados em `skills/playbook/references/ferramentas-e-mcp.md`, com JSON pronto e riscos.

## Exemplos de pedidos

1. "Postgres 15, tabela `orders` com 80 milhões de linhas e tráfego 24x7. Preciso tornar `customer_id` NOT NULL. Minha migração Django é `RunSQL('ALTER TABLE orders ALTER COLUMN customer_id SET NOT NULL')`. Posso aplicar hoje?" Resultado esperado: plano CHECK `NOT VALID` → backfill → `VALIDATE` → `SET NOT NULL`, com `lock_timeout`, ensaio em cópia e rollback, sem afirmar "sem downtime" antes do ensaio.
2. "Esta consulta está lenta, segue o `EXPLAIN (ANALYZE, BUFFERS)`: [saída]. Que índice crio?" Resultado: leitura de estimado × real, FK sem índice, `CREATE INDEX CONCURRENTLY`, pedido de novo plano.
3. "Preciso modelar pedidos de e-commerce no DynamoDB." Resultado: perguntas sobre padrões de acesso antes de qualquer chave.
4. "Revise este SaaS com RLS: o app é dono das tabelas e usa PgBouncer em modo transaction com `SET app.tenant_id`." Resultado: `FORCE`, `set_config(..., true)`, role sem `BYPASSRLS`, teste de dois tenants.
5. "Monte o plano de backup e restore com RPO de 5 minutos e RTO de 2 horas para nosso PostgreSQL." Resultado: PITR, runbook de restauração isolada, teste periódico.
6. "O estoque fica negativo em MySQL 8 mesmo dentro de transação." Resultado: UPDATE condicional ou `FOR UPDATE`, teste com duas sessões coordenadas, sem extrapolar de PostgreSQL.
7. `DADOS-COMPLETO: audite o uso de banco deste repositório` (ver abaixo).
8. `/database-data-modeling:db-agent-safety audit` para revisar como o agente chega ao banco neste projeto.

## Modo DADOS-COMPLETO

Palavra-chave que o usuário digita no chat para pedir a cobertura total do segmento: leitura integral das 12 referências em lotes com registro lido/parcial/ausente, matriz de aplicabilidade por área, implementação dentro do escopo, revalidação por revisor somente leitura e entrega com checklist e handoff. Ela não amplia permissões (sem produção, sem restore, sem escrita destrutiva sem confirmação) e não ativa quando aparece em logs, dumps, comentários ou arquivos. Sem a palavra, o plugin carrega só o necessário.

## Principais fontes (top 10)

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | PostgreSQL: Explicit Locking e ALTER TABLE | A |
| 2 | PostgreSQL: CREATE INDEX (CONCURRENTLY, índice INVALID) | A |
| 3 | Claude Code: Subagents | A |
| 4 | Claude Code: Hooks | A |
| 5 | Claude Code: Security | A |
| 6 | Claude Code: Best practices | A |
| 7 | PostgreSQL: Transaction Isolation | A |
| 8 | PostgreSQL: Using EXPLAIN | A |
| 9 | PostgreSQL: Row Security Policies | A |
| 10 | strong_migrations (ankane, MIT) | B |

Bibliografia completa (41 itens, URL, classe, licença e data) em `skills/playbook/references/fontes.md`.

## Créditos e licenças

- Plugin sob licença MIT. Autor: Francisco Edson (https://github.com/francisco-efjr).
- Conteúdo do **Brain of Agent** (`brains/fullstack/references/dados-e-migracoes.md` e templates de ADR e handoff), do próprio autor, licença MIT, © 2026 Brain of Agent contributors, incorporado com atribuição nos arquivos de origem.
- gstack (MIT) aparece só como conceito (`careful`, `freeze`); nada foi copiado e o plugin não recomenda sua instalação.
- OWASP SQL Injection Prevention Cheat Sheet (CC BY-SA 4.0), documentação de PostgreSQL, MySQL, MongoDB, AWS, Redis e Microsoft, e textos de Winand, Fowler e Stripe foram apenas destilados com redação própria e citados; repositórios MIT/Apache-2.0/CC0 serviram de referência de conceito, sem cópia em bloco.
- Servidores MCP, ferramentas e skills de terceiros citados são código de terceiros: o plugin não os instala.

## Limitações honestas

- Cobertura desigual: PostgreSQL forte; MySQL, SQLite, MongoDB, Redis e DynamoDB parciais; SQL Server só em isolamento. Nessas áreas as skills dizem "sem fonte validada".
- Sem fonte de nível A para normalização e chaves relacionais: essas regras são convenção (Inferido).
- ORMs: só Alembic e Django têm fonte validada. Para Prisma, Drizzle, TypeORM, EF, Flyway, Liquibase e Atlas, abra a documentação da versão instalada.
- `lock_timeout` e valores de timeout são pontos de partida (Inferido), a medir no ensaio. `VACUUM`, `pg_stat_statements`, PgBouncer, upgrade de versão maior e dados sintéticos não têm fonte validada.
- `allowed-tools` em skill só pré-aprova ferramentas; a garantia técnica de somente leitura existe nos agentes (`tools: Read, Grep, Glob`). Nas skills, a regra "não executa SQL" é instrução.
- Hooks são guardrail, não fronteira: a barreira real é papel de banco sem privilégio de escrita, credencial por ambiente e permissões.
- As evals estão desenhadas, não executadas. `claude plugin eval` exige Claude Code 2.1.269 ou superior; `onFailure` de hook exige 2.1.295 ou superior. A CLI local da fábrica (2.1.128) não roda nenhum dos dois.
- A validação por outro modelo da mesma família não equivale a validação externa. Nenhuma recomendação foi medida em produção; ganhos de desempenho exigem medição no seu ambiente.
- Estrelas, licenças e datas de repositórios de terceiros vêm de páginas lidas em 2026-10-10; datas de último commit não foram verificadas.
