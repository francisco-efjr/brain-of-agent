# ux-ui-design: relatório de validação de qualidade de prompt

Data: 2026-10-10 · Plugin: `plugins/ux-ui-design` · Papel: validador de qualidade de prompt e conteúdo técnico (rubrica `docs/foundation/prompt-quality-rubric.md`, D1 a D12, nota 0 a 100).

Independência: este validador é um modelo Claude, da mesma família dos construtores. A revisão é adversarial, mas não é validação externa. As notas são leitura de modelo, não medição. Nenhum eval foi executado.

## 1. Escopo e método

- Lidos por inteiro: os 10 `SKILL.md`, os 5 agentes, o `README.md`, o manifesto, o `evals/README.md`, os 12 `prompt.md` e os 35 graders.
- Biblioteca de prompts: 18 dos 37 prompts lidos por inteiro (PR-01, 02, 03, 04, 09, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 29, 32, 35), além dos sumários dos três arquivos.
- Referências conferidas por `Grep` e leitura parcial: `fontes.md`, `ferramentas-e-mcp.md`, `decisoes-e-tradeoffs.md`, `tokens-3-camadas.md`, `esqueleto-design-md.md`, `esqueleto-dtcg.md`.
- Fidelidade técnica:
  - Todas as razões de contraste citadas no plugin foram recalculadas com a fórmula WCAG por script. Foram 22 pares distintos, entre eles 4,48, 4,54, 2,85, 17,09, 14,35, 6,42, 1,46, 9,82, 5,47, 15,12, 5,02, 6,57, 4,97, 2,58, 1,47, 2,72, 2,17, 7,80, 6,11, 5,13 e 6,39. Nenhuma divergência (Verificado).
  - WCAG 2.2: 86 critérios, Recommendation de 2024-12-12, e 2.4.12, 2.4.13 e 2.5.5 no nível AAA. Conferido contra VALIDATED.
  - Apple HIG: 44×44 pt padrão e 28×28 pt mínimo. Conferido contra V-39.
  - DTCG 2025.10 e o limiar de CLS: reconferidos nas fontes oficiais por WebFetch (ver seção 3).

## 2. Notas antes e depois

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 92 | 92 | Nenhuma. Router, proporcionalidade, modo `UXUI-COMPLETO` com ativação só pelo usuário, fronteira de ações e Gotchas declaradas como previstas |
| `skills/prompts/SKILL.md` | 89 | 90 | Gotcha do CLS atualizada para "conferido em web.dev em 2026-10-10" |
| `skills/design-brief/SKILL.md` | 88 | 89 | "Armadilhas comuns" virou `## Gotchas`, com a declaração "previstas, não observadas" (C-17) |
| `skills/ui-audit/SKILL.md` | 89 | 90 | Idem |
| `skills/heuristic-eval/SKILL.md` | 89 | 90 | Idem |
| `skills/a11y-checklist/SKILL.md` | 90 | 91 | Idem |
| `skills/ux-writing/SKILL.md` | 87 | 88 | Idem |
| `skills/design-tokens/SKILL.md` | 88 | 89 | Idem. O conteúdo técnico sobre `$schema` já estava correto e foi confirmado na spec |
| `skills/user-research-plan/SKILL.md` | 88 | 89 | Idem |
| `skills/design-init/SKILL.md` | 89 | 90 | Idem |
| `agents/design-evaluator.md` | 88 | 88 | Nenhuma. Calibração A, B e C presente e rotulada Suposição; Gotchas previstas |
| `agents/ui-designer.md` | 87 | 87 | Nenhuma. Write e Edit só em caminho indicado pelo pedido; sem Bash |
| `agents/a11y-reviewer.md` | 90 | 90 | Nenhuma |
| `agents/ux-researcher.md` | 88 | 88 | Nenhuma |
| `agents/design-system-auditor.md` | 82 | 88 | Corrigido o erro D12. O agente mandava fixar a versão "no `$schema` ou em comentário", o que contradiz a skill `design-tokens` e a spec 2025.10 (que não define `$schema`) e não funciona em JSON (que não aceita comentário). Agora a versão vai no nome do arquivo, em `$description` de grupo ou na configuração do build |
| Biblioteca de prompts (amostra de 18) | 86 | 88 | PR-32: retirados `$schema` e comentário. Incluída a estrutura de `dimension`, `duration` e `color`, conferida na spec. A nota "sintaxe não verificada" virou "conferida; tipos compostos e modos não". PR-23: limiar de CLS conferido (bom até 0,1, ruim acima de 0,25, percentil 75, móvel e desktop) |
| Evals (12 casos, 35 graders) | 88 | 88 | Nenhuma. Os casos têm critérios PASS/FAIL observáveis, dois negativos (`negativo-css-grid`, `fronteira-implementar-react`), um caso de injeção e keyword, graders `tool_used` com `max: 0` para Write, Edit e Bash, e o status `designed_not_executed` |
| `README.md` | 85 | 87 | "Cinco grupos A a E" foi trocado pelos cinco temas, porque a skill usa A, B e C para os arquivos. A limitação de DTCG agora diz o que foi conferido e o que não foi |

Média antes: 87,9. Média depois: 89,0. Mínimo depois: 87. Nenhum arquivo ficou abaixo de 80, e nenhum critério de reprovação automática foi encontrado.

## 3. Correções de fidelidade técnica e de consistência

