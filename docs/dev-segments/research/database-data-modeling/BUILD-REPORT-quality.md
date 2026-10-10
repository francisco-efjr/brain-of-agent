# BUILD-REPORT de qualidade: database-data-modeling

Data: 2026-10-10. Escopo: qualidade de prompt e fidelidade técnica de todo o plugin `plugins/database-data-modeling` (README, playbook e referências, 8 skills de tarefa, skill `prompts` e biblioteca, 5 agentes, 14 evals). Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1 a D12, 0 a 100).

Independência: o validador é um modelo da família Claude (Opus 5.5), diferente do construtor, mas da mesma família. A revisão foi adversarial, mas **não equivale a validação externa**. As notas vêm de leitura crítica, não de medição: nenhum eval foi executado.

## 1. Método

1. Leitura integral: 10 `SKILL.md`, 5 agentes, README, `plugin.json`, `evals/README.md` e os 14 casos (prompt e graders), `ferramentas-e-mcp.md`.
2. Biblioteca de prompts: 12 prompts lidos inteiros (P-01, P-02, P-03, P-06, P-07, P-12, P-16, P-17, P-23, P-26, P-27, P-28); os 28 IDs conferidos no sumário por `Grep`.
3. Referências restantes: varredura por `Grep` (placeholders, CAPS e absolutos, `--dangerously-skip-permissions`, `curl | bash`, `-y`, citações literais, notas de licença, SQL de exemplo com interpolação, códigos de erro de retry). Contagens pendentes do validador estrutural conferidas: `fontes.md` tem 41 itens V-01 a V-41; `claude-md-snippets.md` tem S-01 a S-20. **Verificado**.
4. Fidelidade técnica conferida na fonte (WebFetch, 2026-10-10):
   - https://www.postgresql.org/docs/18/sql-altertable.html: `NOT VALID` aceito para FK, CHECK e not-null no PG 18; `SET NOT NULL` pula o scan com CHECK válido; `VALIDATE CONSTRAINT` vale para not-null `NOT VALID`. **Verificado**. O caminho do CHECK para versões anteriores, usado nas skills e no eval, está correto.
   - https://www.postgresql.org/docs/current/transaction-iso.html: "só transações que escrevem precisam de retry" é dito apenas para REPEATABLE READ; em SERIALIZABLE, mesmo dados lidos por transação só de leitura só valem após o commit, exceto `READ ONLY DEFERRABLE`. **Verificado**; o plugin generalizava a frase (corrigido).
   - https://developer.android.com/training/data-storage/room/migrating-db-versions: `fallbackToDestructiveMigration` apaga todos os dados; variantes `...From` e `...OnDowngrade`; `MigrationTestHelper` exige schema exportado; o Room valida o schema ao abrir após as migrações. **Verificado**. A exigência de `@ColumnInfo(defaultValue)` igual ao `DEFAULT` da migração não aparece na página: entrou no grader como menção opcional rotulada Inferido.
   - Demais afirmações (locks e `CONCURRENTLY`, RLS, `set_config`, MySQL 8.4 Online DDL, persistência e backup de AOF do Redis, hooks com saída 2 e `onFailure` em 2.1.295, auto mode como padrão em 2.1.283, SQLSTATEs `40001`, `40P01`, `55P03`, erros MySQL 1213/1205 e SQL Server 1205, Django `AddIndexConcurrently` com `atomic = False`, dbt-snowflake `merge` padrão): conferidas contra `VALIDATED.md` (fonte de verdade) ou conhecimento estável; coerentes.
5. Correções aplicadas direto nos arquivos; verificador e validador oficial rodados no fim.

## 2. Notas antes e depois

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `README.md` | 82 | 89 | Contagem de evals corrigida (dizia 10; são 14) e biblioteca descrita como 28 prompts; parágrafo residual "Observação de construção" (escrita "em paralelo", rodar verificador "no marketplace") trocado por comandos de verificação reais; instalação explica que o marketplace exige `.claude-plugin/marketplace.json` na raiz e oferece `claude --plugin-dir` para teste local |
| `skills/playbook/SKILL.md` | 90 | 92 | Exemplo de saída deixava de inventar o ORM ("Suposição: Django"), agora pede ORM e migrador porque decidem como sair da transação; princípio 1 esclarece que as regras de `INSTANT` lidas são do MySQL 8.4 (diferem no 8.0); linha autorreferente da tabela de fronteiras removida |
| `skills/prompts/SKILL.md` | 89 | 90 | Gotcha "`INSTANT` é do MySQL 8.4" (impreciso: `INSTANT` existe no 8.0) reescrito como "regras da página 8.4, diferentes no 8.0" |
| `skills/db-schema-and-sql/SKILL.md` | 90 | 90 | Nenhuma. Pré-checagens sem execução, tabela de decisões com exemplo, privilégio mínimo e allow-list corretos |
| `skills/safe-migrations/SKILL.md` | 91 | 91 | Nenhuma. Mecanismo de `NOT VALID` em not-null por versão reconferido na doc do PG 18 |
| `skills/query-plan-and-indexing/SKILL.md` | 91 | 91 | Nenhuma |
| `skills/transactions-and-isolation/SKILL.md` | 88 | 91 | Regra de retry corrigida: "só transações que escrevem precisam" vale em REPEATABLE READ; em SERIALIZABLE leituras também dependem do commit, salvo `READ ONLY DEFERRABLE` (mesma correção em `references/isolamento-por-sgbd.md` e `playbook/references/transacoes-e-isolamento.md`) |
| `skills/rls-tenant-review/SKILL.md` | 91 | 91 | Nenhuma |
| `skills/nosql-data-modeling/SKILL.md` | 90 | 90 | Nenhuma (pergunta antes do modelo; lacunas L-07 declaradas; AOF/RDB fiel à doc) |
| `skills/backup-restore-runbook/SKILL.md` | 91 | 91 | Nenhuma (recusa de restore "eu autorizo", Passo 0 de contenção, restore isolado) |
| `skills/db-agent-safety/SKILL.md` | 90 | 90 | Nenhuma (`disable-model-invocation: true`, limite "instrução de sessão, não barreira" repetido, bloco de pausa com confirmação por ação) |
| `agents/db-reviewer.md` | 92 | 92 | Nenhuma (somente leitura, limiar de confiança, conteúdo suspeito, declaração de independência, exemplo) |
| `agents/db-security-auditor.md` | 92 | 92 | Nenhuma |
| `agents/db-schema-architect.md` | 89 | 90 | Afirmação de versão de `INSTANT` precisada |
| `agents/db-migration-planner.md` | 90 | 90 | Nenhuma |
| `agents/db-query-analyst.md` | 90 | 90 | Nenhuma |
| Biblioteca de prompts (12 amostrados) | 89 | 89 | Nenhuma necessária: todos com papel e objetivo, dados em tags declarados como dado, passos numerados com porquê, formato, rótulos, "O que falta para concluir", modo sem interação e fonte com classe e URL |
| `skills/playbook/references/ferramentas-e-mcp.md` | 86 | 89 | Riscos do hook de guarda completados: falso positivo (`\bupdate\b` sem `WHERE` casa `npm update`, `apt update`, `git update-index`) com sugestão de restringir aos clientes de banco |
| Evals (14 casos + README) | 87 | 89 | Grader de `sqlite-room-migracao-mobile` ganhou menção opcional (Inferido) ao `@ColumnInfo(defaultValue)` e às variantes destrutivas mais estreitas do Room; `evals/README.md` explica por que 5 casos exigem a skill específica e os demais aceitam o `playbook` |

