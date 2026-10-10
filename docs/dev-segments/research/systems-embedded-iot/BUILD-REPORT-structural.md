# BUILD-REPORT estrutural: plugin systems-embedded-iot

Data: 2026-10-10
Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\systems-embedded-iot`
Papel: validador estrutural (não reescreve conteúdo de referência; o validador de qualidade completa o restante).

## 1. Verificações executadas

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Verificador determinístico | `python tools/verify_plugin.py <pasta>` | PASS (sem erros). Contagem: 10 skills, 5 agentes, 0 commands, 13 evals, 106 arquivos. |
| Validador oficial | `claude.exe plugin validate <pasta>` | Validation passed, sem avisos. |

Verificado: as duas execuções foram feitas antes de qualquer alteração e não exibiram erros nem avisos. Não houve correções a aplicar, então nenhum arquivo do plugin foi modificado neste passo.

## 2. Checagens estruturais adicionais (leitura e grep)

- Nomes de skills e agentes: as 10 pastas em `skills/` (`bus-protocol-review`, `datasheet-first`, `firmware-review`, `firmware-root-cause`, `firmware-test-host`, `hw-bench-loop`, `ota-security-review`, `playbook`, `prompts`, `rtos-concurrency-review`) e os 5 arquivos em `agents/` (`embedded-architect`, `firmware-debugger`, `firmware-reviewer`, `firmware-test-engineer`, `iot-security-auditor`) existem e coincidem com os nomes do playbook e do README.
- Links relativos: todas as referências relativas a `references/`, `assets/templates/` e `evals/` foram resolvidas dentro das pastas de skill corretas. Nenhum link quebrado foi encontrado.
- Placeholders: nenhum arquivo vazio ou com marcador TODO/TBD. A palavra "placeholder" aparece apenas de forma intencional, em evals que exigem placeholders.
- Referência de procedência fora do plugin: `skills/prompts/references/prompt-library-bancada-seguranca-processo.md` cita `brains/fullstack/assets/templates/handoff-checkpoint.md` como fonte de procedência, em texto, não como link. Verificado: não é link quebrado. Inferido: o caminho aponta para o brain-of-agent do usuário, fora da raiz do plugin.
- Fontes externas (URLs de `fontes.md` e das referências) não foram acessadas nesta verificação. Não verificável neste passo.

## 3. Comparação com o SYNTHESIS (componentes previstos x existentes)

| Componente previsto (SYNTHESIS seção 4) | Estado |
| --- | --- |
| `playbook` com 12 references e templates | Presente: 12 references em `skills/playbook/references/` e 16 templates em `skills/playbook/assets/templates/`. O SYNTHESIS fala em T-01 a T-14; há 16, o que é um excedente, não uma falta. |
| `prompts` (SKILL.md + prompt-library) | Presente: `prompt-library.md` (PR-01 a PR-20) e `prompt-library-bancada-seguranca-processo.md` (PR-21 a PR-30). |
| 8 skills de tarefa | Presentes: `firmware-review`, `rtos-concurrency-review`, `bus-protocol-review`, `datasheet-first`, `firmware-root-cause`, `firmware-test-host`, `hw-bench-loop`, `ota-security-review`. |
| 5 agentes | Presentes: `embedded-architect`, `firmware-reviewer`, `firmware-debugger`, `firmware-test-engineer`, `iot-security-auditor`. |
| Evals (E1 a E10 + reserva) | Presentes: 13 pastas, com `evals/README.md` e `evals/.gitignore`. E1 a E10 correspondem aos 10 casos principais. Os 3 restantes são casos de reserva; verificado pelo nome de pasta, não pela lista de reserva do SYNTHESIS (que estava truncada na leitura). |
| Ausência de hooks, `.mcp.json`, `.lsp.json`, `bin/` | Conforme: nenhum desses arquivos existe no plugin. |

Remaining (pendências, nenhuma estrutural):

1. Evals: todos os 13 casos estão em status `designed_not_executed`. Não verificável neste passo: não rodei `claude plugin eval .` (custo e tempo). Os graders não foram avaliados em execução.
2. Lista exata dos casos de reserva: confirmar nos nomes do SYNTHESIS seção 4.9 se os 3 casos de reserva extra correspondem às pastas existentes. Não verificado linha a linha.
3. Qualidade de conteúdo (prompt-score ≥ 80, rubrica D1 a D12 do blueprint): fora do escopo deste validador estrutural. Fica para o validador de qualidade.
4. Fontes externas (URLs e licenças em `fontes.md`): não acessadas nesta passagem. Não verificável.
5. Arquivos de skill, agente e referência não foram lidos integralmente; a checagem foi por existência, nomes, frontmatter aceito pelo validador e links.

## 4. Conclusão

Verificado: o plugin passa no verificador determinístico e no validador oficial, sem erros nem avisos; todos os componentes previstos no SYNTHESIS existem; README e tabela intenção → skill/agente citam apenas componentes existentes; todos os links relativos resolvem.

Correções aplicadas nesta passagem: nenhuma (não havia erros nem avisos a corrigir).
