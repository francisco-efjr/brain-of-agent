# BUILD-REPORT estrutural: data-science-ml

Data: 2026-10-10. Papel: validador estrutural. Escopo: estrutura, frontmatter, links, manifesto, consistência entre README/playbook e componentes previstos em `SYNTHESIS.md`. Não reescreve conteúdo de domínio; a qualidade de prompt é de outro validador.

## 1. Verificações executadas

| Verificação | Antes | Depois |
| --- | --- | --- |
| `python tools/verify_plugin.py plugins/data-science-ml` | PASS (skills 10, agents 5, commands 0, evals 10, files 89) | PASS (sem alteração de contagem) |
| `claude.exe plugin validate plugins/data-science-ml` | "Validation passed" | "Validation passed" |

Ambos passaram sem avisos já na primeira execução. Verificado: a saída do verificador e do validador oficial nesta execução.

## 2. Erros e avisos corrigidos

Nenhum erro estrutural (frontmatter, nome vs pasta, link relativo, campo desconhecido, JSON inválido, grader inválido) foi encontrado pelos dois validadores.

A correção feita foi de consistência: README, playbook e prompts citavam um componente inexistente, o comando `/data-science-ml:ds-validate` (`commands/ds-validate.md`). Esse arquivo não existe. Alterações:

- `README.md`: removida a linha de tabela "Comando | /data-science-ml:ds-validate"; removida a menção a "um comando de validação" no resumo; removido "comando" da lista de componentes.
- `skills/playbook/SKILL.md`: linha da tabela intenção → componente agora aponta para o checklist de REF-01 e diz que não há comando nesta versão.
- `skills/prompts/SKILL.md`: linha PR-32 sem o comando.
- `skills/prompts/references/prompt-library-mlops-sistema.md`: título e texto de PR-32 deixam de afirmar que o comando existe.
- `skills/ds-mlops-promotion/SKILL.md`: removida referência a `/ds-validate`.
- `skills/playbook/references/mlops-governanca-notebooks.md` (seção 9 e item 9) e `skills/playbook/references/ferramentas-e-mcp.md` (seção 7): título marcado como comando planejado, não incluído nesta versão.

Após as correções, ambas as verificações continuam em PASS.

## 3. Comparação com SYNTHESIS (componentes previstos)

Verificado por listagem de arquivos e tamanho (nenhum arquivo vazio; nenhum marcador TODO/TBD/placeholder encontrado).

| Componente previsto (SYNTHESIS §4) | Situação |
| --- | --- |
| `plugin.json`, `README.md` | Presentes |
| `skills/playbook` + 12 referências REF-01..REF-12 | Presentes (nomes em kebab-case, não numerados no arquivo) |
| `skills/playbook/assets/templates` TPL-01..TPL-13 | Presentes (13 arquivos, incluindo `caso-de-eval.jsonl`) |
| 8 skills de tarefa (ds-leakage-audit, ds-eda, ds-model-evaluation, ds-train-debug, ds-time-series-backtest, ds-inference-review, ds-llm-eval, ds-mlops-promotion) | Presentes |
| `skills/prompts` com índice e biblioteca PR-01..PR-33 | Presentes (33 IDs encontrados) |
| 5 agentes somente leitura (AG-01..AG-05) | Presentes |
| 10 casos de eval com `prompt.md` e `graders/` | Presentes; `evals/README.md` e `evals/.gitignore` presentes |
| `commands/ds-validate.md` (opcional, §4.6) | Ausente. Previsto como opcional; não criado |

## 4. Remaining (pendências para o validador de qualidade e o construtor)

1. Comando opcional `commands/ds-validate.md` (SYNTHESIS §4.6) não foi criado. Se for incluído, README, `skills/playbook/SKILL.md` e `skills/prompts/SKILL.md` podem voltar a citá-lo, e as anotações "planejado, não incluído" devem ser removidas.
2. Algumas referências de domínio (`ferramentas-e-mcp.md` seção 7, `mlops-governanca-notebooks.md` seção 9) descrevem o gate de validação em termos de comando; o texto está marcado como planejado, mas o conteúdo não foi revisado para mérito.
3. `evals/README.md` lista `ds-validate` como lacuna de cobertura. Isso é correto e foi mantido.
4. Prompt-score ≥ 80 (rubrica de qualidade de prompt), tamanho das skills (<500 linhas) e cobertura dos graders não foram avaliados aqui. São responsabilidade do validador de qualidade.
5. Limite de ~300 linhas do playbook (SYNTHESIS §4.2) não foi medido nesta execução.

## 5. Não verificado

- Execução real dos evals (`claude plugin eval`) não foi rodada.
- Conteúdo dos prompts e das referências não foi lido linha a linha; a validação foi estrutural e de consistência de nomes.
- Instalação via marketplace não foi testada.
