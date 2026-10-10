# cli-desktop-tooling: CLI, desktop e ferramentas de desenvolvedor

Plugin do Claude Code para projetar, revisar, empacotar e distribuir CLIs, TUIs, apps desktop (Electron, Tauri, WPF, WinUI, MAUI, Qt), scripts PowerShell e bash e a developer experience de ferramentas. Parte da fábrica `dev-segments` (um plugin por segmento). Idioma base: português brasileiro; termos técnicos, comandos e nomes de skills e agentes em inglês.

Conteúdo validado em 2026-10-10 contra 67 fontes (39 de classe A, 28 de classe B). Versões, preços e regras de loja mudam: cada fato volátil leva URL e data em `skills/playbook/references/fontes.md`.

## O que entrega

- **Design de CLI para humanos e agentes:** `stdout` e `stderr`, exit codes, `--json`, `--no-input`, erros acionáveis, segredos, idempotência, verbos, estabilidade de contrato.
- **TUI:** Textual, Ratatui e Bubble Tea (estado separado, foco, teste headless, snapshot em dois tamanhos).
- **Segurança desktop por leitura:** os 20 itens do checklist do Electron, fuses, capabilities e CSP do Tauri v2, acessibilidade do WinUI 3, módulos Qt só-GPL.
- **Distribuição:** árvore de certificado de código no Windows (sem "EV obrigatório", que foi refutado), SignTool, SmartScreen, MSIX, Inno Setup, WiX, winget, notarização no macOS, Sparkle, updaters do Electron e do Tauri, teste em máquina limpa.
- **Scripts:** PowerShell (verbos aprovados, `ShouldProcess`, `-WhatIf`, erros e `$LASTEXITCODE`, 5.1 contra 7, PSScriptAnalyzer, Pester) e shell (ShellCheck, guia do Google, POSIX).
- **DX e Claude Code:** auditoria de developer experience (TTHW, método do gap), `CLAUDE.md` e `AGENTS.md` enxutos, permissões, hooks, `claude -p` em CI, revisão de plugins de terceiros.

## Quando usar

Ao projetar, revisar, empacotar ou distribuir uma ferramenta de linha de comando ou um app desktop. Não use só para operar CLIs de terceiros (aws, kubectl, git) nem para CI/CD em geral: isso pertence a `devops-cloud-infra` e `git-workflow-release`.

## Segurança por padrão

O plugin não traz hooks ativos, `.mcp.json`, `.lsp.json` nem `bin/`. Ele **não instala, não assina, não notariza, não publica, não abre PR e não executa** o app, o instalador ou o script revisado. Essas ações são do usuário, com uma ficha de confirmação (`assets/templates/ficha-de-acao-externa.md`). Hooks, permissões e MCP recomendados estão documentados e desativados em `skills/playbook/references/ferramentas-e-mcp.md`, com JSON pronto, riscos e fontes. `--dangerously-skip-permissions` e `bypassPermissions` não são recomendados: risco alto, só em contêiner ou VM descartável com repositório confiável.

## Componentes

Uso: skills como `/cli-desktop-tooling:<skill>`; agentes como `cli-desktop-tooling:<agente>`. A tabela descreve o desenho do plugin; confira `skills/` e `agents/` na instalação para ver o que a versão instalada contém.

