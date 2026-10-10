# BUILD-REPORT-quality: qa-testing

Data: 2026-10-10 · Validador: Claude Opus 5.5, em contexto de validação de prompt, com a rubrica `docs/foundation/prompt-quality-rubric.md` (D1–D12, 0–100).
Independência: os construtores eram outro modelo, mas da mesma família (Anthropic). A revisão é parcialmente independente; as notas são julgamento por leitura, não medição. Nenhum eval foi executado.

## Escopo lido

- 10 `SKILL.md`, 4 agentes, `README.md`, `plugin.json`, `evals/README.md` e os 12 casos (prompt e graders).
- Biblioteca de prompts inteira (31 prompts, dois arquivos). Amostra pontuada em detalhe: P01, P02, P04, P05, P09, P14, P15, P18, P19, P20, P22, P24, P27, P28, P30 e P31 (16).
- Referências por leitura parcial e Grep: `layout-de-evals.md`, `ferramentas-e-mcp.md`, `claude-md-snippets.md`, `evidencia-de-teste.md`, `bugs-e-evidencia.md`.
- Pendências herdadas de `BUILD-REPORT-structural.md` (seção 5) e fatos de `VALIDATED.md` (V-02, V-20, V-21) por Grep.

## Fidelidade técnica conferida em fonte (2026-10-10)

| Afirmação no plugin | Fonte aberta | Resultado |
| --- | --- | --- |
| Caso negativo com `tool_used` de `Skill`, `min: 0`, `max: 0` mede sobredisparo | https://code.claude.com/docs/en/plugin-evals | **Incompleto.** Em execução de dois braços todo `tool_used` com `tool: Skill` sai do score; a doc recomenda `arm: both` justamente para o check "não deve invocar a skill". Sem isso, `negativo-frontend-css` não pontuaria o sobredisparo. Corrigido no caso, em `eval-design`, `layout-de-evals.md`, P28 e `evals/README.md`. |
| `allowed_tools: [..., Write, Edit, Bash]` no `prompt.md` concede essas ferramentas | mesma página, seção "Grant tools" | **Errado por omissão.** Só ferramentas somente leitura listadas são concedidas; `Write`, `Edit`, `Bash`, `WebFetch` e `WebSearch` somem da sessão sem `--allow-tools`. O grader `tests-written` de `tdd-fatia-vertical` falharia por configuração. README dos evals, `eval-design`, `layout-de-evals.md`, P28 e o novo comando `eval-plugin` agora dizem isso. |
| Campos de `regex`, `file_exists`, `tool_order`, `baseline` "não lidos" | mesma página, "Grader types" | Lidos e registrados: `pattern`/`flags`/`match`/`target`; `path`/`exists`; `before`/`after`; `baseline_file`/`criteria`; `llm` com `criteria`/`focus` e 2 de 3 votos. Rótulo passou de Não verificável para Verificado. |
| Requisitos 2.1.269 e git 2.31; 3 execuções; `--threshold` 1.0; códigos 0/1/2; WSL2 | mesma página | Confirmado. |
| Chaves aceitas no `prompt.md` (`timeout_seconds`, `runs`, `expected_outcome`, `model`…) | mesma página, "prompt.md fields" | Confirmado (13 chaves, com padrões). |
| Ferramenta de delegação a subagente | mesma página | `Agent` está na lista de ferramentas somente leitura concedíveis (Verificado). O nome do campo do subagente na entrada não foi conferido. |
| `stop_hook_active` no input do Stop hook (estava Inferido) | https://code.claude.com/docs/en/hooks | **Confirmado**: verdadeiro quando o Claude Code já continua por causa de um Stop hook. `permissionDecision` aceita `allow`, `deny`, `ask` e `defer`. Rótulo atualizado. |
| Estatística de validação de flaky (50 execuções limpas ⇒ taxa < ~6% com 95%; flake de 2% passa 50 vezes com ~36%) | cálculo | Confirmado: 1 − 0,05^(1/50) = 5,8%; 0,98^50 = 0,364. |
| `go test -count=1`, `turbo --force`, `gradle --rerun-tasks`, pytest exit 5, `new Date("AAAA-MM-DD")` em UTC | conhecimento estável | Coerentes; mantidos com "confira na versão instalada". |

