# BUILD-REPORT: technical-writing-docs (gate final)

Data: 2026-10-10. Plugin: `plugins/technical-writing-docs`. Consolida `BUILD-REPORT-structural.md` e `BUILD-REPORT-quality.md` nesta pasta.

## 1. Resultado

- `verify_plugin.py`: PASS, sem ERROS. Contagem reportada: 10 skills, 4 agentes, 0 comandos, 12 evals, 106 arquivos.
- `claude plugin validate`: Validation passed.
- Rótulo: Verificado (executado nesta sessão).

Nesta etapa não houve correções: os dois validadores passaram sem alteração de arquivos do plugin.

## 2. Contagem de componentes

| Componente | Quantidade | Observação |
| --- | --- | --- |
| Skills | 10 | 8 de tarefa (`auditar-claude-md`, `diagramar-arquitetura`, `documentar-codigo`, `escrever-adr`, `escrever-changelog-release`, `escrever-guia-diataxis`, `escrever-readme`, `escrever-runbook`), mais `playbook` e `prompts` |
| Agentes | 4 | `auditor-de-docs`, `revisor-de-instrucoes`, `revisor-de-leitor`, `technical-writer` |
| Comandos | 0 | não há `commands/` |
| Prompts na biblioteca | 35 | PD-01 a PD-35 em `skills/prompts/references/prompt-library.md` (blocos de prompt) |
| Casos de eval | 12 | pastas em `evals/`, com 28 graders |
| Referências (`playbook`) | 12 | em `skills/playbook/references/` |
| Templates | 26 | em `skills/playbook/assets/templates/` |
| Snippets de CLAUDE.md | 22 | S-01 a S-22 |
| Arquivos no plugin | 106 | contagem do verificador |

Rótulo: Verificado (contagens feitas por `find`, `grep` e pelo verificador).

## 3. Consolidação dos relatórios anteriores

### Estrutural (`BUILD-REPORT-structural.md`)
- Validadores passavam antes e depois das edições estruturais.
- Correções de conteúdo: oito plugins de fronteira citados em `skills/playbook/SKILL.md` marcados como "planejado" (ainda não existem em `plugins/`); contagem de evals corrigida no `README.md`.

### Qualidade (`BUILD-REPORT-quality.md`)
- Média de notas (rubrica D1 a D12): 86,1 antes, 89,1 depois; mínimo 87 (`auditor-de-docs`).
- Correções nos evals: `arm: both` no grader negativo, `arm: with-only` em `references-read`, flag `--ablation` corrigida para `none|with-without`, novo caso negativo de fronteira (`negativo-decisao-ainda-nao-tomada`).
- Ressalva do próprio relatório: o validador de qualidade é o mesmo modelo família dos construtores; não é validação externa.

## 4. Notas

- Evals foram desenhados, mas não executados (`designed_not_executed`). Não há resultado de execução a alegar.
- `auditor-de-docs` tem `Bash` restrito a git de leitura apenas por instrução do prompt: o campo `tools` do subagente não aceita padrões de comando.
- `--dangerously-skip-permissions` aparece apenas como risco (T-11), não como padrão.
- Nenhum hook, `.mcp.json`, `.lsp.json` ou `bin/` ativo no plugin.

## 5. Pendências

1. Executar os evals com `claude plugin eval` (exige Claude Code 2.1.269 ou superior; a CLI local usada nos relatórios era 2.1.128). Resultado: Não verificado até a execução.
2. Decidir sobre o número de casos de eval: 12 atuais contra 10 previstos no SYNTHESIS 4.9. Manter e atualizar o SYNTHESIS, ou podar.
3. `auditor-de-docs` com `Bash`: remover o Bash ou documentar `permissions.deny` no projeto de destino.
4. Cobertura de eval ausente para `prompts`, para os quatro agentes e para o modo `api` de `documentar-codigo`.
5. Oito plugins de fronteira ainda não existem; a marcação "planejado" deve sair quando forem criados.
6. Versões de ferramentas (Vale, lychee, markdownlint, actions de Pages) não rechecadas na web nesta etapa; rótulos Inferido ou Não verificado nos arquivos.
7. Marketplace `brain-of-agent`: nome e comandos de instalação não testados.
8. Referências e templates lidos por amostra, não linha a linha.

## 6. Saídas resumidas das validações

```
python tools/verify_plugin.py plugins/technical-writing-docs
Plugin: technical-writing-docs  {'skills': 10, 'agents': 4, 'commands': 0, 'evals': 12, 'files': 106}
RESULT: PASS

claude.exe plugin validate plugins/technical-writing-docs
Validating plugin manifest: .claude-plugin/plugin.json
Validation passed
```
