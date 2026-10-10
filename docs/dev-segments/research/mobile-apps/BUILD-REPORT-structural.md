# BUILD-REPORT estrutural: plugin mobile-apps

Data: 2026-10-10. Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\mobile-apps`. Escopo: validação estrutural (não é a validação de qualidade do conteúdo).

## 1. Resultado das verificações

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Verificador do repositório (antes) | `python tools/verify_plugin.py <pasta>` | PASS, sem avisos (Verificado) |
| Validador oficial (antes) | `claude.exe plugin validate <pasta>` | Validation passed (Verificado) |
| Verificador do repositório (depois) | idem | PASS, sem avisos (Verificado) |
| Validador oficial (depois) | idem | Validation passed (Verificado) |

Contagem reportada pelo verificador: 11 skills, 5 agents, 0 commands, 10 evals, 103 arquivos.

## 2. Correções feitas

1. `skills/mobile-store-release-check/SKILL.md`, passo 5: a referência `skills/prompts/references/prompts-release.md` apontava para um arquivo que não existe. Trocada por `skills/prompts/references/prompt-library.md`, seção `## P-26` (Notas de versão), que existe. Este era o único link de caminho quebrado para um arquivo do plugin. O verificador não detectou a falha, pois a referência estava em texto com variável `${CLAUDE_PLUGIN_ROOT}`.

Nenhum outro conteúdo foi reescrito.

## 3. Comparação com o SYNTHESIS (seção 4.2, 4.5, 4.8, 4.10)

Presentes conforme previsto:

- Skills: `playbook`, `prompts` e as 9 skills de tarefa (inclui `mobile-build-troubleshoot`, acrescentada na revisão do crítico). Todas com `SKILL.md` e frontmatter `name` igual à pasta.
- Agentes: `mobile-architect`, `mobile-pr-reviewer`, `mobile-release-auditor`, `mobile-security-auditor`, `mobile-test-engineer`.
- Referências do `playbook` (12 arquivos da seção 4.2).
- Templates do `playbook` (18 arquivos da seção 4.8).
- Evals: 10 casos previstos, cada um com `prompt.md` e graders; `evals/README.md` e `evals/.gitignore`.
- Ausência de hooks, `.mcp.json`, `.lsp.json`, `bin/` e `CLAUDE.md` na raiz (Verificado pela listagem de arquivos).

Ausentes ou pendentes (Verificado pela comparação de árvore):

- `skills/prompts/references/`: a seção 4.2 prevê 7 arquivos (`prompt-library.md`, `prompts-ios.md`, `prompts-android.md`, `prompts-cross-platform.md`, `prompts-release.md`, `prompts-qualidade.md`, `prompts-sistema.md`). Existe apenas `prompt-library.md`, que concentra os 33 prompts (94 KB). Não há links quebrados para os seis arquivos ausentes, pois o `SKILL.md` aponta só para `prompt-library.md`. Lacuna de estrutura de organização, não de conteúdo.
- Eval reserva `ios-sem-mac-windows` (caso 11 do SYNTHESIS): não criado. A própria seção 4.10 o marca como opcional.
- O verificador não confere se a árvore corresponde à seção 4.2 do SYNTHESIS; a comparação acima foi manual.

Arquivos pequenos (menos de 200 bytes) em `evals/*/graders/`: são os graders `skill-fired.md`, `no-*.md`, com critérios curtos. O verificador os aceita. Conteúdo não avaliado aqui; o validador de qualidade deve conferir se os critérios são úteis.

## 4. Verificação de README e playbook

- Todo nome de skill ou agente citado em `README.md` e em `skills/playbook/SKILL.md` existe como componente (Verificado: 16 nomes citados, 0 ausentes).
- Contagens do README conferidas: 33 prompts (33 seções `## P-NN` em `prompt-library.md`), 18 templates, 12 referências do `playbook`, 9 skills de tarefa, 5 agentes. Todas batem (Verificado).
- A tabela de componentes do README lista apenas componentes existentes.

## 5. Ressalvas (não corrigidas, fora do escopo estrutural)

- `skills/playbook/references/checklist-completo.md` (ACE-10), `ios-swift.md` e `prompts/references/prompt-library.md` (V-11) citam `references/accessibility.md` e `references/stability.md`. São arquivos do repositório de origem, descritos como não transcritos. Não são caminhos do plugin e não quebram a validação. Ficam como pendência de conteúdo: o plugin não pode abri-los.
- Verificação de links: a checagem manual de links relativos em Markdown não encontrou outros caminhos quebrados. Um falso positivo apareceu em `evals/modo-completo-em-log/graders/no-full-reading.md`, onde uma expressão regular foi escrita entre parênteses; não é link.
- Os avisos da política de nomes (nome do plugin igual à pasta, `description` até 1024 caracteres, `SKILL.md` até 500 linhas) não aparecem na saída do verificador.

## 6. Pendências para o validador de qualidade

1. Decidir se os seis arquivos `prompts-*.md` previstos devem existir ou se a seção 4.2 do SYNTHESIS deve ser atualizada para refletir o arquivo único `prompt-library.md`.
2. Decidir se o eval reserva `ios-sem-mac-windows` entra.
3. Avaliar a qualidade do conteúdo dos graders curtos.
4. Substituir ou recuperar as referências a `accessibility.md` e `stability.md` de repositórios externos, se o conteúdo for necessário.

## 7. Rótulos

- Verificado: resultados dos dois validadores, contagens, existência e ausência de arquivos, correção aplicada.
- Não aplicável: avaliação de qualidade de conteúdo e execução das evals (`designed_not_executed`).
