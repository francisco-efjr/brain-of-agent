# BUILD-REPORT estrutural: code-quality-refactoring

Data: 2026-10-10. Plugin: `plugins/code-quality-refactoring`. Papel: validação estrutural (não é a validação de qualidade de conteúdo).

## 1. Resultado das verificações

| Verificação | Comando | Antes | Depois |
| --- | --- | --- | --- |
| Verificador determinístico | `python tools/verify_plugin.py plugins/code-quality-refactoring` | RESULT: PASS, sem avisos | RESULT: PASS, sem avisos |
| Validador oficial | `claude.exe plugin validate ...\code-quality-refactoring` | Validation passed | Validation passed |
| Links relativos em `.md` | script de checagem (`[texto](caminho)`) | 0 quebrados | 0 quebrados |
| Referências `${CLAUDE_PLUGIN_ROOT}/...` | script de checagem | 20 referências, 0 ausentes | 20 referências, 0 ausentes |
| JSON do manifesto | parser JSON | válido | válido |
| Arquivos vazios | `find -empty` | nenhum | nenhum |
| Placeholders (TODO, TBD, a preencher) | busca textual | nenhum placeholder real (ocorrências são conteúdo, ex.: a palavra TODO como marcador de dívida) | igual |

Inventário final: 10 skills (`playbook`, `prompts`, `review-diff`, `debug-causa-raiz`, `refactor-seguro`, `simplify-safe`, `migration-parity`, `tech-debt-triage`, `code-health-report`, `codebase-onboarding`), 5 agentes (`code-reviewer`, `finding-validator`, `debugger`, `refactor-planner`, `codebase-mapper`), 12 casos de eval, 0 hooks, 0 `.mcp.json`, 0 `.lsp.json`, 0 `bin/`, 0 `commands/`.

## 2. Correções feitas

Verificado: a única inconsistência encontrada foi a contagem de evals.

- `README.md`, tabela de componentes: "10 casos" corrigido para "12 casos".
- `README.md`, seção "Limitações honestas": "os 10 casos" corrigido para "os 12 casos".

Motivo: `evals/README.md` e a própria pasta `evals/` contêm 12 casos. Nenhum arquivo de conteúdo foi reescrito.

## 3. Componentes previstos (SYNTHESIS seção 4) versus existentes

Verificado por listagem de arquivos e comparação com `SYNTHESIS.md` (4.2 a 4.8) e `plugin-blueprint.md`.

| Componente previsto | Situação |
| --- | --- |
| Skills de tarefa (9) e skill `playbook` | Presentes: 10 de 10 |
| Skill `prompts` com `references/prompt-library.md` | Presente |
| `prompts/references/` com 4 arquivos por subtema (`prompts-revisao.md`, `prompts-debug.md`, `prompts-refatoracao.md`, `prompts-legado-e-divida.md`) | Ausentes. `prompt-library.md` (656 linhas) contém os 34 IDs PL-01 a PL-34. Nenhuma referência quebrada, porque a skill não cita esses arquivos. Não bloqueante (o blueprint diz "se grande"). |
| 12 referências do `playbook/references/` | Presentes: 12 de 12 |
| 10 templates em `playbook/assets/templates/` | Presentes: 10 de 10 |
| 5 agentes | Presentes: 5 de 5 |
| 10 casos de eval previstos + `evals/README.md` + `evals/.gitignore` | Presentes, mas com 12 casos (ver item 4) |
| Hooks, `.mcp.json`, `.lsp.json`, `bin/`, `commands/` | Ausentes de propósito (política de segurança) |

## 4. Pendências (remaining)

Inferido, a partir da comparação com o plano. Nada disto é erro estrutural.

1. **Número de casos de eval.** O plano (`SYNTHESIS.md` 4.8) prevê 10 casos e diz que alternativas "entram substituindo um caso, não somando". O `plugin-blueprint.md` limita a 6 a 10 casos. O plugin tem 12: `prompts-revisao-adversarial` e `review-android-lifecycle-batch` foram acrescentados. Decisão necessária: remover dois casos para voltar ao plano, ou ajustar o blueprint para 12. Não alterei.
2. **Subtemas da biblioteca de prompts.** Os quatro arquivos previstos em `prompts/references/` não existem (ver item 3). Decisão: criar, ou registrar que `prompt-library.md` basta.
3. **Modelo dos agentes.** O `SYNTHESIS.md` 4.4 prevê `model: sonnet` (e `haiku` para `finding-validator` como Suposição). Os cinco agentes usam `model: inherit`. O formato aceita `inherit`, então não é erro, mas diverge do plano. Ajuste por custo deve ser medido nos evals.
4. **Cobertura de evals.** Segundo `evals/README.md`: nenhum caso próprio para `finding-validator`, `debugger`, `refactor-planner` e `codebase-mapper`; nenhum caso de disparo para `simplify-safe`; nenhum caso para o modo `QUALIDADE-COMPLETO`. Esses pontos já estão declarados no README do eval.
5. **Evals não executados.** Os 12 casos estão como `designed_not_executed`. Executar exige Claude Code 2.1.269 ou superior; a versão local registrada na fundação é 2.1.128. Isso é tarefa do validador de qualidade, não do estrutural.
6. **Referências a fontes externas por nome.** `testes-e-debugging.md` aparece como crédito ao repositório `brain-of-agent` em três lugares. Não é link quebrado, e a fonte está em `fontes.md` (item 19). Não exige ação.

## 5. Limites desta verificação

- Este relatório cobre apenas estrutura: existência de arquivos, frontmatter, links, JSON, política de segurança e coerência de nomes e contagens.
- Não avaliou a qualidade do conteúdo, a pontuação de prompt (meta ≥ 80) nem a licença dos trechos de terceiros. Isso cabe ao validador de qualidade.
- Não há `commands/`; por isso não houve verificação de comandos.
- Nenhum eval foi executado.

## 6. Próximo passo

Passar o plugin ao validador de qualidade, com as pendências 1 e 2 decididas pelo usuário antes disso.
