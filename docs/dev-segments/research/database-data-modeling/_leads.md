# database-data-modeling — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| supabase/agent-skills (EC-21) | https://github.com/supabase/agent-skills | B (6) | Regras de Postgres em 8 categorias (query, conexões, schema, locks, RLS, monitoramento). MIT (HTML); conteúdo não lido (Suposição de qualidade). |
| wshobson/agents, `database-design` (EC-10) | https://github.com/wshobson/agents | B | Plugin de design de banco (nome citado); abrir e verificar. MIT. |
| Subagentes: db-reader com hook PreToolUse (AO-09) | https://code.claude.com/docs/en/subagents | A | Exemplo oficial: agente somente leitura que bloqueia escrita por hook (`exit 2`). Plugins ignoram `hooks` em agentes. |
| Hooks (AO-10, CP-19) | https://code.claude.com/docs/en/hooks | A | `PreToolUse/Edit|Write` negando `migrations/`; bloquear `DROP TABLE`. Regex não substitui revisão; documentar, não ativar. |
| Sanity, "First attempt will be 95% garbage" (CP-22) | https://www.sanity.io/blog/first-attempt-will-be-95-garbage | B | DB de produção nunca conectado ao agente; read-only em não-prod. |
| NestJS anti-hallucination (CT-08) | https://github.com/PatrickJS/awesome-cursorrules | B | `synchronize: true` nunca em produção; config tipada. CC0. |
| Jason Liu, RAG (PC-20) | https://jxnl.co/writing/2024/05/22/systematically-improving-your-rag/ | B | Query understanding estruturada; relevante a bancos vetoriais. Não reverificado. |
| rmoff, dbt real (CP-26) | https://rmoff.net/2026/03/11/claude-code-isnt-going-to-replace-data-engineers-yet/ | B | Contagem origem vs destino; idempotência; testes unique/not null/relationships. |
| Amplifying (CP-24) | https://amplifying.ai/research/claude-code-picks | B | Declarar ORM e banco antes de gerar. |
| gstack `/cso` e `/careful` (BR-22) | https://github.com/garrytan/gstack | B | Pausar antes de comando destrutivo, com confirmação explícita; hook só como exemplo desativado. |
| `/plan-eng-review` (BR-21) | https://github.com/garrytan/gstack | B | Itens de migração e rollback, concorrência, authz no checklist. |
| Security-and-owasp (CT-16) | https://github.com/github/awesome-copilot | B | Consultas parametrizadas. MIT. |
| PySpark ETL .mdc (CT-11) | https://github.com/PatrickJS/awesome-cursorrules | B | "Validate primary key uniqueness after writes"; merges idempotentes. CC0. |

## 2. Repositórios e arquivos a abrir
- `supabase/agent-skills`: regras de Postgres (RLS, locks, schema, índices); verificar LICENSE.
- `wshobson/agents/plugins/database-design`.
- `anthropics/claude-code` docs de subagentes e hooks (`db-reader`).
- `PatrickJS/awesome-cursorrules/rules/pyspark-etl-best-practices-…mdc`, `nestjs-anti-hallucination-…mdc`.
- Documentação oficial de PostgreSQL, MySQL, MongoDB, Redis, DynamoDB, e padrões expand/contract não estão no atlas: lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-09 (db-reader), AO-10 (hooks), AO-23 (escopo estreito de autorização, defesa em profundidade), AO-01 (confirmar ações destrutivas). Docs: https://code.claude.com/docs/en/security.

## 4. Padrões da comunidade
- Produção jamais conectada ao agente; leitura livre, escrita confirmada (CP-22, CP-15).
- Hook de negação em `migrations/` e comandos destrutivos como exemplo documentado, não ativo (CP-19).
- Idempotência e reconciliação antes de confiar em pipelines (CP-26).
- Revisão de decisões "literais do prompt" (ex.: SCD2 só numa entidade) (CP-26).

## 5. O que o brain-of-agent já oferece
- `brains/fullstack/references/dados-e-migracoes.md` (próprio, MIT).
- BR-21: checklist com migração e rollback; BR-22: `/careful`, `/guard`, `/freeze`.
- BR-14: OWASP Top 10:2025 (A01 e A03 relevantes a dados). BR-03: modo `DADOS-COMPLETO`.
- Coverage do brain é rasa em database (BR transversais).

## 6. Lacunas e cuidados
- Sem fonte A para índices, planos de execução, isolamento de transações, particionamento, backup/restore, ORMs por stack.
- supabase/agent-skills e wshobson não foram lidos: Suposição de qualidade.
- Qualquer script que execute SQL em banco real exige autorização explícita; plugin deve ser somente leitura por padrão.
