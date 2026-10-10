# BUILD-REPORT: web-frontend

Data: 2026-10-10. Papel: gate final do plugin `plugins/web-frontend`. Consolida `BUILD-REPORT-structural.md` e `BUILD-REPORT-quality.md` nesta pasta.

## 1. Resultado

| Critério | Resultado | Rótulo |
| --- | --- | --- |
| Verificador do projeto (`tools/verify_plugin.py`) sem ERROS | `RESULT: PASS` | Verificado |
| Validador oficial (`claude plugin validate`) | `Validation passed` | Verificado |
| Correções nesta rodada | Nenhuma. Ambos passaram sem alteração de arquivos do plugin | Verificado |

Pass: sim.

## 2. Contagem de componentes

| Componente | Quantidade | Detalhe | Rótulo |
| --- | --- | --- | --- |
| Skills | 10 | 8 de tarefa (`design-ui`, `verify-ui`, `component-review`, `a11y-review`, `perf-audit`, `e2e-tests`, `frontend-security-review`, `forms-and-data`), `playbook` e `prompts` | Verificado |
| Agentes | 5 | `frontend-a11y-reviewer`, `frontend-code-reviewer`, `frontend-perf-reviewer`, `frontend-security-auditor`, `ui-evaluator` | Verificado |
| Comandos | 0 | Diretório `commands/` inexistente | Verificado |
| Prompts na biblioteca | 40 | `PR-01` a `PR-40`: 27 em `prompt-library.md` e 13 em `prompt-library-dados-testes.md` (`PR-24` a `PR-36`) | Verificado |
| Casos de eval | 10 | Cada um com `prompt.md` e `graders/` | Verificado |
| Arquivos de referência | 38 | 25 em `skills/*/references/` e 13 templates em `skills/playbook/assets/templates/` | Verificado |
| Arquivos totais no plugin | 91 | Saída do verificador | Verificado |

## 3. Saídas resumidas das validações

- Verificador: `Plugin: web-frontend {'skills': 10, 'agents': 5, 'commands': 0, 'evals': 10, 'files': 91}` seguido de `RESULT: PASS`.
- Validador oficial: `Validating plugin manifest: .../plugins/web-frontend/.claude-plugin/plugin.json` seguido de `✔ Validation passed`, exit 0.

## 4. Qualidade (resumo do BUILD-REPORT-quality)

- Notas por arquivo: média antes 90,5, média depois 92,2, mínimo 90. Nenhum arquivo abaixo de 80. Nenhum critério de reprovação automática.
- Correções de conteúdo registradas na rodada de qualidade: `next/image` (`priority` substituída por `preload`, `loading="eager"` ou `fetchPriority` no Next 16); `middleware` renomeado para `proxy.ts` no Next 16 com a nota de que não substitui autorização na Server Action; `ref` como prop no React 19; `disallowed-tools` em três skills de leitura.
- Fidelidade técnica: afirmações conferidas contra documentação oficial (nextjs.org, react.dev, code.claude.com) e contra `VALIDATED.md`. Rótulo: Verificado para as afirmações com URL e data; Coerentes com a base para as demais.
- Direitos autorais e segurança: sem trechos literais longos de terceiros; créditos Apache-2.0 e MIT presentes no README e em `fontes.md`; sem segredos reais; sem hooks, `.mcp.json`, `.lsp.json` ou `bin/` ativos; `--dangerously-skip-permissions` aparece apenas como risco, em contexto de sandbox e repositório confiável.
- Agentes com `tools: Read, Grep, Glob`, sem Bash, Write ou Edit.

## 5. Correção estrutural já aplicada (rodada anterior)

- `plugins/web-frontend/README.md`: removida a linha que citava `/web-frontend:design-brief`, comando inexistente. Verificado nesta rodada: `grep design-brief` em todo o plugin retorna 0 ocorrências.

## 6. Pendências

1. Evals não executadas (`designed_not_executed`). `claude plugin eval` exige Claude Code 2.1.269 ou superior; a CLI local registrada é 2.1.128. Não verificável nesta rodada.
2. Skill `prompts` e os 5 agentes não têm caso de eval próprio. Incluir exige trocar um dos 10 casos atuais (limite do blueprint: 6 a 10). Decisão do usuário.
3. Fronteiras do playbook (`skills/playbook/SKILL.md`, tabela de fronteiras, e `skills/playbook/references/css-tokens-e-design-ui.md`) citam segmentos previstos em `docs/foundation/segments.json` que ainda não estão em `plugins/`. Mantidos como plano da fábrica; o playbook diz o que fazer quando o plugin vizinho não existe. Revalidar quando forem construídos. Não verificável: existência futura desses plugins.
4. `commands/design-brief.md` (opcional no SYNTHESIS) segue ausente. Não exigido pelo validador. Decisão do usuário.
5. Divergência de organização: o SYNTHESIS previa `prompt-library-revisao.md`; o conteúdo está em `prompt-library.md`. Sem link quebrado.
6. Lacunas declaradas no README (Signal Forms, hidratação sem página primária, CrUX, i18n e SEO) continuam Não verificadas.
7. Comportamento em runtime das skills e agentes não foi testado. Links externos de `fontes.md` não foram checados em rede.

## 7. Limites desta verificação

- Nenhum arquivo do plugin foi alterado nesta rodada.
- As notas de qualidade são leitura adversarial, não medição; nenhum eval foi executado.
