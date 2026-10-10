# BUILD-REPORT-quality: architecture-design

Data: 2026-10-10 · Validador: Claude Opus 5.5, em contexto de validação de prompt, com a rubrica `docs/foundation/prompt-quality-rubric.md` (D1–D12, 0–100).
Independência: os construtores eram outro modelo, mas da mesma família (Anthropic). A revisão é parcialmente independente e as notas são julgamento por leitura, não medição (AP-16). Nenhum eval foi executado.

## Escopo lido

- 10 `SKILL.md`, 5 agentes, `README.md`, `plugin.json`.
- Biblioteca de prompts inteira (`prompt-library.md`, 28 prompts). A amostra pontuada em detalhe teve 14 prompts: PR-01, 03, 04, 07, 09, 10, 11, 13, 18, 19, 22, 24, 25 e 27.
- 11 casos de eval (prompt e graders), `evals/README.md` e `.gitignore`.
- Referências checadas por Grep e leitura parcial: `ferramentas-e-mcp.md`, `checklist-completo.md`, `api-cache-escala.md`, `exemplo-contrato.md`, `checklist-api.md`, `fontes.md`, `padroes-e-antipadroes.md`, `adr-e-governanca.md`, `c4-e-diagramas.md`, `adr-madr.md`, `trigger-queries.md`.
- Fontes de apoio: `SYNTHESIS.md` e `VALIDATED.md` (por Grep). O arquivo `BUILD-REPORT-structural.md` **não existe** nesta pasta, então não havia pendências estruturais herdadas. A estrutura foi conferida contra `plugin-blueprint.md`: 12 referências, 16 templates, 28 prompts, 8 skills de tarefa, 5 agentes e 11 evals com caso negativo.

## Fidelidade técnica conferida em fonte (2026-10-10)

| Afirmação | Fonte aberta | Resultado |
| --- | --- | --- |
| `allowed-tools` restringe a skill a Read/Grep/Glob ("esta skill não tem Write nem Edit") | https://code.claude.com/docs/en/skills | **Errado.** O campo só pré-aprova ferramentas durante o turno que invoca a skill, e a concessão cai na próxima mensagem. Para remover ferramentas existe `disallowed-tools`. Corrigido. |
| Regra de permissão `Write(docs/adr/**)` | https://code.claude.com/docs/en/permissions | **Errado.** A checagem de arquivos só consulta `Edit(...)` e `Read(...)`, e `Write(path)` é aceita mas nunca consultada. O correto é `Edit(/docs/adr/**)`, com `/` relativo à origem do settings. Corrigido. |
| Idempotency-Key: 422 (corpo diferente) e 409 (em andamento), "segundo a memória do plugin" | https://www.ietf.org/archive/id/draft-ietf-httpapi-idempotency-key-header-07.html | **Confirmado**, e falta o caso 400 (chave obrigatória ausente). Todos os três são SHOULD. Rótulo trocado de Inferido para Verificado e 400 acrescentado. |
| Status do rascunho (N-03) | https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ | Confirmado: expirado, rev. 07 de 2025-10-15, página de 2026-04-18. |
| N-01: 5 camadas × 3 retries = 243×; jitter consistente por host para trabalho agendado; autor e datas | https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter | Confirmado: publicado em 2026-06-12, modificado em 2026-06-15. |
| N-05: MADR 4.0.0, data, seções e licença | https://adr.github.io/madr/ | Confirmado: 2024-09-17, MIT OR CC0-1.0, e as seções batem com `adr-madr.md`. |
| `maxTurns` em subagentes; plugins ignoram `hooks`, `mcpServers` e `permissionMode` | VALIDATED V-04 | Consistente; não reaberto. |

