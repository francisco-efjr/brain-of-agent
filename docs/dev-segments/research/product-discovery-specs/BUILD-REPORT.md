# BUILD-REPORT: product-discovery-specs

Data: 2026-10-10 · Plugin: `plugins/product-discovery-specs` · Gate final consolidado.

## Resumo

- Verificador `tools/verify_plugin.py`: **PASS**, sem erros.
- Validador oficial `claude plugin validate`: **Validation passed**.
- Relatório estrutural (`BUILD-REPORT-structural.md`): **não existe** nesta pasta; nada a cruzar.
- Relatório de qualidade (`BUILD-REPORT-quality.md`): consolidado abaixo; média de qualidade 85,3 → 86,9, mínimo 85, nenhum artefato abaixo de 80 (Verificado pelo relatório de qualidade, julgamento por leitura).
- Evals: desenhados, **não executados** (rótulo Não verificável para desempenho real).

## Contagens (Verificado por `verify_plugin.py` e contagem direta)

| Componente | Quantidade | Observação |
| --- | --- | --- |
| Skills (`skills/*/SKILL.md`) | 10 | playbook, prompts, spec-interview, write-prd, write-spec, acceptance-criteria, refine-backlog, prioritize-roadmap, run-discovery, spec-to-tasks |
| Agentes (`agents/*.md`) | 5 | spec-reviewer, plan-writer, decision-recorder, discovery-synthesizer, feasibility-scout |
| Blocos de prompt na biblioteca | 43 identificadores (P-01 a P-43) | `skills/prompts/references/prompt-library.md`, contados por grep de IDs únicos. O relatório de qualidade menciona "40 prompts"; a diferença não foi resolvida e fica registrada como nota. |
| Casos de eval (`evals/*/`) | 17 | com `prompt.md` e `graders/` |
| Arquivos de referência (`references/`) | 30 | dentro de `skills/*/references/` |
| Assets (templates) | 26 | dentro de `skills/playbook/assets/` e afins |
| Arquivos totais do plugin | 130 | `verify_plugin.py` |

## Validações (saídas resumidas)

- `python tools/verify_plugin.py ...product-discovery-specs` → `Plugin: product-discovery-specs {'skills': 10, 'agents': 5, 'commands': 0, 'evals': 17, 'files': 130}` / `RESULT: PASS` (exit 0).
- `claude plugin validate ...product-discovery-specs` → `Validating plugin manifest: .claude-plugin\plugin.json` / `✔ Validation passed` (exit 0).

Nenhuma correção foi necessária nesta rodada de gate: ambos os validadores passaram sem erros remanescentes.

## Notas (do relatório de qualidade)

- Correções de fidelidade aplicadas na fase de qualidade: caso negativo com `arm: both`; `allowed_tools` corrigido (só leitura; escrita e Bash exigem `--allow-tools`, tag `needs-write-grant`); `--ablation` recebe modo `none` ou `with-without`; `Agent` adicionado em casos de delegação; graders `scores` e `sample-size` testados com Node.
- Hook `Stop` (exit 2 e `stop_hook_active`) e sintaxe `:*` em permissões confirmados na documentação oficial (Verificado, com data).
- `--dangerously-skip-permissions` aparece só como risco em 5 pontos, nunca como padrão.
- Sem hooks, `.mcp.json`, `.lsp.json` ou `bin/` ativos.
- Licenças: literal só de conteúdo próprio (MIT, com atribuição); terceiros apenas destilados com atribuição em `fontes.md`; `deanpeters/Product-Manager-Skills` (CC BY-NC-SA) declarado como não usado.

## Pendências

1. Nenhum `BUILD-REPORT-structural.md` existe; se o validador estrutural rodar depois, cruzar as pendências dele com este relatório.
2. Evals não executados. A CLI local é 2.1.128 e `claude plugin eval` exige 2.1.269. Recomendado rodar em WSL2/Linux: primeiro `--ablation none` para ajustar graders, depois a suíte padrão, e `--tag needs-write-grant --allow-tools Write Bash` em sandbox.
3. Campo de entrada da ferramenta `Agent` não conferido (Inferido); conferir no primeiro transcript.
4. Cobertura de eval fraca em `spec-to-tasks` (manual), `plan-writer`, `feasibility-scout`, modo `update` do `write-spec` e OKR para avaliar pessoas (menos de 3 casos por skill).
5. Juiz LLM da mesma família por padrão; usar `--judge-model` de outra família e calibrar contra leitura humana.
6. Dos 43 prompts, a maioria não foi pontuada individualmente na qualidade (amostra de 12 lida em detalhe; restante por índice e grep).
7. Lacunas de evidência herdadas de `VALIDATED.md` (JTBD sem fonte primária, OEC/SRM, North Star/HEART/AARRR, roadmap com fonte única) seguem declaradas no README; não são corrigíveis por edição.
8. Divergência de contagem de prompts (40 no relatório de qualidade × 43 IDs no arquivo): revisar a numeração.

## Verificação final

- `verify_plugin.py` → PASS.
- `claude plugin validate` → passed.
- Gate concluído sem alterações no plugin nesta rodada.
