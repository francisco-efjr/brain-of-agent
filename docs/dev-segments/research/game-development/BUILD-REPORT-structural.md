# BUILD-REPORT estrutural: plugin game-development

Data: 2026-10-10. Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\game-development` (versão 0.1.0).
Papel: validação estrutural (não substitui o validador de qualidade de prompts nem a execução dos evals).

## 1. Resultado das verificações

| Verificação | Antes | Depois | Rótulo |
| --- | --- | --- | --- |
| `tools/verify_plugin.py` | PASS, 0 erros, 0 avisos (10 skills, 5 agentes, 0 comandos, 12 evals, 101 arquivos) | PASS, 0 erros, 0 avisos (10 skills, 5 agentes, 3 comandos, 12 evals, 104 arquivos) | Verificado |
| `claude plugin validate` (CLI 2.1.128) | Falhou em um comando novo: frontmatter YAML inválido em `commands/init-session.md` | "Validation passed" | Verificado |

O verificador determinístico não checa referências `/plugin:comando` nem o parse YAML de comandos. Por isso as duas falhas acima só apareceram por inspeção manual (referências) e pelo validador oficial (YAML).

## 2. Erros encontrados e corrigidos

1. **Comandos citados e inexistentes.** README (tabela de componentes, exemplo 7), `skills/playbook/SKILL.md` (tabela de intenção, linhas 95, 104 e 174), `skills/prompts/SKILL.md` (linha 45), `skills/prompts/references/prompt-library.md` (linha 299), `skills/playbook/references/verificacao-por-execucao.md` (linha 94) e `skills/game-qa-plan/SKILL.md` (linha 119) citavam `/game-development:verify`, `/game-development:init-session` e `/game-development:playtest-report`. A pasta `commands/` não existia. Correção: criados os três comandos finos previstos em `SYNTHESIS.md` 4.4.9:
   - `commands/verify.md` (atalho para `game-verify-by-running`);
   - `commands/init-session.md` (rotina de início de sessão, `allowed-tools: Read, Glob, Grep`; não grava nem executa script sem confirmação);
   - `commands/playtest-report.md` (atalho para `game-qa-plan` no modo `playtest-relatorio`, já previsto no `argument-hint` da skill).
2. **YAML inválido em `commands/init-session.md`.** A `description` continha `: ` dentro de plain scalar. Correção: valor entre aspas. Verificado pelo validador oficial.

Nenhum outro erro estrutural foi encontrado: nomes de pasta e `name` batem, frontmatter de skills e agentes usa só campos válidos, os `tools` dos agentes de revisão são somente leitura (`Read, Glob, Grep`; `game-evaluator` tem `Bash`, previsto por `SYNTHESIS` 4.5.4 para rodar só os comandos do contrato), `plugin.json` não declara diretórios padrão, não há hooks, `.mcp.json`, `.lsp.json` nem `bin/`, e os links relativos e as referências `${CLAUDE_PLUGIN_ROOT}/...` apontam para arquivos existentes (verificado por grep sobre todos os arquivos citados).

## 3. Comparação com o SYNTHESIS (seções 4.2 a 4.10)

| Componente previsto | Estado | Rótulo |
| --- | --- | --- |
| Skill `playbook` + 12 references + templates | Presentes (12 references; 19 templates, incluindo `matriz-aplicabilidade-gamedev.md`) | Verificado |
| Skill `prompts` + 4 arquivos em `references/` | Presentes | Verificado |
| 8 skills de tarefa (`game-verify-by-running`, `game-perf-audit`, `game-qa-plan`, `gdd-review`, `godot-gdscript`, `unity-csharp`, `unreal-cpp`, `game-netcode-review`) | Presentes, com `references/` | Verificado |
| 5 agentes (`game-engine-specialist`, `gameplay-programmer`, `gameplay-reviewer`, `game-evaluator`, `gdd-reviewer`) | Presentes | Verificado |
| 3 comandos (4.4.9) | Criados nesta execução | Verificado |
| 10 casos de eval + 2 reservas (4.10), `evals/README.md`, `evals/.gitignore` | Presentes (12 casos, README e .gitignore) | Verificado (existência) |
| `README.md` pt-BR com tabela de componentes | Presente; tabela cita só componentes existentes | Verificado |

Arquivos vazios ou placeholder: nenhum arquivo abaixo de 300 bytes com conteúdo de placeholder foi encontrado. Os menores são graders curtos e `evals/.gitignore`, que têm conteúdo funcional. Busca por `TODO`, `TBD`, `placeholder` e `lorem` retornou apenas usos legítimos (regras de veredito de agentes e campos de grader).

## 4. Pendências (não estruturais; ficam para o validador de qualidade e para a execução)

- **Evals não executados.** `evals/README.md` declara `designed_not_executed`. O comando `claude plugin eval` não existe na CLI local 2.1.128 (verificado pelo próprio README do eval, não repetido aqui); exige Claude Code 2.1.269 ou superior. Não verificado nesta execução.
- **Comportamento dos comandos novos não foi testado com o runtime.** O validador oficial só checa frontmatter e schema. Que `/game-development:verify`, `/game-development:init-session` e `/game-development:playtest-report` disparem o fluxo esperado é Não verificado.
- **Texto do README (linha 39)** ainda diz que skills, agentes e comandos "são escritos em paralelo" e pede para conferir a pasta instalada. Agora todos existem; a frase pode ser simplificada no próximo ciclo de edição de conteúdo. Não alterado nesta etapa (escopo estrutural).
- **Qualidade de conteúdo e prompt-score ≥ 80** (rubrica do blueprint) não foram avaliados aqui. Pertencem ao validador de qualidade.
- **Comandos finos** foram escritos a partir da especificação de `SYNTHESIS` 4.4.9. Ficam com redação própria e curta; revisão de conteúdo é pendência.
- **Marketplace** (`.claude-plugin/marketplace.json` na raiz) não foi conferido nesta etapa, por estar fora do plugin.

## 5. Como reproduzir

```text
python "C:\Users\Francisco Edson\dev-segments\tools\verify_plugin.py" "C:\Users\Francisco Edson\dev-segments\plugins\game-development"
"/c/Users/Francisco Edson/.local/bin/claude.exe" plugin validate "C:\Users\Francisco Edson\dev-segments\plugins\game-development"
```

Resultado final desta execução: verificador PASS (0 erros, 0 avisos) e validador oficial "Validation passed".
