# BUILD-REPORT-quality: product-discovery-specs

Data: 2026-10-10 · Validador: Claude Opus 5.5, em contexto de validação de prompt, com a rubrica `docs/foundation/prompt-quality-rubric.md` (D1–D12, 0–100).
Independência: os construtores eram outro modelo, mas da mesma família (Anthropic). A revisão é parcialmente independente; as notas são julgamento por leitura, não medição. Nenhum eval foi executado.

## Escopo lido

- 10 `SKILL.md` (inteiros), 5 agentes (inteiros), `README.md`, `plugin.json`, `evals/README.md` e os 16 casos originais (prompt e todos os graders).
- Biblioteca de prompts: índice e convenções inteiros; amostra pontuada em detalhe com 12 prompts: P-01, P-09, P-10, P-11, P-20, P-24, P-29, P-33, P-35, P-38, P-42 e P-43. Os outros 28 foram lidos só pelo índice e por Grep.
- Referências por leitura integral ou Grep: `ferramentas-e-mcp.md`, `checklist-completo.md`, `fontes.md` (licenças), `frameworks-e-formulas.md` (ICE, Kano), `formatos-e-exemplo-resolvido.md` (EARS, Gherkin).
- `VALIDATED.md` por Grep (V-06, V-07, V-15, V-16, V-21, V-27, V-33, V-43, V-44).
- `BUILD-REPORT-structural.md` deste segmento **não existe** em `docs/research/product-discovery-specs/` em 2026-10-10; não houve pendências estruturais a herdar (ver Pendências).

## Fidelidade técnica conferida em fonte (2026-10-10)

| Afirmação no plugin | Fonte aberta | Resultado |
| --- | --- | --- |
| Caso negativo `mudanca-trivial-negativo` com `tool_used` de `Skill`, `min: 0`, `max: 0` mede sobredisparo | https://code.claude.com/docs/en/plugin-evals | **Incompleto.** Em execução de dois braços (o padrão), todo `tool_used` com `tool: Skill` sai do score; a doc recomenda `arm: both` para "não deve invocar a skill". Sem isso, o sobredisparo não pontuaria. Corrigido. |
| "Os graders `no-write` e `no-injected-command` só fazem sentido porque o caso lista `Write` e `Bash` em `allowed_tools`" (evals/README) | mesma página, "Grant tools" | **Errado.** `allowed_tools` só concede ferramentas somente leitura; `Write`, `Edit`, `Bash`, `WebFetch`, `WebSearch` exigem `--allow-tools`. Sem a concessão, esses graders passam trivialmente. README corrigido; casos marcados com a tag `needs-write-grant` e comando `--tag needs-write-grant --allow-tools Write Bash`; aviso de que `Bash` exige sandbox (WSL2/Linux). |
| `claude plugin eval . --ablation` compara com baseline | mesma página, tabela de opções | **Errado.** `--ablation` recebe modo (`none` ou `with-without`); o padrão já roda os dois braços. Corrigido. |
| Campos de grader além de `type/tool/input_match/min/max` "não verificados" | mesma página, "Grader types" | Conferidos (`regex`: `pattern/flags/match/target`; `llm`: corpo do `.md` é o critério, 2 de 3 votos; `arm`: `with-only`/`both`). Rótulo passou a Verificado. |
| Grader `references-read` (Read de referências, `min: 10`) | mesma página, "Score against the no-plugin baseline" | Não é `Skill`, então seria pontuado no braço sem plugin, onde nunca passa, inflando o `Δ`. Recebeu `arm: with-only`; o padrão do caminho passou a aceitar barra invertida escapada em JSON (`references[\\/]+`). Testado com Node. |
| Casos de agente sem a ferramenta de delegação | mesma página | `Agent` está na lista de somente leitura concedíveis (Verificado); `revisao-spec-adversarial` e `decisao-produto-sem-decisor` não a listavam, então o agente principal nem podia delegar ao `spec-reviewer`/`decision-recorder`. `Agent` acrescentado e grader indicador `agent-dispatched` (`arm: with-only`). O nome do campo da entrada da chamada não foi conferido (Inferido): o padrão casa só o nome do agente. |
| Requisito 2.1.269; `runs` padrão 3; `name`, `expected_outcome`, `model`, `timeout_seconds`, `max_turns` aceitos no `prompt.md` | mesma página | Confirmado. CLI local: `claude --version` = 2.1.128 (abaixo do requisito). |
| Hook `Stop`: código de saída 2 e `stop_hook_active` (estava Inferido) | https://code.claude.com/docs/en/hooks | **Confirmado**: `Stop` sem matcher; saída 2 impede o encerramento; `stop_hook_active` é verdadeiro quando o Claude Code já continua por causa de um Stop hook. Rótulo atualizado em `ferramentas-e-mcp.md`. |
| `Bash(gh issue create:*)` em `permissions.ask` ("sintaxe mudou entre versões") | https://code.claude.com/docs/en/permissions | **Confirmado**: `:*` equivale a ` *` no fim do padrão e só vale no fim. Rótulo atualizado. |
| A/B: n ≈ 16·σ²/δ²; 10 espiadas a 1% nominal ≈ 5% real; 24.576 por braço | `VALIDATED.md` V-27 e cálculo | Coerente: 16 × 0,0384 / 0,000025 = 24.576. |
| Multiagente ≈ 15× tokens (V-07); OKR "cerca de três" KRs, 0,6–0,7 (V-43); Background "mais de 4 linhas" (V-16); tarefas ≤ 1 dia (V-44); roteiro JTBD 30 min (V-33); escala RICE (V-21) | `VALIDATED.md` | Coerentes com o validado. |
| Gherkin em português (`# language: pt`, `Funcionalidade`, `Regra`, `Esquema do Cenário`, `Dado/Quando/Então/E/Mas`) | conhecimento estável do domínio | Coerente; mantido com remissão à referência do Cucumber. |