1. **`$schema` no DTCG (D12).** WebFetch da spec 2025.10, primeiros 100 mil de 113 mil caracteres:
   - não há propriedade `$schema`;
   - JSON Schema só aparece como nota do editor ("o grupo está explorando") e na analogia de `$extends` e `$ref`.

   VALIDATED (V-20) recomendava "fixar a versão no `$schema`", e quatro arquivos repetiam isso. Arquivos corrigidos:
   - `agents/design-system-auditor.md`;
   - `skills/playbook/references/decisoes-e-tradeoffs.md` (C8);
   - `skills/prompts/references/prompts-design-system.md` (PR-32);
   - `skills/playbook/assets/templates/tokens-3-camadas.md`. Este template também mandava usar "a URL publicada pela versão 2025.10", que não existe.

   O template passou a rotular a estrutura de `color`, `dimension` e `duration` como Verificado, e não mais Inferido. Tipos compostos e modos continuam Não verificado. Registro em `fontes.md`, linha V-20 de reconferência.
2. **Limiar de CLS.** O web.dev dá bom ≤ 0,1 e ruim > 0,25, no percentil 75, por móvel e desktop (página atualizada em 2023-04-12, consultada em 2026-10-10). O rótulo passou de Inferido para conferido em PR-23 e na skill `prompts`. Nova linha Q-01 em `fontes.md`.
3. **Comando sem versão.** `ferramentas-e-mcp.md` recomendava `npx storybook add @storybook/addon-a11y` sem versão, contra a regra do próprio arquivo (nunca `npx` sem versão). Agora o comando é `npx storybook@<VERSAO_FIXADA> add ...`, igual ao Storybook instalado e só por pedido do usuário.
4. **Gotchas nas skills de tarefa (C-17, P-33).** As 8 skills de tarefa tinham "Armadilhas comuns" sem dizer que eram previstas. Agora têm `## Gotchas` com a declaração explícita, coerente com o `playbook`, os agentes e o SYNTHESIS (seção de convenções).

## 4. Segurança e direitos autorais

- Nenhuma ocorrência de `--dangerously-skip-permissions`, bypass de permissões, CAPS de ênfase, segredo ou placeholder `TODO`. Conferido por `Grep`.
- Revisores somente leitura: `design-evaluator`, `a11y-reviewer`, `ux-researcher` e `design-system-auditor` têm `tools: Read, Grep, Glob`.
- `ui-designer` tem Write e Edit, conforme previsto no SYNTHESIS. Só escreve em caminho que o pedido indicar, nunca em arquivo gerado, em `tokens.json` de marca ou em `CLAUDE.md`, e não tem Bash.
- Nenhuma skill lista Bash, Write ou Edit em `allowed-tools`.
- `design-init` usa `disable-model-invocation: true` e exige duas confirmações literais: uma para o DESIGN.md e outra para o CLAUDE.md.
- `design-tokens` só edita depois que a lista de nomes é confirmada.
- Conteúdo externo é tratado como dado em todas as skills e agentes. O eval `escopo-injecao-e-keyword` mede isso.
- Direitos autorais: NN/g, W3C, Apple, web.dev e a documentação da Anthropic aparecem só destilados. Fontes MIT e Apache-2.0 têm atribuição em `fontes.md`, no README e no fim de cada skill. Não encontrei trecho literal longo de terceiros nos arquivos lidos.

## 5. Pendências (dependem do dono do plugin ou de execução)

1. **Evals não executados.** A CLI local é a 2.1.128, abaixo da 2.1.269 exigida por `claude plugin eval`. Os 12 casos continuam `designed_not_executed`, e nenhuma taxa pode ser alegada. Depois de executar, calibre os graders `llm` com leitura humana.
2. **Calibração do `design-evaluator`.** Os cenários A, B e C existem, mas são sintéticos e não foram calibrados por humano (Suposição). Faltam testes contra julgamento de especialista.
3. **Gotchas reais.** Todas as listas são "previstas". Substitua por falhas observadas, com data e origem, depois das primeiras execuções.
4. **Árvore de prompts.** Mantive os três arquivos atuais no lugar dos cinco previstos no SYNTHESIS. Todo o conteúdo está presente (PR-01 a PR-37), e a skill `prompts` lê por `Grep` em `## PR-nn`, sem carregar o arquivo inteiro. Voltar aos cinco arquivos é decisão do dono, sem ganho funcional demonstrado.
5. **VALIDATED.md (V-20)** ainda diz "fixar a versão 2025.10 no `$schema`". O documento de pesquisa não foi editado, por estar fora do plugin. Recomenda-se anotar a correção ali.
6. **Lacunas declaradas que seguem abertas:** Material 3 e o alvo de 48 dp, motion, tipografia e grid, Figma Dev Mode e MCP, guia de voz PT-BR, i18n e RTL, e tamanhos de amostra de card sorting e tree testing.
7. **Trecho final da spec DTCG.** Os 13 mil caracteres finais da spec 2025.10 não foram lidos por nenhum validador. Tipos compostos e modos seguem Não verificado.

## 6. Verificação final

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Verificador da fábrica | `python tools/verify_plugin.py plugins/ux-ui-design` | RESULT: PASS (10 skills, 5 agentes, 12 evals, 114 arquivos) |
| Validador oficial | `claude plugin validate plugins/ux-ui-design` | Validation passed |
| Contraste | script com a fórmula WCAG sobre os 22 pares distintos citados | sem divergência |