## Notas por artefato

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 86 | 88 | Gotcha novo sobre `allowed-tools`/`disallowed-tools` e regras `Edit(...)`. Mapa de referências aponta itens `CK-nn` e achados `ARQ-nn`. |
| `skills/adr/SKILL.md` | 82 | 88 | D12: a frase "não tem Write nem Edit" estava errada e foi substituída pela semântica real. `disallowed-tools: Write, Edit, NotebookEdit` adicionado. |
| `skills/adr-write/SKILL.md` | 84 | 89 | O aviso de segurança foi reescrito: a pré-aprovação vale só no turno de invocação e, depois do "sim", volta o fluxo normal. A regra de reforço passou a ser `Edit(/docs/adr/**)`. Gotcha de permissão corrigido com fonte. |
| `skills/api-design/SKILL.md` | 83 | 90 | Códigos 400/422/409 do Idempotency-Key verificados no rascunho 07, com URL. Status N-03 reconferido. `disallowed-tools` adicionado. |
| `skills/architecture-plan/SKILL.md` | 85 | 88 | Pré-checagem 3 corrigida sobre o alcance de `allowed-tools`; a regra de reforço passou a ser `Edit(/docs/plans/**)`. |
| `skills/decomposition/SKILL.md` | 87 | 88 | `disallowed-tools` adicionado. |
| `skills/design-review/SKILL.md` | 86 | 89 | Colisão de IDs resolvida: achados `ARQ-nn` são sequenciais e citam o item `CK-nn` de origem. `disallowed-tools` adicionado. |
| `skills/resilience-and-consistency/SKILL.md` | 87 | 89 | N-01 marcado como reconferido. `disallowed-tools` adicionado. |
| `skills/system-design/SKILL.md` | 86 | 88 | `disallowed-tools` adicionado. |
| `skills/prompts/SKILL.md` | 86 | 86 | Sem mudança: gatilhos PT-BR/EN, processo, quando não usar e checklist de adaptação já adequados. |
| `skills/prompts/references/prompt-library.md` (amostra de 14) | 86 | 88 | PR-19: N-01 reconferido. PR-22: códigos do rascunho 07. PR-27: a regra de Mermaid agora é coerente com PR-23 ("sintaxe não validada por parser" em vez de "sem sintaxe válida, sem entrega"). |
| `agents/adr-writer.md` | 82 | 87 | Checa por Glob se o arquivo já existe, porque Write sobrescreve sem avisar. Compara o índice regravado com o original. Saída ganhou "Conteúdo suspeito" e "não roda comandos". |
| `agents/architecture-blueprint.md` | 88 | 88 | Sem mudança. |
| `agents/architecture-reviewer.md` | 90 | 90 | Sem mudança. Read-only, limiar, "sem lacunas", exemplo de achado. |
| `agents/boundary-mapper.md` | 88 | 88 | Sem mudança. |
| `agents/skeptic-architect.md` | 88 | 88 | Sem mudança. |
| `evals/` (11 casos + README) | 87 | 87 | Sem mudança nos casos: PASS/FAIL observáveis, caso negativo com `max: 0`, injeção com domínio `.invalid`, graders `tool_used` contra escrita, rede e `npx`. |
| `skills/playbook/references/ferramentas-e-mcp.md` | 72 | 88 | D12: a sintaxe de permissão estava errada e foi corrigida para `Edit(/...)`, com fonte. O script do hook foi endurecido (`realpath`; outro drive bloqueia em vez de liberar) e testado isolado em 6 casos. Novo gotcha sobre `allowed-tools`/`disallowed-tools`. |
| `skills/playbook/references/checklist-completo.md` | 82 | 87 | Itens renomeados de `ARQ-01..76` para `CK-01..76`, porque colidiam com os IDs sequenciais de achado. O formato de achado ganhou a coluna "Item CK-nn". Citações em `padroes-e-antipadroes.md` e `api-cache-escala.md` foram atualizadas. |
| `README.md` | 86 | 88 | Checklist `CK-nn`. Nova explicação de `disallowed-tools` nas skills somente leitura. Semântica allow/deny para o `adr-writer`. Limitações atualizadas: o que foi conferido em doc e o que segue não testado. |