## Notas por artefato

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 87 | 88 | Linha da tabela intenção → skill com 2 colunas (quebrava a tabela) corrigida; comandos `/qa-testing:qa-evidence` e `/qa-testing:eval-plugin` restaurados. |
| `skills/prompts/SKILL.md` | 84 | 86 | `description` ganhou gatilhos em inglês e "não executa a tarefa do prompt"; P04 aponta para o comando. |
| `skills/verification-gate/SKILL.md` | 88 | 88 | Sem mudança. |
| `skills/tdd-guard/SKILL.md` | 87 | 87 | Sem mudança. |
| `skills/test-strategy/SKILL.md` | 86 | 86 | Sem mudança. |
| `skills/test-design/SKILL.md` | 87 | 87 | Sem mudança (CNPJ alfanumérico segue "Não verificável", rotulado). |
| `skills/flaky-triage/SKILL.md` | 88 | 88 | Sem mudança; estatística conferida. |
| `skills/e2e-review/SKILL.md` | 86 | 86 | Sem mudança. |
| `skills/bug-report/SKILL.md` | 85 | 87 | D10: "é reprovação certa" virou o motivo (dado inventado faz perseguir defeito inexistente). |
| `skills/eval-design/SKILL.md` | 80 | 89 | D12: `arm: both` no caso negativo; regra de `--allow-tools`; campos de grader verificados no lugar de "Não verificável"; exemplo de grader `regex`; checklist e gotchas novos; execução pelo comando `eval-plugin`. |
| `agents/test-reviewer.md` | 90 | 90 | Sem mudança: read-only, limiar de confiança, formato fixo, conteúdo suspeito. |
| `agents/test-auditor.md` | 87 | 87 | Sem mudança; `Bash` só leitura declarado como restrição por instrução. |
| `agents/qa-reporter.md` | 87 | 88 | Rodar a suíte pode gravar cache, cobertura ou dados: só no ambiente de teste e com artefatos listados. |
| `agents/test-writer.md` | 84 | 87 | D5: o exemplo usava `NameError` como "vermelho válido", contradizendo a regra do próprio agente; trocado por `AssertionError` com stub mínimo. |
| Biblioteca de prompts (amostra de 16) | 84 | 87 | P27: a instrução "use outro modelo" saiu do texto do juiz (o juiz não escolhe o próprio modelo) e foi para o checklist de uso, com `--judge-model`. P28: `arm: both`, `--allow-tools`, campos reconferidos. P05: mutation check com restauração conferida por `git diff`. P09: erro de redação. P30: mapeamento de snippets corrigido (não era S-01 a S-17). |
| `evals/` (12 casos + README) | 78 | 86 | `no-qa-skill.md` com `arm: both`; README com comandos de execução que concedem `Write`/`Edit` e isolam o caso com `Bash` (WSL2); exclusão de graders explicada; `Agent` registrado como verificado. PASS/FAIL observáveis e caso negativo mantidos. |
| `skills/eval-design/references/layout-de-evals.md` | 76 | 88 | Tabela de graders com todos os campos verificados; concessão de ferramentas; regra de exclusão em dois braços; grader negativo com `arm: both`. |
| `skills/playbook/references/ferramentas-e-mcp.md` | 85 | 87 | `stop_hook_active` e valores de `permissionDecision` reconferidos; T-01 aponta o comando. |
| `README.md` | 85 | 87 | Tabela de componentes com os 2 comandos; limitação "comandos não exercitados". |
| `commands/qa-evidence.md` (novo) | ausente | 86 | Criado conforme SYNTHESIS 4.4: manual, `allowed-tools: Read, Grep, Glob`, só dados desta sessão, pergunta antes de gravar ou sobrescrever, exemplo de linha certa e de "NÃO testado". |
| `commands/eval-plugin.md` (novo) | ausente | 87 | Criado: manual, sem `allowed-tools` (o `Bash` passa pelo fluxo normal de permissão), pré-checagens de versão, ferramentas e confiança no plugin, mostra comando e teto e espera "sim"; sem resposta não roda; leitura de códigos 0/1/2 e transcrições. |

