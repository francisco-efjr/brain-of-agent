# BUILD-REPORT estrutural — plugin data-engineering

Data: 2026-10-10 · Papel: validador estrutural · Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\data-engineering`

Rótulos: Verificado = saída de ferramenta nesta execução. Inferido = dedução a partir de leitura. Suposição = premissa não checada. Não verificável = sem como checar aqui.

## 1. Verificações executadas

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Verificador do repositório | `python "C:\Users\Francisco Edson\dev-segments\tools\verify_plugin.py" "C:\Users\Francisco Edson\dev-segments\plugins\data-engineering"` | Verificado: `RESULT: PASS`, sem avisos. Contagem: 10 skills, 5 agents, 0 commands, 13 evals, 93 arquivos |
| Validador oficial do Claude Code | `claude.exe plugin validate "...\plugins\data-engineering"` | Verificado: `Validation passed` |

Nenhuma alteração de conteúdo foi necessária para passar nas duas verificações. Nenhum arquivo do plugin foi editado nesta execução.

## 2. Checagens estruturais adicionais (Verificado por leitura e script)

- **Links relativos em Markdown:** 0 links quebrados em todos os `.md` do plugin (script que resolve cada `](caminho)` a partir do arquivo de origem; links `http` e `${CLAUDE_PLUGIN_ROOT}` ignorados).
- **Nome × pasta:** os 10 `SKILL.md` e os 5 agentes têm `name` igual ao nome da pasta ou ao nome do arquivo.
- **Frontmatter de skills:** `description` entre 471 e 805 caracteres (todas abaixo de 1024). `disable-model-invocation: true` presente em `pipeline-acceptance` e `gated-pipeline-migration`, como previsto.
- **Frontmatter de agentes:** todos com `tools` em allowlist sem `Write`, `Edit` ou `Bash`. `eval-judge` tem só `Read`.
- **Tamanho do corpo das skills:** todos os `SKILL.md` com até 165 linhas (playbook), dentro do limite de 300 do SYNTHESIS.
- **Sem componentes proibidos:** não há `hooks/`, `.mcp.json`, `.lsp.json` nem `bin/` (Verificado pela listagem de arquivos).
- **Placeholders:** nenhuma ocorrência de TODO, TBD, FIXME ou lorem nos arquivos do plugin. A única ocorrência de instrução injetada está em `evals/text-to-sql-com-injecao-no-schema/prompt.md`, de propósito, como caso de teste.
- **Evals:** 13 casos, cada um com `prompt.md` e `graders/`. Os `graders/skill-fired.md` e `no-*.md` são arquivos curtos de frontmatter (`type`, `tool`, `input_match`) e não são placeholders (Inferido pela forma).
- **Manifesto:** `.claude-plugin/plugin.json` válido, com `name` igual à pasta, versão `0.1.0`, licença MIT. Sem campos `skills`, `agents` ou `commands`, como previsto no SYNTHESIS §4.1.

## 3. README e tabela intenção → componente (playbook)

- Verificado: todos os componentes citados no README e na tabela de intenções do `skills/playbook/SKILL.md` existem: as 10 skills, os 5 agentes, as 12 referências e os 12 templates.
- Verificado: as contagens citadas conferem. "22 regras" (cabeçalho em `claude-md-snippets.md`), "9 passos" (playbook, passos 0 a 8), "8 verificações" (`pipeline-acceptance`, passos 1 a 8), "12 princípios" (K-01 a K-12), "8 skills de tarefa" e "5 agentes".
- Nenhuma alteração foi feita no README nem na tabela.

## 4. Comparação com SYNTHESIS.md (lista de componentes previstos)

Componentes previstos e presentes: `plugin.json`, `README.md`, 10 skills (`playbook`, `prompts`, `dbt-model-workflow`, `pipeline-acceptance`, `airflow-dag-workflow`, `spark-streaming-review`, `sql-review`, `text-to-sql-safe`, `data-contracts-quality`, `gated-pipeline-migration`), 5 agentes (`data-pipeline-reviewer`, `analytics-reviewer`, `pipeline-debugger`, `eval-judge`, `data-pipeline-architect`), 12 referências do playbook, 12 templates, `evals/README.md`, `evals/.gitignore`.

Ausentes: nenhum componente previsto obrigatório está ausente.

Divergências a registrar (não corrigidas, por serem de conteúdo ou de decisão de design):

1. **Modelo dos agentes.** SYNTHESIS §4.4 prevê `model: sonnet` para `analytics-reviewer` e `data-pipeline-architect`. No plugin, os cinco agentes têm `model: inherit`. Validador passa com ambos. Decisão de design, não estrutural: cabe ao autor escolher. Classificação: Inferido.
2. **Contagem de evals na árvore do SYNTHESIS.** A árvore da §4.0 diz `10 casos`, mas o plano de evals (§ de evals e `evals/README.md`) e o disco têm 13. O erro está na árvore do SYNTHESIS, não no plugin. Verificado.
3. **Referências do prompts.** SYNTHESIS §4.0 prevê a divisão de `prompt-library` em arquivos extras só se passar de 600 linhas. O arquivo atual é único. Não há falta. Verificado pela listagem.
4. **Evals não executados.** O SYNTHESIS registra que `claude plugin eval` exige versão 2.1.269 ou superior, e a CLI local é anterior. Os evals estão apenas desenhados, não executados. Verificado pela leitura do SYNTHESIS; não verificável aqui se a CLI atual já atende.

## 5. Pendências para o validador de qualidade

- Conferir o conteúdo substantivo das 12 referências e 12 templates, que esta etapa não leu integralmente (o escopo é estrutural). Não verificável nesta etapa.
- Decidir se os agentes `analytics-reviewer` e `data-pipeline-architect` ficam em `inherit` ou passam a `sonnet` (item 4.1).
- Executar os evals com a CLI atualizada, quando disponível. Não verificável nesta etapa.
- Revisar a proporção de skills automáticas: `prompts` e `playbook` ficam com descrição longa (718 e 805 caracteres) para roteamento. Inferido: dentro do limite, sem problema estrutural.

## 6. Resultado

- Verificador do repositório: PASS, sem avisos.
- Validador oficial: passou.
- Erros corrigidos: nenhum (não havia erros).
- Links quebrados: 0.
- Componentes previstos ausentes: 0.
