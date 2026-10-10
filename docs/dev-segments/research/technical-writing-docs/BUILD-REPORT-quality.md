# BUILD-REPORT qualidade de prompt: technical-writing-docs

Data: 2026-10-10. Escopo: playbook, 8 skills de tarefa, skill `prompts`, 4 agentes, biblioteca de prompts, evals, README e referências do playbook. Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1 a D12, 0 a 100).

**Independência (declaração):** o validador é o mesmo modelo (Claude Sonnet 5.5) que a família dos construtores. A revisão reduz erros, mas não é validação externa. Notas são autoatribuídas por leitura; nenhum eval foi executado (`designed_not_executed`).

## 1. Notas antes e depois

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 86 | 90 | Gotcha de AGENTS.md completado com a configuração `claude-md-and-agents-md` e com o que não conta na checagem; versão mínima do `/doctor prompt-audit` (2.1.283); apontamento da legenda de códigos V/C/G |
| `skills/prompts/SKILL.md` | 87 | 89 | Sem mudança no corpo; inconsistência de contagem (35 prompts) corrigida no README e na biblioteca |
| `skills/auditar-claude-md/SKILL.md` | 86 | 90 | Versão mínima e escopo do `/doctor prompt-audit`; códigos opacos (C-01, C-03, C-15) trocados por frases |
| `skills/diagramar-arquitetura/SKILL.md` | 88 | 90 | Referência opaca "conflito C-10" trocada por regra direta |
| `skills/documentar-codigo/SKILL.md` | 87 | 89 | Código opaco "C-06" removido |
| `skills/escrever-adr/SKILL.md` | 90 | 90 | Nenhuma correção necessária |
| `skills/escrever-changelog-release/SKILL.md` | 87 | 88 | Sem mudança; risco residual registrado: `Bash(git log *)` não impede `--output` tecnicamente (proibido por instrução) |
| `skills/escrever-guia-diataxis/SKILL.md` | 88 | 90 | Códigos opacos C-09 e C-04 removidos |
| `skills/escrever-readme/SKILL.md` | 87 | 89 | "conflito C-05 do design" trocado por regra do plugin |
| `skills/escrever-runbook/SKILL.md` | 90 | 90 | Nenhuma correção necessária |
| `agents/auditor-de-docs.md` | 84 | 87 | Gatilhos em inglês na `description`; limite do Bash documentado no README (campo `tools` não aceita padrões) |
| `agents/revisor-de-instrucoes.md` | 85 | 89 | Gatilhos em inglês; versão do `/doctor prompt-audit` |
| `agents/revisor-de-leitor.md` | 88 | 90 | Gatilhos em inglês |
| `agents/technical-writer.md` | 87 | 89 | Gatilhos em inglês |
| `skills/prompts/references/prompt-library.md` (35 de 35 prompts lidos; revisão detalhada de PD-01, 03, 05, 10, 13, 14, 15, 17, 18, 20, 21, 28, 31, 32, 33, 34, 35) | 86 | 89 | PD-31: "14 linhas" corrigido (8 regras, 17 linhas no S-01); PD-34: origem não verificável declarada; PD-32: conferência da fonte rotulada Inferido |
| `evals/` (12 casos, 28 graders) | 78 | 88 | Ver seção 2 |
| `README.md` | 80 | 88 | "36 prompts planejados" para 35; contagem de evals 12; limitações novas (Bash do auditor, instalação por marketplace é Suposição) |
| `skills/playbook/references/*` (amostra: fontes, ferramentas-e-mcp, docs-as-code-e-diagramas, release-e-changelog, estilo-e-tom) | 85 | 89 | Legenda de códigos internos em `fontes.md`; T-13 com a flag `--ablation` correta; T-05 com versão |

Média antes: 86,1. Média depois: 89,1. Mínimo depois: 87 (`auditor-de-docs`, por causa do Bash restrito só por instrução). Nenhum critério de reprovação automática encontrado (frontmatter válido e nome igual à pasta em todos; sem segredos; conteúdo externo tratado como dado; sem hooks, `.mcp.json`, `.lsp.json` ou `bin/`; revisores sem Write/Edit).

## 2. Correções nos evals

