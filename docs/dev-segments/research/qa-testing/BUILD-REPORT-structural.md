# BUILD-REPORT estrutural: plugin qa-testing

Data: 2026-10-10. Escopo: validação estrutural (não avalia qualidade de conteúdo; isso cabe ao validador de qualidade).

## 1. Resultado das verificações

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Verificador do segmento | `python tools/verify_plugin.py plugins/qa-testing` | RESULT: PASS, 0 erros, 0 avisos (Verificado) |
| Validador oficial | `claude plugin validate plugins/qa-testing` | Validation passed, 0 erros, 0 avisos (Verificado) |

Contagem reportada pelo verificador: 10 skills, 4 agentes, 0 comandos, 12 casos de eval, 99 arquivos.

Após as correções (seção 2), as duas verificações foram repetidas e continuam sem erros.

## 2. Correções feitas

Não havia erro de frontmatter, nome ≠ pasta, JSON inválido, grader inválido ou link relativo quebrado: o verificador e o validador oficial já passavam na primeira execução. Corrigi o que restava de referência a componentes inexistentes:

- Os comandos `/qa-testing:qa-evidence` e `/qa-testing:eval-plugin` são citados em README, playbook, skills e template, mas não existem (`commands/` ausente). As citações foram reescritas para não nomear o componente ausente. Onde a execução de eval é descrita, o texto agora cita o comando real `claude plugin eval`.

Arquivos alterados (todos dentro de `plugins/qa-testing/`):

- `README.md` (tabela de componentes)
- `evals/README.md`
- `skills/eval-design/SKILL.md` (2 trechos)
- `skills/playbook/SKILL.md` (2 linhas da tabela intenção → skill/agente)
- `skills/playbook/references/bugs-e-evidencia.md`
- `skills/playbook/references/ferramentas-e-mcp.md`
- `skills/playbook/assets/templates/evidencia-de-teste.md`
- `skills/prompts/SKILL.md` (P04)
- `skills/verification-gate/SKILL.md`

Verificação de conformidade: nenhum resto de `eval-plugin` ou `qa-evidence` no plugin (grep, Verificado). A tabela intenção → skill/agente cita somente skills e agentes existentes (`verification-gate`, `tdd-guard`, `test-strategy`, `test-design`, `flaky-triage`, `e2e-review`, `bug-report`, `eval-design`, `prompts`, `test-reviewer`, `test-auditor`, `qa-reporter`, `test-writer`, `playbook`, `code-quality-refactoring` como fronteira de outro segmento).

Não reescrevi conteúdo grande. Criar os comandos está na lista de pendências.

## 3. Comparação com SYNTHESIS (componentes previstos)

Itens presentes: 10 skills (`playbook`, `prompts`, `verification-gate`, `tdd-guard`, `test-strategy`, `test-design`, `flaky-triage`, `e2e-review`, `bug-report`, `eval-design`), 4 agentes, 12 referências do playbook, 16 templates, 31 prompts na tabela de `prompts/SKILL.md`.

Itens pendentes (Verificado por listagem de diretório):

1. **Comandos ausentes.** SYNTHESIS 4.4 prevê `commands/qa-evidence.md` e `commands/eval-plugin.md`. Não existem. A blueprint marca `commands/` como opcional, mas o SYNTHESIS os previa e o plugin os citava.
2. **Evals fora do previsto.** SYNTHESIS 4.10 lista 10 casos (EV-01 a EV-10). A pasta `evals/` tem 12. Ficam fora da lista do SYNTHESIS `prompt-pronto-revisao-testes` e `revisao-teste-gerado-por-ia`. A blueprint pede 6 a 10 casos.
3. **Sem eval para agentes.** Já reconhecido no SYNTHESIS (crítico): nenhum dos 4 agentes tem caso de eval.
4. **Índice de prompts não confere com a biblioteca.** `skills/prompts/SKILL.md` tem 31 linhas `| P## |`. `skills/prompts/references/prompt-library.md` tem 0 linhas nesse formato. Não auditei o conteúdo da biblioteca (Não verificável nesta etapa; cabe ao validador de qualidade).

## 4. Itens verificados e sem ação

- `evals/negativo-frontend-css/prompt.md` contém `<!-- TODO QA-COMPLETO antes do lançamento -->`. Não é placeholder do plugin: é a entrada de teste do caso negativo que mede se a keyword em comentário não ativa o modo (Verificado por leitura do SYNTHESIS, EV-09).
- Arquivos pequenos (até 200 bytes): são os graders `skill-fired.md` e `no-write.md` e similares, todos com formato aceito pelo validador. Não são placeholders.
- Nenhum `hooks/`, `.mcp.json`, `.lsp.json` ou `bin/` no plugin (Verificado por listagem).

## 5. Pendências para o builder

1. Criar `commands/qa-evidence.md` e `commands/eval-plugin.md` conforme SYNTHESIS 4.4, com `disable-model-invocation: true`. Depois, restaurar nas citações os nomes `/qa-testing:qa-evidence` e `/qa-testing:eval-plugin` e rodar as duas verificações de novo.
2. Decidir sobre os 2 casos extras de eval (manter e mapear no SYNTHESIS, ou remover para ficar em 10).
3. Criar pelo menos um caso de eval para o agente `test-reviewer` (SYNTHESIS, sugestão P18).
4. Verificar se o índice de prompts deve apontar para uma biblioteca em formato de tabela ou se o `prompt-library.md` precisa do formato `| P## |`.

Rótulos: Verificado (comandos executados e saídas lidas nesta sessão) · Inferido (leitura do SYNTHESIS e da blueprint) · Não verificável (qualidade de conteúdo fora do escopo estrutural).