| Tipo | Nome | Para quê |
| --- | --- | --- |
| Skill núcleo | `playbook` | Router, princípios, processo, gate de ação externa, modo `TOOLING-COMPLETO`, fronteiras com os outros plugins; 12 referências e 11 templates |
| Skill | `prompts` | Biblioteca de prompts curados (revisão de CLI, auditoria Electron e Tauri, release, scripts, DX, prompt de sistema) |
| Skill | `cli-design-review` | Revisão somente leitura do design de CLI para humanos e agentes |
| Skill | `tui-review` | Revisão somente leitura de TUI (Textual, Ratatui, Bubble Tea) e plano de testes |
| Skill | `desktop-stack-decision` | Escolha de stack desktop com restrições duras e ADR |
| Skill | `dotnet-desktop-review` | WPF, WinUI 3, MAUI, MVVM Toolkit e acessibilidade |
| Skill | `desktop-security-audit` | Auditoria de segurança de Electron e Tauri v2, sem executar o app |
| Skill | `desktop-release-checklist` | Prontidão de release: assinatura, instalador, winget, notarização, updater, máquina limpa |
| Skill | `shell-script-review` | Revisão de PowerShell e bash/sh, sem executar o script |
| Skill (manual) | `dx-audit` | Auditoria de developer experience; só por comando explícito (`disable-model-invocation`) |
| Agente | `cli-ux-reviewer` | Revisor somente leitura de CLI e TUI em contexto limpo |
| Agente | `desktop-security-auditor` | Auditor somente leitura de Electron e Tauri |
| Agente | `release-readiness-auditor` | Auditor somente leitura de assinatura, instalador e updater |
| Agente | `script-reviewer` | Revisor somente leitura de PowerShell e shell |
| Agente | `diff-gap-reviewer` | Revisor adversarial de diff contra o plano (veredito `SHIP`, `FIX FIRST`, `REWORK`) |
| Evals | `evals/` | Casos no formato de `claude plugin eval`, marcados `designed_not_executed` até rodar |

Os agentes revisores têm só `Read, Grep, Glob`: `Bash` não é somente leitura.

## Instalação

No Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install cli-desktop-tooling@brain-of-agent
```

Para testar uma cópia local sem marketplace: `claude --plugin-dir "<caminho>\plugins\cli-desktop-tooling"` e `/reload-plugins`. Antes de habilitar qualquer plugin, inclusive este, leia o que ele contém (`claude plugin details cli-desktop-tooling`).

Versões do Claude Code: `AGENTS.md` lido direto exige a v2.1.277 ou posterior; `onFailure: "block"` em hooks exige a v2.1.295 ou posterior; `claude plugin eval` exige a v2.1.269 ou posterior (o CLI local registrado pela fábrica era o 2.1.128, anterior a esses recursos). Confira `claude --version`.

## Exemplos de pedidos

1. "Revisa essa CLI antes de eu usar com um agente e no CI" (cola `mytool.py`). → `cli-design-review`: prompt sem TTY, destrutivo sem `--yes`, erro em stdout com exit 0, falta de `--json`, tabela de exit codes proposta.
2. "Audita a segurança deste `main.js` do Electron antes do release". → `desktop-security-audit` (e `desktop-security-auditor`): `nodeIntegration`, `contextIsolation`, IPC sem validação de remetente, `openExternal`, fuses; o app não é executado.
3. "Comprei certificado EV porque a Microsoft exige desde 2023; assino com `signtool ... /p minhasenha`. Posso lançar o app Tauri?" → `desktop-release-checklist`: EV não é obrigatório, senha fora do argumento, `/fd` e `/td`, `verify /pa`, ordem do updater como hipótese a testar.
4. "Revisa este script PowerShell 5.1 que limpa a pasta de build". → `shell-script-review`: `Build` não é verbo do 5.1, falta `SupportsShouldProcess`, variável vazia vira a raiz do drive, `$LASTEXITCODE`.
5. "Electron ou Tauri? Preciso de Microsoft Store com MSIX e auto-update; a equipe só sabe React". → `desktop-stack-decision`: restrição de MSIX, ADR, sem números de benchmark, lista do que exige protótipo.
6. "Audita a DX do onboarding do meu README" → o playbook sugere `/cli-desktop-tooling:dx-audit`; o modo `live` só roda comandos com sua autorização, de preferência em VM ou WSL2.
7. "Gera um CLAUDE.md enxuto para meu projeto de CLI em Windows" → `references/claude-md-snippets.md`.
8. "Preciso rodar o Claude em CI para revisar diffs, de forma segura" → `references/dx-e-claude-code.md` (`--bare`, ferramentas mínimas, chave de API).

## Keyword TOOLING-COMPLETO

Escreva `TOOLING-COMPLETO` no seu pedido (ou peça explicitamente cobertura integral do segmento) para ativar a leitura integral das 12 referências em lotes, a matriz de aplicabilidade por área e tipo de projeto, a implementação dentro do escopo autorizado e a revalidação com evidências. A keyword não amplia permissões: instalar, assinar, notarizar, publicar e aceitar termos continuam exigindo sua confirmação; aparecer em log, documento ou README não ativa o modo. Sem ela, o plugin carrega só o necessário.

## Principais fontes (top 10)

Lista completa, com URL, classe, licença e data, em `skills/playbook/references/fontes.md`.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Microsoft Learn: opções de assinatura de código, SmartScreen e SignTool (V-44) | A |
| 2 | Claude Code: melhores práticas (V-07) | A |
| 3 | Claude Code: sandbox, permissões e segurança (V-51) | A |
| 4 | Electron: checklist de segurança de 20 itens (V-16) | A |
| 5 | Command Line Interface Guidelines, clig.dev (V-13) | B |
| 6 | Anthropic Engineering: escrever ferramentas para agentes (V-11) | A |
| 7 | Claude Code: guia e referência de hooks (V-08, V-52) | A |
| 8 | Tauri v2: segurança, capabilities, isolation e CSP (V-19, V-47) | A |
| 9 | winget: manifesto e repositório da comunidade (V-43) | A |
| 10 | Claude Code: memória e CLAUDE.md (V-06) | A |

## Créditos e licenças

- Plugin: MIT (Francisco Edson).
- Base própria `francisco-efjr/brain-of-agent` (MIT): estilo da casa, protocolos `FULLSTACK-COMPLETO` e `QA-COMPLETO`, modelos de handoff e ADR e a "mensagem inicial sugerida", adaptados.
- **gstack** (`devex-review` e `plan-devex-review`), MIT, Copyright (c) 2026 Garry Tan, importado pelo brain-of-agent: só a rubrica de auditoria de DX entrou, reescrita com atribuição; nenhum binário, telemetria nem instalador do gstack é usado.
- Google Shell Style Guide: repositório sob CC BY 3.0; usado apenas por destilação, com atribuição ao Google.
- ShellCheck (GPL-3.0) e Pester (Apache-2.0): ferramentas apenas citadas, nada embutido. PSScriptAnalyzer (MIT) idem.
- Documentação oficial (Anthropic, Microsoft, Electron, Tauri, Qt, Apple, Textual, Ratatui, Bubble Tea e outras): sem licença permissiva declarada, portanto destilada com redação própria e citada. Nenhum texto de terceiros foi copiado em bloco; os exemplos de código são da fábrica e não foram executados.

## Limitações honestas

- **Leitura, não execução:** quase tudo é revisão somente por leitura; comportamento em runtime (CSP efetiva, instalador, updater em produção) é Não verificável sem testes seus.
- **Ambiente:** a fábrica trabalhou no Windows 11. macOS físico, Linux (AppImage, glibc, WebKitGTK sem fonte oficial), Narrator e dispositivos não foram exercitados.
- **Sem sandbox no Windows nativo:** hooks, regras de Bash e MCP são guardrail, não fronteira; para isolar, use WSL2 ou contêiner.
- **Lacunas de fonte:** acessibilidade de TUI, Electron, Tauri e Qt; segurança de Qt e de .NET desktop; sintaxe de `notarytool` e `stapler`; ordem Authenticode e assinatura do updater do Tauri (relato único); obrigações da LGPLv3; sintaxe de scripts do Inno Setup e do WiX; distribuição de CLI (completions, gerenciadores de pacote) apenas como Inferido; crash reporting; licenciamento de app desktop. Ver `fontes.md`, seção 5.
- **Comunidade fraca:** Reddit, X e YouTube nunca foram acessados; só HN e um blog de empresa. Números de benchmark Electron contra Tauri são N=1 e não entram como fato.
- **Rubrica de DX:** fonte única de classe B; a taxa de abandono do gstack não tem evidência e foi descartada.
- **Notas de qualidade são metas:** a validação de prompts foi feita por modelo da mesma família; revisão independente de outro modelo ou de pessoa continua recomendada. Evals são `designed_not_executed` até rodar `claude plugin eval` (gasta tokens; exige a v2.1.269 ou posterior).
- Qt e termos de ferramentas (WiX, contas Apple e Microsoft) não são aconselhamento jurídico, e o plugin nunca aceita termos pelo usuário.