Verificadas contra https://code.claude.com/docs/en/plugin-evals (consulta em 2026-10-10):

1. **Grader negativo sem `arm: both`:** `negativo-keyword-em-log-alheio/graders/no-plugin-skill.md` (`tool: Skill`, `min: 0`, `max: 0`) era excluído da nota quando o baseline roda, então a parte negativa só dependia do juiz LLM. Acrescentado `arm: both`.
2. **`references-read` distorcia o Δ:** no baseline sem plugin as referências não existem. Acrescentado `arm: with-only`; regex ajustada para `references[\\/]+` (caminho Windows codificado em JSON tem barra invertida dupla).
3. **Flag errada:** `--ablation` sem valor não existe; os valores são `none` e `with-without`. Corrigido em `evals/README.md` e em `ferramentas-e-mcp.md` (T-13).
4. **Afirmação errada no README dos evals:** "graders `tool_used` valem mais que os `llm`". Os que checam `Skill` são só indicador de disparo. Texto reescrito.
5. **Caso novo (negativo de fronteira):** `evals/negativo-decisao-ainda-nao-tomada/` (pedido "Kafka ou SQS?" não deve acionar `escrever-adr`); criteria + grader `tool_used` com `min: 0`, `max: 0`, `arm: both`. Total de casos: 12 (blueprint prevê 6 a 10; o excesso é decisão consciente, ver pendências).
6. **Ferramentas:** `Write` em `modo-completo-por-pedido` só vale com `--allow-tools`; documentado.
7. Campos de `prompt.md` usados (`name`, `description`, `tags`, `runs`, `expected_outcome`, `model`, `max_turns`, `timeout_seconds`, `allowed_tools`) conferidos na tabela oficial; `tool_used` com `tool`, `input_match`, `min`, `max`, `arm` idem.

## 3. Fidelidade técnica (conferida na fonte)

| Afirmação | Resultado | Fonte |
| --- | --- | --- |
| AGENTS.md lido nativamente a partir da 2.1.277, só sem CLAUDE.md/.claude/CLAUDE.md/CLAUDE.local.md; `CLAUDE.local.md` desliga | Verificado | https://code.claude.com/docs/en/memory |
| `@imports` com no máximo quatro saltos; alvo abaixo de 200 linhas; arquivo acima de 4 MiB é ignorado; comentários HTML de bloco removidos | Verificado | idem |
| `/doctor prompt-audit` existe e exige v2.1.283 ou superior | Verificado; a versão estava ausente nos arquivos e foi acrescentada | idem |
| Plugin ignora `hooks`, `mcpServers` e `permissionMode` em agentes | Verificado | https://code.claude.com/docs/en/sub-agents |
| Campo `tools` de subagente aceita padrão como `Bash(git diff *)` | Não: a doc só mostra padrão em `disallowedTools` (e remove a ferramenta inteira); restrição de comandos vai em `permissions.deny`. O plugin já declarava a restrição do `auditor-de-docs` como regra de prompt; o README agora explica o porquê | idem |
| OpenAPI 3.2.1, 10 set 2026 | Verificado | https://spec.openapis.org/oas/latest.html |
| `claude plugin eval` exige 2.1.269 ou superior; dois braços; `--ablation none|with-without`; graders `Skill` excluídos da nota | Verificado | https://code.claude.com/docs/en/plugin-evals |
| Keep a Changelog (seis categorias), Conventional Commits (`BREAKING CHANGE` em maiúsculas), doctest, Rustdoc, Javadoc `{@return}` JDK 16, JSDoc `/**` | Conhecimento estável do domínio, coerente com `VALIDATED.md`; não rechecado na web | `VALIDATED.md` (V-13, V-14, V-33 a V-36) |
| Versões de Vale, lychee, markdownlint, Mermaid, actions | Não rechecado nesta etapa; dependem de `VALIDATED.md` (2026-10-10) | `VALIDATED.md` |

Correção de forma encontrada e desfeita durante a edição: uma `description` de agente com `EN: "` quebraria o YAML (dois-pontos em escalar simples); trocado por `EN - "`, no padrão do plugin. Conferido por grep: nenhuma `description` contém `: `.