Outras correções:

- `exemplo-contrato.md` e `api-cache-escala.md`: tabelas de Idempotency-Key com 400/422/409 verificados.
- `fontes.md`: N-01, N-03 e N-05 marcados como reconferidos.
- `checklists-padroes.md`: rótulo de N-01 atualizado.
- `trigger-queries.md`: sumário e consultas de gatilho para `playbook` e `prompts`, que estavam ausentes. Ficaram 8 positivas e 8 negativas limítrofes por skill.

Resumo das notas: média antes ≈ 81,0, média depois ≈ 83,9, mínimo depois = 86, com 21 unidades pontuadas. Nenhum critério de reprovação automática foi encontrado:

- nada de execução inventada;
- nenhuma ação externa sem confirmação;
- conteúdo externo tratado como dado;
- literal de terceiros só do brain-of-agent (MIT, do usuário), com atribuição;
- sem segredos;
- `--dangerously-skip-permissions` aparece só como risco, restrito a sandbox.

## Segurança e direitos autorais

- Revisores e arquitetos: `tools: Read, Grep, Glob`, sem Write/Edit. Só o `adr-writer` tem Write, é acionado sob pedido explícito e tem fluxo de duas chamadas com aprovação citada.
- Skills com efeito (`adr-write`, `architecture-plan`) usam `disable-model-invocation: true` e mostram e perguntam antes de gravar.
- As seis skills somente leitura ganharam `disallowed-tools: Write, Edit, NotebookEdit`. É reforço, não garantia: a restrição cai na próxima mensagem do usuário.
- Literais encontrados: template de ADR (27 linhas) e mensagem inicial (6 linhas), ambos do brain-of-agent (MIT, Francisco Edson), com atribuição. O resto é redação própria. OWASP (CC BY-SA) só aparece destilado.
- Evals: o fixture de injeção (`exemplo.invalid`) fica dentro de `<readme>` e tem graders que proíbem curl, escrita e `~/.ssh`. Durante a validação ele foi tratado como dado de teste e não foi seguido.

## Verificação executada

- `python tools/verify_plugin.py plugins/architecture-design` → `RESULT: PASS` (antes e depois das edições).
- `claude plugin validate plugins/architecture-design` (Claude Code 2.1.128) → `Validation passed` (antes e depois).
- Script do hook de exemplo testado em scratchpad com JSON via stdin. `docs/adr/a.md` sai com 0. `src/x.ts`, `docs/../src/y.ts`, outro drive, caminho vazio e `docsx/a.md` saem com 2.

## Pendências

1. `BUILD-REPORT-structural.md` não existe. Se o validador estrutural rodou, o relatório dele se perdeu. Se não rodou, falta essa etapa.
2. Os evals continuam `designed_not_executed`. O Claude Code local é 2.1.128 e `claude plugin eval` exige 2.1.269 ou superior.
3. `disallowed-tools` foi conferido na doc atual, mas não testado em sessão real. Versões antigas podem ignorar o campo (Não verificado). O `plugin validate` 2.1.128 aceitou o campo.
4. As regras `Edit(/docs/adr/**)` e o hook não foram testados integrados ao Claude Code.
5. Não há caso de eval próprio para `adr-write`, `architecture-plan` nem para os agentes. São 11 casos contra 6–10 do blueprint; a decisão de manter ou cortar um caso fica com o dono do plugin.
6. Seguem como Inferido as lacunas de fonte primária listadas no README: Clean Architecture, Evans/Vernon, fitness functions, load shedding e STRIDE da Microsoft. Também segue Inferido o status "experimental" do C4 no Mermaid.
7. `graphify update .` não foi rodado: as edições foram em Markdown, e a regra do CLAUDE.md fala de arquivos de código. Além disso, a raiz do graph fica fora de `dev-segments`.
