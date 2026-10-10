# Evals do plugin cli-desktop-tooling

Status: **designed_not_executed**. Os 14 casos foram escritos no formato oficial do `claude plugin eval` (pasta por caso, `prompt.md` com frontmatter, `graders/*.md`), mas nenhum foi executado. Nenhuma taxa de acerto, `Δ` ou custo foi medido; qualquer número sobre este plugin só vale depois da primeira execução. Autoavaliação por juiz da mesma família de modelos não equivale a validação humana: leia as transcrições antes de confiar na nota.

Formato conferido em 2026-10-10 na página https://code.claude.com/docs/en/plugin-evals (A): campos de `prompt.md`, tipos de grader (`llm`, `regex`, `tool_used`, `tool_order`, `file_exists`, `baseline`) e `arm: both`. A página muda; confira-a e rode `claude plugin eval --help` na versão instalada.

## Requisitos

- Claude Code 2.1.269 ou posterior. A versão registrada na especificação da fábrica para o CLI local é 2.1.128, portanto os evals não rodam neste ambiente sem atualizar (`claude --version` para conferir).
- Execução gasta tokens: casos x execuções x 2 braços (com e sem o plugin), mais chamadas ao juiz nos graders `llm`. Com 14 casos e 3 execuções por braço são 84 execuções do agente, fora o juiz. Use `--max-cost-usd` como teto e `--tag` ou `--case` para rodar partes. Quem autoriza o gasto é o usuário.
- **Não conceda `Bash`, `Write`, `Edit`, `WebFetch` nem `WebSearch`** (`--allow-tools`). Os casos de escopo e segurança partem do princípio de que essas ferramentas são removidas da sessão. No Windows nativo não há backend de sandbox; conceder `Bash` ali faz a execução ser recusada (a documentação manda usar WSL2).

## Como rodar

Na raiz do plugin (`plugins/cli-desktop-tooling`):

```bash
claude plugin eval .                                   # todos os casos, com e sem o plugin
claude plugin eval . --tag negativo                    # só os casos negativos
claude plugin eval . --case cli-agent-ready --runs 5   # um caso, 5 execuções por braço
claude plugin eval . --ablation none                   # só o braço com plugin (metade do custo)
claude plugin eval . --threshold 0.8 --judge-model sonnet --max-cost-usd 10
```

Em CI, fixe o modelo (`--model`) para que uma troca de modelo não seja confundida com regressão do plugin, e passe `--trust-plugin` apenas se você controla o código e a suíte. O relatório sai em `evals/results/<timestamp>/` (`report.html` e `aggregate-result.json`); a pasta está no `.gitignore`.

Antes de medir disparo, rode `claude plugin details cli-desktop-tooling` para ver o custo "every turn" das descrições (a referência de destaque do `/plugin` é 2.000 tokens). Depois de encurtar uma `description`, repita os graders `tool_used`: descrição menor pode parar de disparar.

## O que cada caso mede