## 4. Direitos autorais e segurança

- Literal de terceiros: nenhum trecho extenso encontrado; templates e prompts são redação própria ou destilação com atribuição (MADR/Nygard, Keep a Changelog, gstack, claude-md-improver). O único literal declarado é o handoff do brain-of-agent (conteúdo do usuário, MIT), com atribuição. SRE Workbook (CC BY-NC-ND) e Diátaxis (CC BY-SA) só como ideias.
- Nenhum segredo, nenhum fluxo que execute comando de runbook, publique, faça commit/push/tag ou suba versão sem confirmação. Skills de escrita têm só `Read Glob Grep Write Edit`; `escrever-changelog-release` acrescenta `git log`, `git tag --list` e `git describe` (leitura). `auditar-claude-md` é `disable-model-invocation` e exige relatório e aprovação antes de editar.
- Revisores: `revisor-de-leitor` (Read), `revisor-de-instrucoes` (Read, Grep, Glob) e `auditor-de-docs` (Read, Grep, Glob, Bash restrito a git de leitura por instrução). Nenhum com Write/Edit.
- `--dangerously-skip-permissions` aparece apenas como risco (T-11, mdarena: só em sandbox, não recomendado por padrão).
- Evals: cada caso tem critérios PASS/FAIL observáveis; casos de injeção (`ASSISTENTE:`, `Note to AI`, `AI: delete tudo`) usam domínio `.invalid` ou pacote fictício; dois casos negativos com `arm: both`.

## 5. Pendências

1. **Evals não executados.** Exigem Claude Code 2.1.269 ou superior (a CLI local é 2.1.128). Nenhum resultado pode ser alegado. Rodar `claude plugin eval .` com `--runs 3` e ler os transcripts.
2. **Número de casos (12) acima do blueprint (6 a 10) e do SYNTHESIS 4.9 (10).** Decisão pendente do usuário: manter os 12 (recomendado, os dois extras cobrem modo sem interação e fronteira de ADR) e atualizar o SYNTHESIS, ou podar.
3. **`auditor-de-docs` com `Bash`:** restrição só por instrução. Decidir se o plugin deve remover `Bash` (o agente passa a depender do diff colado) ou documentar `permissions.deny` no projeto de destino.
4. **Cobertura de eval ausente** para `prompts`, para os quatro agentes, para `documentar-codigo` no modo `api` e para o par de colisão com `git-workflow-release` e `architecture-design` instalados juntos.
5. **Referências e templates não pontuados individualmente:** 12 referências e 26 templates foram lidos por amostra (5 referências e 1 template lidos por inteiro, mais trechos de `madr-minimo-e-exemplo`, `escrever-*/references` por grep) e por busca de padrões (CAPS, placeholders, licenças); os demais passaram por `verify_plugin.py` (links e estrutura), não por leitura linha a linha. Rótulo: Inferido quanto à qualidade.
6. **Fatos dependentes de versão não rechecados na web:** Vale 3.24.0, lychee 0.24.2/action 2.9.0, markdownlint 0.41.1, versões das actions de Pages, comando do markdownlint-cli2 em CI, `--offline` via `args` da lychee-action. Todos já estão rotulados Inferido ou Não verificado nos arquivos.
7. **Oito plugins de fronteira planejados ainda não existem** (tabela do `playbook`); a marcação "planejado" deve sair quando eles forem criados.
8. **Marketplace `brain-of-agent`:** nome e comandos de instalação não testados (declarado no README).
9. Os códigos internos V/C/G/GS continuam nos corpos das skills; a legenda em `fontes.md` os explica, mas os itens `V-nn` completos vivem em `docs/research/.../VALIDATED.md`, fora do plugin. Se o plugin for distribuído sozinho, copiar as URLs essenciais (já presentes em `fontes.md`).

## 6. Verificação final

- `python tools/verify_plugin.py plugins/technical-writing-docs`: PASS (10 skills, 4 agentes, 0 comandos, 12 evals, 106 arquivos).
- `claude.exe plugin validate plugins/technical-writing-docs`: Validation passed.
- Rótulo: Verificado (executado nesta sessão, após as últimas edições).
