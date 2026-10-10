# BUILD-REPORT: plugin qa-testing

Data: 2026-10-10. Gate final do plugin `plugins/qa-testing`. Consolida `BUILD-REPORT-structural.md` e `BUILD-REPORT-quality.md` (mesma pasta).

## 1. Resultado do gate

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Verificador do segmento | `python tools/verify_plugin.py plugins/qa-testing` | `RESULT: PASS`, 0 erros, 0 avisos (Verificado) |
| Validador oficial | `claude plugin validate plugins/qa-testing` | `Validation passed` (Verificado) |

Saída resumida do verificador: `Plugin: qa-testing {'skills': 10, 'agents': 4, 'commands': 2, 'evals': 12, 'files': 101}`.

Saída resumida do validador oficial: validação do manifesto `.claude-plugin/plugin.json` concluída sem erros. O validador também listou servidores MCP de outros plugins da sessão que exigem autenticação ou falharam ao conectar; isso não pertence a `qa-testing`, que não declara `.mcp.json`.

Nenhuma correção foi necessária neste gate: não havia erro remanescente. Não houve edição de arquivos do plugin nesta passada.

## 2. Contagem de componentes

| Componente | Quantidade | Observação |
| --- | --- | --- |
| Skills | 10 | `playbook`, `prompts`, `verification-gate`, `tdd-guard`, `test-strategy`, `test-design`, `flaky-triage`, `e2e-review`, `bug-report`, `eval-design` |
| Agentes | 4 | `test-reviewer`, `test-auditor`, `qa-reporter`, `test-writer` |
| Comandos | 2 | `qa-evidence`, `eval-plugin` (manuais, `disable-model-invocation: true`) |
| Prompts na biblioteca | 31 | Títulos `### P##`: 20 em `prompt-library.md` e 11 em `prompts-flaky-bugs-evals.md`; batem com as 31 linhas do índice em `skills/prompts/SKILL.md` |
| Casos de eval | 12 | Pasta `evals/` com 12 casos e `README.md` (o validador conta 12) |
| Arquivos de referência | 27 | `references/` de 9 skills, sendo 12 só no `playbook` |
| Templates | 19 | 16 em `skills/playbook/assets/templates/` e 3 no caso de template `eval-case` |
| Total de arquivos | 101 | Contagem do verificador (o relatório estrutural antigo dizia 99 antes das edições de qualidade) |

Não há `hooks/`, `.mcp.json`, `.lsp.json` nem `bin/` ativos no plugin (Verificado por listagem).

## 3. Consolidação das duas auditorias

**Estrutural (`BUILD-REPORT-structural.md`).** Confirmou que o verificador e o validador passavam, e apontou: comandos ausentes, citações quebradas aos comandos, 12 evals contra 10 previstos, agente sem eval, e índice de prompts sem conferência. Desde então:

- Os comandos `qa-evidence` e `eval-plugin` foram criados e as citações foram restauradas. A pendência 1 está resolvida (Verificado: `commands/` tem 2 arquivos e o verificador os conta).
- Os 12 evals foram mantidos como decisão registrada: a biblioteca pede 6 a 10 casos, e os dois extras cobrem a skill `prompts` e o papel de revisor.
- O índice de prompts confere com a biblioteca (31 × 31). A pendência 4 está resolvida.

**Qualidade (`BUILD-REPORT-quality.md`).** Pontuação média antes ≈ 84,9 e depois ≈ 87,2 (mínimo 86), pela rubrica D1–D12 de `docs/foundation/prompt-quality-rubric.md`. Correções relevantes registradas por ela: caso negativo com `arm: both` (sem isso o sobredisparo não era medido), regra de `--allow-tools` (Write/Edit/Bash não são concedidos por padrão), campos de grader conferidos na documentação oficial, e `stop_hook_active` confirmado. Nenhum critério de reprovação automática foi encontrado.

Notas de quality que continuam abertas são registradas na seção 5.

## 4. Saídas e validações

- Verificador: `RESULT: PASS`, sem erros nem avisos.
- Validador oficial: `Validation passed`.
- Busca por resíduos (`eval-plugin`, `qa-evidence`, `TODO`): as únicas ocorrências são as citações corretas aos dois comandos existentes e a linha `<!-- TODO QA-COMPLETO -->` do caso negativo `negativo-frontend-css`, que é entrada de teste intencional e não placeholder.

## 5. Notas e pendências

Pendências herdadas, sem ação neste gate (exigem decisão ou execução fora deste escopo):

1. **Suíte não executada.** Todos os casos estão `designed_not_executed`. Rodar `claude plugin eval . --allow-tools Write Edit` (e o caso com `Bash` em WSL2) quando a CLI estiver em 2.1.269 ou superior. Custo e ferramentas exigem confirmação do usuário.
2. **Comandos não exercitados** em sessão real.
3. **Eval de agente.** O agente `test-reviewer` ainda não tem caso de delegação. Falta conferir, num transcript real, o nome do campo do subagente na entrada da ferramenta `Agent`; sem isso um `input_match` seria palpite.
4. **Fundação compartilhada.** `docs/foundation/plugin-blueprint.md` descreve o caso negativo sem `arm: both`. Isso afeta outros plugins da fábrica; a recomendação é acrescentar `arm: both` ao modelo e revisar os casos negativos dos demais plugins. Não foi editado aqui.
5. **Dado não verificado.** CNPJ alfanumérico em `test-design` segue "Não verificável" até confirmação na Receita Federal.

Rótulos: Verificado (comandos executados e saídas lidas nesta sessão) · Inferido (leitura dos relatórios anteriores) · Suposição (nenhuma) · Não verificável (item 5 acima) · Não aplicável (hooks/MCP/LSP/bin ausentes).
