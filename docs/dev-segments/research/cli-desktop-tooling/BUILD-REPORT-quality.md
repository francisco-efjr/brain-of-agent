# BUILD-REPORT qualidade: cli-desktop-tooling

Data: 2026-10-10. Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\cli-desktop-tooling`.
Papel: validador de qualidade de prompt e conteúdo técnico (rubrica D1 a D12, 0 a 100).

Independência: os construtores foram outro modelo, mas o validador é da mesma família de modelos de linguagem. As notas abaixo são autoavaliação de família, não validação humana nem execução dos evals (`designed_not_executed`).

## 1. Escopo lido

- Lidos integralmente: `README.md`, `evals/README.md`, os 10 `SKILL.md`, os 5 agentes, `prompt-library.md` (P-01 a P-22), `prompts-dx-claude.md` (P-23 a P-27, P-29, P-30), `prompts-sistema.md` (P-28), os 14 casos de eval (`prompt.md` e `graders/`).
- Amostrados (cabeçalho, trechos de risco, buscas): `fontes.md`, `claude-md-snippets.md`, `ferramentas-e-mcp.md`, `desktop-stacks-e-seguranca.md`, `electron.md`, `ficha-de-acao-externa.md`. As demais referências foram verificadas por busca de placeholders, segredos, CAPS e recomendação de bypass de permissões (nenhum achado).
- Busca automática: nenhum `TODO`, `TBD`, placeholder vazio, segredo literal, `--dangerously-skip-permissions` recomendado (só aparece como risco) nem CAPS de ameaça.

## 2. Notas antes e depois

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 90 | 91 | Gotcha 2: `OnlyLoadAppFromAsar` deixou de ser "deve" e passou a recomendação da fábrica (Inferido) |
| `skills/prompts/SKILL.md` | 88 | 89 | Gotcha 3 alinhada (fuse) |
| `skills/cli-design-review/SKILL.md` | 90 | 90 | Nenhuma necessária |
| `skills/tui-review/SKILL.md` | 88 | 88 | Nenhuma necessária |
| `skills/desktop-stack-decision/SKILL.md` | 89 | 89 | Nenhuma necessária |
| `skills/dotnet-desktop-review/SKILL.md` | 87 | 87 | Nenhuma necessária |
| `skills/desktop-security-audit/SKILL.md` (+ `references/electron.md`) | 86 | 90 | Fuses: "valor seguro" sem sustentação trocado por recomendação da fábrica; `EnableEmbeddedAsarIntegrityValidation` vale para macOS e Windows; `EnableCookieEncryption` é de mão única |
| `skills/desktop-release-checklist/SKILL.md` | 89 | 89 | Nenhuma necessária |
| `skills/shell-script-review/SKILL.md` | 90 | 90 | Nenhuma necessária |
| `skills/dx-audit/SKILL.md` | 87 | 87 | Nenhuma necessária |
| `agents/cli-ux-reviewer.md` | 86 | 89 | Rótulos epistêmicos alinhados às skills (o que o arquivo diz é Verificado; comportamento em execução é Inferido) |
| `agents/desktop-security-auditor.md` | 85 | 90 | Removida a frase "correção do validador" (vazamento do processo de construção); fuses alinhados |
| `agents/diff-gap-reviewer.md` | 91 | 91 | Nenhuma necessária |
| `agents/release-readiness-auditor.md` | 90 | 90 | Nenhuma necessária |
| `agents/script-reviewer.md` | 90 | 90 | Nenhuma necessária |
| `skills/prompts/references/prompt-library.md` (22 prompts) | 88 | 91 | P-01: rótulos Verificado/Inferido alinhados; P-09: "20 itens" listava só 16, agora manda percorrer as 20 recomendações e cita HTTPS/WSS, recursos experimentais e `will-attach-webview` |
| `skills/prompts/references/prompts-dx-claude.md` (7 prompts) | 87 | 88 | P-23: "CADA" em maiúsculas trocado por minúsculas |
| `skills/prompts/references/prompts-sistema.md` (P-28) | 90 | 90 | Nenhuma necessária |
| `evals/*` (14 casos; média) | 86 | 86 | Dois graders `llm` sem CAPS ("TODOS", "E"); formato conferido na página oficial (ver 3) |
| `evals/README.md` | 90 | 90 | Nenhuma necessária |
| `README.md` | 88 | 88 | Nenhuma necessária |
| Outras referências e templates (fontes, snippets, templates; fuses) | n/a | n/a | `fontes.md` C-2, `desktop-stacks-e-seguranca.md`, `padroes-e-antipadroes.md` AP-12, template `relatorio-auditoria-desktop.md`: rótulo de `OnlyLoadAppFromAsar` Verificado para Inferido |

Média antes: 87,4. Média depois: 88,0. Mínimo depois: 86 (grupo de evals). Nenhum item abaixo de 80; nenhum critério de reprovação automática encontrado.

Pontuação por dimensão (resumo, vale para o conjunto): D1 5, D2 5 (razão de cada regra), D3 5, D4 4 a 5, D5 4 (exemplos presentes nas skills de tarefa, ausentes nos agentes), D6 5, D7 5, D8 5, D9 3 a 4 (densidade alta; "Gotchas" e "Ressalvas" repetem `fontes.md`), D10 5, D11 5 (modo sem interação nos agentes), D12 4 a 5 (uma recomendação rotulada como verificada sem sustentação foi corrigida).

## 3. Fidelidade técnica (WebFetch em 2026-10-10)

| Afirmação | Fonte | Resultado |
| --- | --- | --- |
| Nove fuses do Electron e seus padrões | https://www.electronjs.org/docs/latest/tutorial/fuses | Confere a lista. **Correção:** a página não recomenda `OnlyLoadAppFromAsar` ligado de forma geral (associa-o à validação de integridade); o plugin dizia "deve ficar ligado" e rotulava Verificado. Agora é recomendação da fábrica, Inferido. `EnableEmbeddedAsarIntegrityValidation` vale para macOS e Windows (o plugin dizia só macOS). `EnableCookieEncryption` é de mão única (acrescentado). |
| Tauri v2: capabilities por rótulo, `remote.urls`, `AppManifest::commands`, todos os comandos acessíveis por padrão, iframe em Linux e Android | https://v2.tauri.app/security/capabilities/ | Confere. |
| Textual: `priority=True` é checado antes do widget e não pode ser desativado por ele; `show=False` só controla o rodapé | https://textual.textualize.io/guide/input/ | Confere. A página não diz se a descrição do `Binding` é obrigatória: o plugin trata "sem descrição" como achado de usabilidade, o que segue válido. |
| `Build` e `Deploy` são verbos do PowerShell 6 em diante; `Delete` é sinônimo a evitar | https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands | Confere (`Build` também aparece como sinônimo a evitar de `New`). |
| WinUI 3 recomendado para novos apps, Windows 10 1809 ou posterior | https://learn.microsoft.com/en-us/windows/apps/winui/winui3/ | Confere. |
| Campos de `prompt.md` (`name`, `description`, `tags`, `runs`, `expected_outcome`, `model`, `max_turns`, `timeout_seconds`, `allowed_tools`) e graders `regex` (`flags`, `target`) e `tool_used` (`input_match`, `min`, `max`, `arm`) | https://code.claude.com/docs/en/plugin-evals | Confere; chave desconhecida seria erro e não há nenhuma. |
| `claude -p`: stdin até 10 MB, `--bare`, 143, `plugin_errors` | `VALIDATED.md` V-09; `onFailure` v2.1.295 em `docs/research/automation-integrations` | Confere com as fontes do repositório (não reconsultado na web). |
| Assinatura Windows (EV, SmartScreen, Azure Artifact Signing) | `VALIDATED.md` V-44 | Consistente; não reconsultado na web nesta rodada. |

## 4. Direitos autorais e segurança

- Literal de terceiros: apenas a mensagem inicial do brain-of-agent (MIT, do próprio usuário, atribuída em P-28A). Rubrica de DX do gstack reescrita, com atribuição (MIT). Sem cópia sem licença.
- Segredos: nenhum literal; exemplos usam senha de ilustração dentro de casos de eval e a ficha manda não colar segredo.
- Fluxos de ação externa: todos exigem ficha e confirmação do usuário; nenhum prompt ou skill autoriza assinar, notarizar, publicar, instalar ou fazer push sem confirmação nomeada. `--dangerously-skip-permissions` só aparece como risco (sandbox, repositório confiável).
- Agentes revisores: `tools: Read, Grep, Glob` (sem Write, Edit, Bash).
- Evals: graders com PASS/FAIL observáveis; há dois negativos (SQL e AWS CLI, `min: 0`, `max: 0`, `arm: both`) e dois casos de escopo e segurança (notarização e injeção em README). O arquivo `readme-injection-dx/prompt.md` contém, de propósito, uma "nota para assistentes de IA" como isca de teste; foi tratada como dado.

## 5. Pendências do validador estrutural: resolução

1. Prompts previstos em `prompts-cli-tui`, `prompts-desktop`, `prompts-release`, `prompts-scripts`: a consolidação em `prompt-library.md` cobre os temas (CLI e TUI em P-01 a P-08, desktop em P-09 a P-13, release em P-14 a P-18, scripts em P-19 a P-22) e o índice da skill `prompts` aponta cada ID ao arquivo certo. Decisão: manter consolidado; separar seria só divisão de arquivo, sem conteúdo novo.
2. Conteúdo dos 14 evals: revisado; formato conferido na página oficial. Continuam `designed_not_executed`.
3. Marketplace de instalação: o README usa `francisco-efjr/brain-of-agent` e `@brain-of-agent`, igual aos demais plugins de `dev-segments\plugins`. Mantido por consistência; o SYNTHESIS previa `@dev-segments`. Decisão do usuário quando o marketplace for publicado (não existe `marketplace.json` na raiz).

## 6. Pendências abertas

- Rodar `claude plugin eval` (exige Claude Code 2.1.269 ou posterior; o CLI local era 2.1.128) e ler as transcrições; nenhuma nota de eval existe.
- Sem eval para `prompts`, `dx-audit` e para quatro dos cinco agentes (cobertos indiretamente). Acrescentar casos mudaria as contagens de 14 documentadas no README e no `evals/README.md`.
- Densidade (D9): "Gotchas" e "Ressalvas e lacunas" das skills repetem `fontes.md`; encurtar reduziria tokens, mas exige reteste de disparo dos evals.
- Revisão independente de outro modelo ou de pessoa continua recomendada; fatos de assinatura (V-44), `claude -p` e Qt não foram reconsultados na web nesta rodada.
- A skill `desktop-security-audit` mantém os valores de fuse como Inferido: reconferir a página de fuses do Electron na versão do app auditado.

## 7. Verificação final

| Verificação | Resultado |
| --- | --- |
| `python tools/verify_plugin.py plugins/cli-desktop-tooling` | PASS (10 skills, 5 agentes, 14 evals, 111 arquivos) |
| `claude.exe plugin validate plugins/cli-desktop-tooling` | Validation passed |