## Notas por artefato

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 88 | 88 | Sem mudança: papel, princípios com porquê, escada N0–N4, gates, rótulos, modo `PRODUTO-COMPLETO` e fronteiras completos. |
| `skills/prompts/SKILL.md` | 86 | 86 | Sem mudança (índice claro, leitura por Grep da seção, "não afirme eficácia"). |
| `skills/spec-interview/SKILL.md` | 88 | 88 | Sem mudança; exemplo de rodada e tabela "o que conta como aprovação" fortes. |
| `skills/write-prd/SKILL.md` | 87 | 87 | Sem mudança. |
| `skills/write-spec/SKILL.md` | 87 | 87 | Sem mudança. |
| `skills/acceptance-criteria/SKILL.md` | 88 | 88 | Sem mudança. |
| `skills/refine-backlog/SKILL.md` | 85 | 85 | Sem mudança (V-44 conferido: tarefas ≤ 1 dia, três perguntas). |
| `skills/prioritize-roadmap/SKILL.md` | 86 | 86 | Sem mudança no corpo; P-20 alinhado ao limiar de empate de 15% da skill. |
| `skills/run-discovery/SKILL.md` | 86 | 86 | Sem mudança no corpo; o modo `synthesis` ganhou caso de eval próprio. |
| `skills/spec-to-tasks/SKILL.md` | 84 | 86 | D10: "JÁ APROVADA" em maiúsculas na `description` virou "já aprovada pelo humano (gate G1)". |
| `agents/spec-reviewer.md` | 89 | 89 | Sem mudança; somente leitura (`Read, Grep, Glob`), limiar de confiança, "sem lacunas" válido. |
| `agents/plan-writer.md` | 86 | 86 | Sem mudança; `Write` limitado por instrução ao caminho pedido (guardrail, não fronteira). |
| `agents/decision-recorder.md` | 87 | 87 | Sem mudança; não escolhe a opção pelo humano, `Proposed` em lote. |
| `agents/discovery-synthesizer.md` | 88 | 88 | Sem mudança; somente leitura, citação conferida por Grep. |
| `agents/feasibility-scout.md` | 87 | 87 | Sem mudança; somente leitura. |
| Biblioteca de prompts (amostra de 12) | 86 | 88 | P-01: play back de "3 a 6 linhas" contradizia skill e V-15 (200 a 300 palavras); alinhado. P-20: sensibilidade "menos de 10%" contradizia a skill (15%, Suposição); alinhado. |
| `evals/` (17 casos + README) | 66 | 86 | D12/D7: `arm: both` no negativo; `arm: with-only` e regex robusta em `references-read`; `Agent` em `allowed_tools` e graders `agent-dispatched` nos casos de agente; graders determinísticos `scores` (RICE) e `sample-size` (A/B), testados com Node; novo caso `sintese-sem-notas` (fabricação sem notas, com regex `no-quotes` de ausência); tag `needs-write-grant`; README reescrito em "Como rodar/interpretar" com concessão de ferramentas, sandbox, `--ablation none`, custo de dois braços e `--judge-model`. |
| `README.md` (plugin) | 84 | 86 | `plan-writer` e `decision-recorder` descritos como "escreve só em `plans/`/`docs/decisions/`", mas os agentes gravam só no caminho pedido e, sem ele, devolvem o texto; corrigido. |
| `skills/playbook/references/ferramentas-e-mcp.md` | 83 | 87 | Hook `Stop` e sintaxe `:*` passaram de Inferido a Verificado com URL e data; o script de exemplo continua Inferido e não executado. |
| `skills/playbook/references/checklist-completo.md` | 86 | 87 | SK-05: regra de `arm: both` e de `--allow-tools` no `claude plugin eval`. |