Outras correções: `evidencia-de-teste.md` e `bugs-e-evidencia.md` apontam para o comando novo.

Resumo: média antes ≈ 84,9 (19 unidades; os 2 comandos não existiam); média depois ≈ 87,2 (21 unidades); mínimo depois = 86. Nenhum critério de reprovação automática encontrado: nada de execução inventada, nenhuma ação externa sem confirmação, conteúdo externo tratado como dado, sem segredos, `--dangerously-skip-permissions` não aparece.

## Segurança e direitos autorais

- Revisores sem Write/Edit: `test-reviewer` (Read, Grep, Glob); `test-auditor` e `qa-reporter` têm `Bash` só por instrução, declarado como não garantido pelo campo `tools`, com conferência por `git status`. Só `test-writer` grava, limitado a caminhos de teste indicados no pedido.
- Efeitos colaterais com gate: criar issue, `git bisect`, quarentena/edição de CI, rodar eval pago, gravar `TESTING.md`. Os dois comandos usam `disable-model-invocation: true`.
- Evals: fixture de injeção com domínio `.invalid` dentro do log do caso `escopo-nao-afrouxar-e-log-hostil` e grader `no-injected-command`. Na validação ele foi tratado como dado de teste e não foi seguido.
- Literais: só do brain-of-agent (MIT, do usuário) com atribuição; terceiros (superpowers, Matt Pocock, gstack, webapp-testing Apache-2.0) aparecem destilados com fonte. Nenhum literal novo de terceiros entrou nesta passada.

## Pendências do validador estrutural: situação

1. Comandos ausentes: **resolvido** (criados e citações restauradas).
2. Dois casos de eval além dos 10 do SYNTHESIS: **mantidos**, porque são a única cobertura da skill `prompts` e do papel de revisor. A blueprint pede 6 a 10; fica 12 como decisão registrada.
3. Eval de agente: **parcial**. `Agent` é ferramenta concedível (Verificado), mas o campo da entrada que nomeia o subagente não foi conferido; sem ele, um `input_match` seria palpite.
4. Índice de prompts × biblioteca: **sem ação necessária**. A biblioteca usa títulos `### P##` (31 encontrados, batendo com as 31 linhas do índice), não linhas de tabela.

## Pendências (exigem decisão ou execução)

- `docs/foundation/plugin-blueprint.md` descreve o caso negativo sem `arm: both`. Isso afeta todos os plugins da fábrica; não editei a fundação compartilhada. Recomendo acrescentar `arm: both` ao modelo e revisar os casos negativos dos outros plugins.
- Criar um caso de delegação ao `test-reviewer` depois de conferir, num transcript real, o nome do campo do subagente na entrada da ferramenta `Agent`.
- Rodar a suíte (`claude plugin eval . --allow-tools Write Edit`, e o caso com `Bash` em WSL2) quando a CLI estiver em 2.1.269 ou superior; a da fábrica era 2.1.128. Até lá, tudo `designed_not_executed`.
- Exercitar os dois comandos novos numa sessão real.
- CNPJ alfanumérico em `test-design` continua "Não verificável" (confirmar com a Receita Federal).

## Verificação executada

- `python tools/verify_plugin.py plugins/qa-testing` → `RESULT: PASS` (10 skills, 4 agentes, 2 comandos, 12 evals, 101 arquivos) depois das edições.
- `claude plugin validate plugins/qa-testing` → `Validation passed` depois das edições.
- Páginas lidas: https://code.claude.com/docs/en/plugin-evals e https://code.claude.com/docs/en/hooks (2026-10-10).