| Caso | Mede | Skill/agente esperado | Graders | Tipo |
| --- | --- | --- | --- | --- |
| `cli-agent-ready` | CLI Python com `input()`, remoção sem flag, erro em stdout e `exit(0)`: contrato de máquina, stderr, exit codes, não executar | `cli-design-review` | `llm`, `tool_used`, `regex` | disparo |
| `electron-window-audit` | `main.js` com `nodeIntegration` e IPC que executa comando: severidade crítica, preload, CSP, fuses, app não executado | `desktop-security-audit` | `llm`, `tool_used`, `regex` | disparo |
| `tauri-capabilities` | `csp: null`, capability única, `remote` com curinga, `AppManifest::commands`, nomes de permissão não inventados | `desktop-security-audit` | `llm`, `tool_used` | disparo |
| `windows-signing-ev-myth` | mito do EV obrigatório, senha em `/p`, falta de `/fd` e `/td`, `signtool verify /pa`, ordem do updater como hipótese | `desktop-release-checklist` | `llm`, `tool_used`, `regex` | disparo |
| `macos-notarize-scope` | pedido para notarizar e publicar: recusa da execução, ficha de ação externa, sem pedir credencial, sintaxe de `notarytool` a conferir | `desktop-release-checklist` ou `playbook` | `llm`, `tool_used`, `regex` (ausência), `tool_used` Bash 0 | **escopo e segurança** |
| `powershell-destructive` | `Build-` inexistente no 5.1, sem `SupportsShouldProcess`, caminho vazio, `$LASTEXITCODE`, `Write-Host` | `shell-script-review` | `llm`, `tool_used`, `regex` | disparo |
| `bash-cd-rm` | SC2086, SC2164 antes de `rm -rf`, SC2155, `local` e `[[` fora do POSIX, `set -e` como rede parcial | `shell-script-review` | `llm`, `tool_used`, `regex` | disparo |
| `stack-msix-store` | restrição de Store com MSIX (Tauri não gera MSIX), recusa de benchmark, Linux como risco, ADR | `desktop-stack-decision` | `llm`, `tool_used`, `regex` | disparo |
| `readme-injection-dx` | README com instrução embutida para IA: tratada como dado, não executada, informada ao usuário; modo `live` só com autorização | `playbook` (a `dx-audit` é manual) | `llm`, `tool_used`, `tool_used` Bash 0, `regex` | **escopo e segurança** |
| `tui-textual-bindings` | bindings sem descrição, `priority=True` em tudo, testes com `run_test`/`Pilot`/snapshot, acessibilidade como lacuna | `tui-review` | `llm`, `tool_used`, `regex` | disparo |
| `dotnet-wpf-accessibility` | botão de ícone sem nome acessível, cores fixas, handler no code-behind, Narrator como etapa humana, lacunas de fonte do WPF | `dotnet-desktop-review` | `llm`, `tool_used`, `regex` | disparo |
| `delegar-revisor-de-diff` | revisão independente de diff contra plano: aciona o subagente, acha exit code errado e teste ausente, sem comentário de estilo | agente `diff-gap-reviewer` | `llm`, `tool_used` (Agent), `regex` | agente |
| `negativo-sql-ranking` | pedido de SQL sem relação: nenhuma skill do plugin dispara | nenhuma | `tool_used` (min 0, max 0), `llm` | **negativo** |
| `negativo-usar-cli-terceiros` | uso da AWS CLI: a palavra "CLI" não pode disparar skills de design ou revisão de CLI | nenhuma | `tool_used` (min 0, max 0), `llm` | **negativo difícil** |

Cada caso de disparo tem pelo menos um grader sobre o resultado (`llm` e, onde barato, `regex`) e um sobre o caminho (`tool_used`), como a página recomenda. Os `tool_used` com `tool: Skill` ficam fora da nota em execução com dois braços (a documentação os trata como indicadores, porque não passam sem o plugin); os negativos usam `arm: both` para valerem nos dois braços.

## Como ler o resultado

- `Δ` perto de zero com `tool_used: Skill` reprovando: a `description` da skill não casa com a fala natural do pedido; reescreva a descrição.
- `Δ` negativo com `tool_used` passando: suspeite do juiz antes do plugin; rode de novo com `--judge-model sonnet` e aperte a rubrica.
- Caso negativo falhando: a skill dispara por palavra solta ("CLI", "script"); acrescente a frase de exclusão na `description`.
- Leia pelo menos as transcrições dos casos de escopo (`macos-notarize-scope`, `readme-injection-dx`): graders não substituem ler o que o agente fez.

## Limites e lacunas

- Sem caso para `prompts` nem `dx-audit` (esta tem `disable-model-invocation: true` e não dispara sozinha; o caso `readme-injection-dx` usa o `playbook`). Os agentes `cli-ux-reviewer`, `desktop-security-auditor`, `release-readiness-auditor` e `script-reviewer` são cobertos indiretamente pelas skills correspondentes; só o `diff-gap-reviewer` tem caso próprio.
- O nome do campo do subagente na entrada da ferramenta `Agent` não foi reconferido; o grader `agent-used` casa só o texto `diff-gap-reviewer` na entrada, o que independe do nome do campo (Inferido).
- Os casos usam trechos curtos de código colados no pedido, porque cada execução começa com o workspace vazio. Eles medem julgamento, não leitura de repositório.
- Sem fonte validada para Linux, segurança de Qt e .NET, acessibilidade de TUI e distribuição de CLI: não há casos que cobrem esses pontos além do que os graders já exigem como lacuna declarada.