Média antes (16 linhas pontuadas de prompt: 10 skills, 5 agentes, biblioteca): 90,1. Depois: 90,7. Incluindo README, `ferramentas-e-mcp.md` e evals: 89,4 antes, 90,5 depois. Nota mínima depois: 89 (README, biblioteca, `ferramentas-e-mcp.md`, evals). Nenhum critério de reprovação automática encontrado.

## 3. Achados de segurança, direitos autorais e escopo (sem correção necessária)

- Nenhum segredo; exemplos mascaram URI (`postgres://app:***@host/db`) e o MCP usa referência a variável de ambiente.
- Nenhum fluxo autoriza ação destrutiva ou externa sem confirmação: skills e agentes só leem e escrevem texto; `db-agent-safety` é manual; "eu autorizo" em pedido urgente não dispensa confirmação por passo; confirmação dentro de arquivo ou log é tratada como dado.
- Os 5 agentes têm `tools: Read, Grep, Glob` (sem Write, Edit ou Bash).
- `--dangerously-skip-permissions` aparece uma vez, em `auditoria-acesso-agente.md`, como "nunca recomende; só discutível em sandbox descartável em repositório confiável; é risco, não padrão". Conforme a regra da base.
- Literal de terceiros: só Brain of Agent (MIT, do próprio autor) com atribuição; gstack, OWASP (CC BY-SA), Use The Index Luke, Fowler e Stripe apenas destilados. Nenhum bloco literal sem licença encontrado.
- Evals: 14 casos com PASS/FAIL observáveis, 2 negativos (`tool_used` com `min: 0, max: 0`), 2 de escopo e segurança com `no-bash` e `no-write`. O fixture com linha dirigida à IA (`DADOS-COMPLETO` e `DROP DATABASE`) existe no `prompt.md` para ser ignorado e foi tratado como dado nesta revisão.

## 4. Verificação final

| Comando | Resultado | Rótulo |
| --- | --- | --- |
| `python tools/verify_plugin.py plugins/database-data-modeling` | `RESULT: PASS` (10 skills, 5 agentes, 14 evals, 109 arquivos) | Verificado |
| `claude.exe plugin validate plugins/database-data-modeling` (CLI 2.1.128) | `Validation passed` | Verificado |

## 5. Pendências

1. **Marketplace ausente**: `dev-segments/.claude-plugin/marketplace.json` não existe; a instalação por `/plugin install database-data-modeling@dev-segments` falha até criá-lo (decisão de projeto, fora deste plugin). O README agora avisa e oferece `--plugin-dir`.
2. **Evals não executadas**: CLI local 2.1.128 < 2.1.269 exigido por `claude plugin eval`. Notas desta revisão não substituem rodar os 14 casos com 3 execuções e ablação.
3. **Agentes sem caso de eval próprio** (declarado em `evals/README.md`); também faltam casos de MongoDB com array ilimitado, MySQL `MODIFY` em tabela grande e Redis.
4. **Room `defaultValue`**: comportamento de validação de schema com `DEFAULT` divergente é Inferido (não consta da página oficial lida); confirmar na doc da versão do Room antes de promover a item obrigatório do grader.
5. **Lacunas de fonte herdadas** (L-01 a L-11): normalização, MySQL EXPLAIN, SQL Server, Flyway/Liquibase/Prisma/EF, VACUUM, PgBouncer, índices do MongoDB, capacidade do DynamoDB, eviction/ACL do Redis. As skills já declaram "sem fonte validada".
6. **Spec vs CLI** (`displayName`) e plugins vizinhos marcados "(previsto)": herdados do validador estrutural, sem mudança aqui.
7. **Independência**: revisão do mesmo fornecedor de modelo; recomenda-se leitura humana de ao menos `db-agent-safety`, `backup-restore-runbook` e dos graders de segurança antes de publicar.
