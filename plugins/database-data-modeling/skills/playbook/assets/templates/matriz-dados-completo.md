# Matriz DADOS-COMPLETO

Projeto/objeto: [nome] · Pedido e escopo: [objetivo] · Revisão/ambiente: [commit, SGBD e versão] · Data: [AAAA-MM-DD]
Autorização: [análise | implementação local | ações externas específicas (liste)]
A keyword não amplia permissões. Sem produção, sem restore, sem escrita destrutiva sem confirmação por ação.

## 1. Leitura das referências (lotes)

Marque uma coluna por arquivo: lido, parcial ou ausente.

| Lote | Arquivo | lido | parcial | ausente | Decisão extraída |
| --- | --- | --- | --- | --- | --- |
| a | migracoes-e-locks.md | | | | |
| a | transacoes-e-isolamento.md | | | | |
| b | indices-e-planos.md | | | | |
| b | nosql.md | | | | |
| c | multi-tenant-e-rls.md | | | | |
| c | operacao-e-seguranca-de-dados.md | | | | |
| d | padroes-e-antipadroes.md | | | | |
| d | decisoes-e-tradeoffs.md | | | | |
| d | checklist-completo.md | | | | |
| e | ferramentas-e-mcp.md | | | | |
| e | claude-md-snippets.md | | | | |
| e | fontes.md | | | | |

## 2. Aplicabilidade por área

| Área | aplica | não aplica (motivo) | lacuna de informação | Skill/agente usado | Evidência |
| --- | --- | --- | --- | --- | --- |
| Modelagem e normalização | | | | db-schema-and-sql, db-schema-architect | |
| Constraints e tipos | | | | db-schema-and-sql | |
| Índices | | | | query-plan-and-indexing | |
| Planos de execução | | | | db-query-analyst | |
| Transações e isolamento | | | | transactions-and-isolation | |
| Locks e DDL | | | | safe-migrations | |
| Migrações e backfill | | | | db-migration-planner | |
| ORM | | | | safe-migrations | |
| Multi-tenant e RLS | | | | rls-tenant-review, db-security-auditor | |
| Backup e restore | | | | backup-restore-runbook | |
| Particionamento | | | | db-schema-architect | |
| Segurança de dados | | | | db-security-auditor | |
| NoSQL | | | | nosql-data-modeling | |
| Acesso do agente ao banco | | | | db-agent-safety | |

## 3. Backlog rastreável

| ID | Requisito ou risco | Critério | Análise | Implementação (arquivos) | Validação | Revalidação | Evidência | Pendência |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Estados: pendente, inferido, verificado, falhou, não autorizado, NA, NV.

## 4. Revalidação final

Revisão pelo db-reviewer em contexto limpo e somente leitura: [resumo]. Declaração: revisão pelo mesmo modelo não é validação externa.
Checks invalidados por mudanças posteriores: [..]

## 5. Resultado

Leitura: [integral | parcial] · Execução: [completa no escopo | parcial | não executada] · Críticos abertos: [IDs] · Recomendação: [..]