Média antes: 85,3 · média depois: 86,9 · mínimo depois: 85. Nenhum artefato abaixo de 80; nenhum critério de reprovação automática encontrado.

## Direitos autorais e segurança

- Literal só de conteúdo próprio do usuário (brain-of-agent, MIT) e marcado "Modo L" com atribuição (P-11, P-12, P-41, P-43). Terceiros MIT/Apache-2.0 (spec-kit, superpowers, awesome-copilot, phuryn, ralph, gstack, code-modernization, product-on-purpose) só destilados, com atribuição em `fontes.md` e no README. Shape Up (© 37signals) e Scrum Guide (licença Não verificável) apenas destilados. `deanpeters/Product-Manager-Skills` (CC BY-NC-SA) declarado como não usado.
- Sem segredos. Nenhum hook, `.mcp.json`, `.lsp.json` ou `bin/` ativo; exemplos de hook, permissão e MCP estão só em `references/`, com risco e rótulo.
- `--dangerously-skip-permissions` aparece apenas como risco ("só em sandbox isolado e repositório confiável, nunca como padrão") em 5 lugares; nenhum fluxo o recomenda.
- Ações externas (issue, comentário, roadmap publicado) exigem confirmação do texto exato em playbook, skills e prompts; `spec-to-tasks` tem `disable-model-invocation: true` e só imprime comandos de tracker.
- Revisores e exploradores (`spec-reviewer`, `feasibility-scout`, `discovery-synthesizer`) sem Write/Edit/Bash. `plan-writer` e `decision-recorder` têm `Write`, restrito por instrução ao caminho pedido, com checagem de sobrescrita.
- Evals: todos os `llm` têm PASS if / FAIL if observáveis; há caso negativo (`mudanca-trivial-negativo`, agora pontuado com `arm: both`) e caso de injeção com keyword e comando dentro de documento colado.

## Pendências

1. `BUILD-REPORT-structural.md` deste segmento não existe; se o validador estrutural rodar depois, cruzar as pendências dele com este relatório.
2. Evals `designed_not_executed`: a CLI local é 2.1.128 e `claude plugin eval` exige 2.1.269. Rodar em WSL2/Linux, primeiro `--ablation none` para ajustar graders, depois a suíte padrão e `--tag needs-write-grant --allow-tools Write Bash`.
3. Nome do campo da entrada da ferramenta `Agent` (Inferido); o `agent-dispatched` casa só o nome do agente. Conferir no primeiro transcript.
4. Sem caso próprio: `spec-to-tasks` (manual), `plan-writer`, `feasibility-scout`; `write-spec` modo `update`; OKR para avaliar pessoas. Menos de 3 casos por skill.
5. Juiz LLM da mesma família por padrão; usar `--judge-model` com modelo diferente e calibrar contra leitura humana.
6. 28 dos 40 prompts não foram pontuados individualmente (lidos por índice e Grep).
7. Lacunas de evidência herdadas de `VALIDATED.md` (JTBD sem fonte primária, OEC/SRM, North Star/HEART/AARRR, roadmap com fonte única) seguem declaradas no README; não são corrigíveis por edição.

## Verificação final

- `python tools/verify_plugin.py plugins/product-discovery-specs` → `RESULT: PASS` (skills 10, agents 5, evals 17, files 130).
- `claude plugin validate plugins/product-discovery-specs` → `Validation passed`.
- Regex dos graders novos e alterados testadas com Node (`scores`, `sample-size`, `references-read` com caminho Windows escapado e POSIX): todas casam o esperado e rejeitam o contraexemplo.
