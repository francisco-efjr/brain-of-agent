# Fontes validadas do segmento CLI, desktop e ferramentas de desenvolvedor

Verificado em 2026-10-10 (consulta feita por um validador de modelo diferente do pesquisador, sem executar nenhum comando de terceiros). Cada fonte tem um código `V-nn`; os demais arquivos de `references/` e as skills citam esses códigos. Classe A = fonte primária ou oficial; B = autor reconhecido ou repositório com sinais de uso; C = relato de praticante (nenhum item C sustenta regra neste plugin). A nota entre parênteses vai de 0 a 10. "Destilar" significa: a licença do texto não é permissiva ou não foi declarada, então o plugin usa redação própria e cita a fonte.

Sumário: 1. Como usar · 2. Fatos voláteis · 3. Bibliografia V-01 a V-67 · 4. Conflitos resolvidos · 5. Lacunas conhecidas · 6. Créditos e licenças.

## 1. Como usar

- Antes de citar versão, preço, região, prazo ou flag, abra a URL da fonte e confira a data da página (`ms.date` em páginas Microsoft Learn, "Last updated" no Tauri). A coluna "Consulta" informa quando o plugin foi validado, não quando a página mudou.
- Onde a tabela diz "sem data", trate a atualidade como desconhecida e confira a versão da ferramenta instalada (`--version`, `pip show`, `Get-Module`).
- Sintaxe de comando nunca vem só do plugin: use `--help` ou `/?` da versão instalada.

## 2. Fatos voláteis (reconferir antes de citar)

| Fato | Fonte | Observação |
| --- | --- | --- |
| Preço e regiões do Azure Artifact Signing, preço de OV, regras do CA/Browser Forum | V-44 | Lidos como estão na página em 2026; mudam |
| Regras do SmartScreen e do Smart App Control | V-44 | Reputação por certificado e por hash |
| WiX v7: EULA obrigatório e taxa OSMF (receita acima de US$ 10 mil) | V-42 | Decisão do usuário; o plugin nunca aceita |
| Versões mínimas do Claude Code por recurso (evals 2.1.269, `AGENTS.md` direto 2.1.277, `--permission-prompts none` 2.1.259, `onFailure: "block"` 2.1.295) | V-50, V-06, V-09, V-52 | O CLI local registrado na especificação da fábrica era 2.1.128; confira `claude --version` |
| Versão do Pester, `Should -Be` contra `Should-Be` | V-58 | O Windows traz o Pester 3.4.0 |
| Sparkle 2.9 (feed assinado, notas em Markdown) | V-49 | Confira a versão instalada |
| Lista dos 14 módulos Qt só-GPL | V-39 | Confira a página de licenciamento |
| Verbos `Build` e `Deploy` | V-14, V-60 | Existem a partir do PowerShell 6, não no 5.1 |
| Nomes de permissões do Tauri | V-19 | Variam por plugin e versão |

## 3. Bibliografia

| V | Título | URL | Classe | Licença | Consulta |
| --- | --- | --- | --- | --- | --- |
| V-01 | Claude Code: plugins, referência de plugins, repositório oficial de plugins | https://code.claude.com/docs/en/plugins · https://code.claude.com/docs/en/plugins-reference · https://github.com/anthropics/claude-plugins-official | A (9) | docs: destilar; repositório Apache-2.0 | 2026-10-10 |
| V-02 | Claude Code: segurança de plugins | https://code.claude.com/docs/en/plugins/security | A (9) | destilar | 2026-10-10 |
| V-03 | Claude Code: skills; repositório anthropics/skills | https://code.claude.com/docs/en/skills · https://github.com/anthropics/skills | A (9) | docs: destilar; repositório sem licença raiz detectada (README: Apache-2.0 em muitas skills; docx, pdf, pptx e xlsx são source-available) | 2026-10-10 |
| V-04 | Anthropic Engineering: equipar agentes com skills | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | A (9) | destilar | 2026-10-10 |
| V-05 | Lições de Thariq sobre skills (espelho de terceiro) | https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/tips/claude-thariq-tips-17-mar-26.md | B (7) | espelho MIT; texto do autor: destilar | 2026-10-10 |
| V-06 | Claude Code: memória e CLAUDE.md; melhores práticas | https://code.claude.com/docs/en/memory · https://code.claude.com/docs/en/best-practices | A (9) | destilar | 2026-10-10 |
| V-07 | Claude Code: melhores práticas (verificar, planejar, revisar) | https://code.claude.com/docs/en/best-practices | A (9) | destilar | 2026-10-10 |
| V-08 | Claude Code: guia de hooks | https://code.claude.com/docs/en/hooks-guide · https://code.claude.com/docs/en/hooks | A (9) | destilar | 2026-10-10 |
| V-09 | Claude Code: modo `-p` em scripts e CI | https://code.claude.com/docs/en/headless | A (9) | destilar | 2026-10-10 |
| V-10 | AGENTS.md (formato aberto) | https://agents.md/ | B (7) | não declarada: destilar | 2026-10-10 |
| V-11 | Anthropic Engineering: escrever ferramentas para agentes (2025-09-11) | https://www.anthropic.com/engineering/writing-tools-for-agents | A (9) | destilar | 2026-10-10 |
| V-12 | Armin Ronacher: agentic coding (2025-06-12) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | B (6) | sem licença: destilar | 2026-10-10 |
| V-13 | Command Line Interface Guidelines (clig.dev) | https://clig.dev/ | B (7) | sem licença declarada: destilar | 2026-10-10 |
| V-14 | PowerShell: verbos aprovados | https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands | A (8) | destilar | 2026-10-10 |
| V-15 | PowerShell: diretrizes de design de cmdlets | https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/strongly-encouraged-development-guidelines | B (7) | destilar | 2026-10-10 |
| V-16 | Electron: checklist de segurança (20 itens) | https://www.electronjs.org/docs/latest/tutorial/security | A (8) | sem licença declarada: destilar | 2026-10-10 |
| V-17 | Electron: assinatura de código (corrigida por V-44) | https://www.electronjs.org/docs/latest/tutorial/code-signing | A (8) | destilar | 2026-10-10 |
| V-18 | Electron: atualizações (autoUpdater) | https://www.electronjs.org/docs/latest/tutorial/updates | A (8) | destilar | 2026-10-10 |
| V-19 | Tauri v2: segurança e capabilities | https://v2.tauri.app/security/ · https://v2.tauri.app/security/capabilities/ | A (8) | destilar; página "Last updated: Jul 22, 2026" | 2026-10-10 |
| V-20 | Tauri v2: plugin updater | https://v2.tauri.app/plugin/updater/ | A (8) | destilar; sem data | 2026-10-10 |
| V-21 | Tauri: assinatura no Windows; relato Fluxzy sobre a ordem de assinatura | https://v2.tauri.app/distribute/sign/windows/ · https://www.fluxzy.io/resources/blogs/electron-to-tauri-migration-fluxzy-desktop | B (7) | destilar; ordem de assinatura é relato único | 2026-10-10 |
| V-22 | gstack `devex-review` (arquivo local do brain-of-agent) | https://github.com/garrytan/gstack · `docs/foundation/brain-of-agent-snapshot/vendor/gstack/devex-review/SKILL.md` | B (7) | MIT, Copyright (c) 2026 Garry Tan; só a rubrica, reescrita | 2026-10-10 |
| V-23 | Claude Code: subagentes; coleção VoltAgent | https://code.claude.com/docs/en/sub-agents · https://github.com/VoltAgent/awesome-claude-code-subagents | A (8) formato; B (7) coleção | docs: destilar; coleção MIT | 2026-10-10 |
| V-24 | wshobson/agents: validação em camadas | https://github.com/wshobson/agents | B (7) | MIT | 2026-10-10 |
| V-25 | cc-sdd: fases orientadas a especificação | https://github.com/gotalab/cc-sdd | B (7) | MIT | 2026-10-10 |
| V-26 | ECC: anti-padrões de instalação em massa | https://github.com/affaan-m/ECC | B (6) | MIT | 2026-10-10 |
| V-27 | Trail of Bits: claude-code-config | https://github.com/trailofbits/claude-code-config | B (6) | sem licença: só destilar | 2026-10-10 |
| V-28 | Ruler: fonte única de regras | https://github.com/intellectronica/ruler | B (6) | MIT; beta | 2026-10-10 |
| V-29 | Subagente de revisão com veredito (blog arps18, 2026-05-26) | https://arps18.github.io/posts/claude-code-mastery/ | B (6) | sem licença: destilar | 2026-10-10 |
| V-30 | Textual: input, foco e testes | https://textual.textualize.io/guide/input/ · https://textual.textualize.io/guide/testing/ · https://github.com/Textualize/textual | A (8) | MIT (repositório); páginas sem data | 2026-10-10 |
| V-31 | Ratatui: renderização, layout e snapshots | https://ratatui.rs/concepts/rendering/ · https://ratatui.rs/concepts/layout/ · https://ratatui.rs/recipes/testing/snapshots/ · https://github.com/ratatui/ratatui | B (7) | MIT | 2026-10-10 |
| V-32 | Bubble Tea e teatest | https://github.com/charmbracelet/bubbletea · https://pkg.go.dev/github.com/charmbracelet/bubbletea · https://pkg.go.dev/github.com/charmbracelet/x/exp/teatest | B (7) | MIT; `teatest` é experimental | 2026-10-10 |
| V-33 | WPF: visão geral | https://learn.microsoft.com/en-us/dotnet/desktop/wpf/overview/ | A (8) | destilar | 2026-10-10 |
| V-34 | MVVM Toolkit (CommunityToolkit.Mvvm) | https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/ · https://github.com/CommunityToolkit/dotnet | A (8) | MIT (arquivo License.md) | 2026-10-10 |
| V-35 | WinUI 3 e acessibilidade | https://learn.microsoft.com/en-us/windows/apps/winui/winui3/ · https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-overview | A (8) | destilar | 2026-10-10 |
| V-36 | Windows App SDK: empacotamento e implantação | https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/deploy-overview | A (8) | destilar | 2026-10-10 |
| V-37 | .NET MAUI: visão geral | https://learn.microsoft.com/en-us/dotnet/maui/what-is-maui | B (7) | destilar | 2026-10-10 |
| V-38 | Qt 6: implantação (`windeployqt`, `macdeployqt`) | https://doc.qt.io/qt-6/windows-deployment.html · https://doc.qt.io/qt-6/macos-deployment.html | B (7) | documentação GFDL 1.3: destilar | 2026-10-10 |
| V-39 | Qt: licenciamento | https://doc.qt.io/qt-6/licensing.html | B (7) | destilar; não é aconselhamento jurídico | 2026-10-10 |
| V-40 | MSIX e App Installer | https://learn.microsoft.com/en-us/windows/msix/overview · https://learn.microsoft.com/en-us/windows/msix/app-installer/app-installer-root | A (8) | destilar | 2026-10-10 |
| V-41 | Inno Setup | https://jrsoftware.org/ishelp/topic_whatisinnosetup.htm · https://jrsoftware.org/ishelp/topic_setup_signtool.htm | B (7) | licença própria permissiva; destilar | 2026-10-10 |
| V-42 | WiX: assinatura e OSMF | https://docs.firegiant.com/wix/tools/signing/ · https://docs.firegiant.com/wix/osmf/ | B (7) | destilar | 2026-10-10 |
| V-43 | winget: manifesto e repositório da comunidade | https://learn.microsoft.com/en-us/windows/package-manager/package/manifest · https://learn.microsoft.com/en-us/windows/package-manager/package/repository · https://github.com/microsoft/winget-pkgs | A (9) | docs: destilar; repositório MIT | 2026-10-10 |
| V-44 | Windows: opções de assinatura, SmartScreen e SignTool | https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options · https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation · https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool | A (9) | destilar | 2026-10-10 |
| V-45 | Notarização no macOS (Apple, Tauri, Qt) | https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution · https://v2.tauri.app/distribute/sign/macos/ · https://doc.qt.io/qt-6/macos-deployment.html | B (7) | destilar; sintaxe de `notarytool` e `stapler` não verificada | 2026-10-10 |
| V-46 | Tauri v2: assinatura, instaladores Windows e Store | https://v2.tauri.app/distribute/sign/windows/ · https://v2.tauri.app/distribute/windows-installer/ · https://v2.tauri.app/distribute/microsoft-store/ | A (8) | destilar; repositório Apache-2.0 | 2026-10-10 |
| V-47 | Tauri v2: isolation pattern e CSP | https://v2.tauri.app/concept/inter-process-communication/isolation/ · https://v2.tauri.app/security/csp/ | A (8) | destilar | 2026-10-10 |
| V-48 | Electron Fuses | https://github.com/electron/fuses | B (7) | MIT | 2026-10-10 |
| V-49 | Sparkle (auto-update no macOS) | https://sparkle-project.org/documentation/ · https://github.com/sparkle-project/Sparkle | A (8) | MIT | 2026-10-10 |
| V-50 | Claude Code: evals de plugin e medição de custo | https://code.claude.com/docs/en/plugin-evals · https://code.claude.com/docs/en/plugins/measure | A (9) | destilar | 2026-10-10 |
| V-51 | Claude Code: sandbox, permissões e segurança | https://code.claude.com/docs/en/sandboxing · https://code.claude.com/docs/en/permissions · https://code.claude.com/docs/en/security | A (9) | destilar | 2026-10-10 |
| V-52 | Claude Code: referência de hooks | https://code.claude.com/docs/en/hooks | A (9) | destilar; seção de privilégios não lida | 2026-10-10 |
| V-53 | Claude Code: criar plugin e componentes | https://code.claude.com/docs/en/plugins/create · https://code.claude.com/docs/en/plugins/components | A (9) | destilar | 2026-10-10 |
| V-54 | plugin-dev (Anthropic): agentes de validação | https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev | A (8) | Apache-2.0 (o README da pasta diz MIT; o arquivo LICENSE prevalece) | 2026-10-10 |
| V-55 | claude-code-setup, mcp-server-dev, skill-creator | https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup | A (8) | Apache-2.0 | 2026-10-10 |
| V-56 | Guia de prompting da plataforma Claude | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A (9) | destilar | 2026-10-10 |
| V-57 | PowerShell: ShouldProcess, -WhatIf, -Confirm, -Force | https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess | A (8) | destilar (texto original de Kevin Marquette, creditado pela página) | 2026-10-10 |
| V-58 | PSScriptAnalyzer e Pester | https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview · https://pester.dev/docs/quick-start · https://pester.dev/docs/introduction/installation | A (8) | PSScriptAnalyzer MIT; Pester Apache-2.0 | 2026-10-10 |
| V-59 | PowerShell: try/catch/finally, erros e variáveis de preferência | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally · https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling · https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables | A (8) | destilar | 2026-10-10 |
| V-60 | PowerShell 5.1 contra 7 | https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell | A (8) | destilar | 2026-10-10 |
| V-61 | ShellCheck: wiki de códigos SC | https://www.shellcheck.net/wiki/ · https://github.com/koalaman/shellcheck | A (8) | ferramenta GPL-3.0 (não embutir); wiki sem licença: destilar | 2026-10-10 |
| V-62 | Google Shell Style Guide | https://google.github.io/styleguide/shellguide.html | B (7) | repositório CC BY 3.0 (aqui só destilado) | 2026-10-10 |
| V-63 | POSIX.1-2017: Shell Command Language | https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html | B (6) | destilar | 2026-10-10 |
| V-64 | Guidelines do Azure CLI (com Heroku e Atlassian como sinal) | https://github.com/Azure/azure-cli/blob/dev/doc/command_guidelines.md · https://devcenter.heroku.com/articles/cli-style-guide · https://www.atlassian.com/blog/it-teams/10-design-principles-for-delightful-clis | B (7); Heroku C (4); Atlassian C (3) | Azure CLI MIT; demais destilar | 2026-10-10 |
| V-65 | DoltHub: Electron contra Tauri (2025-11-13) e discussão no HN | https://www.dolthub.com/blog/2025-11-13-electron-vs-tauri/ · https://news.ycombinator.com/item?id=46082291 | B (6) | destilar; N=1, nunca citar números como benchmark | 2026-10-10 |
| V-66 | skill-based-architecture (WoJiSama) | https://github.com/WoJiSama/skill-based-architecture | B (6) | MIT; não instalar | 2026-10-10 |
| V-67 | VoltAgent: catálogo e dois agentes lidos | https://github.com/VoltAgent/awesome-claude-code-subagents | B (7) catálogo | MIT; agentes lidos reprovados (`cli-developer` com métricas inventadas): não copiados | 2026-10-10 |

## 4. Conflitos resolvidos (usar esta resolução, não a fonte antiga)

| # | Conflito | Resolução | Rótulo |
| --- | --- | --- | --- |
| C-1 | "EV obrigatório desde junho de 2023" (Electron, V-17) contra Microsoft 2026 (V-44) | A Microsoft prevalece: em 2023 a mudança foi chave em HSM para OV; o bypass do SmartScreen pelo EV acabou em 2024. "EV obrigatório" está refutado | Verificado |
| C-2 | `OnlyLoadAppFromAsar` "desligado" (pesquisador) contra README de `@electron/fuses` (V-48) | O fuse restringe o carregamento ao `app.asar`; a fábrica recomenda ligado. A página de fuses do Electron (lida em 2026-10-10) não dá recomendação geral e o liga junto com a validação de integridade | Inferido |
| C-3 | `set -euo pipefail` como convenção do Google | O guia não recomenda `set -e` nem `pipefail`; `set -e` tem exceções no POSIX. É convenção própria, com aviso | Verificado |
| C-4 | Ordem Authenticode contra assinatura do updater do Tauri | Só relato único (V-21); páginas oficiais não tratam. Hipótese a testar em build descartável | Não verificável |
| C-5 | `plugin.json` obrigatório ou opcional | Opcional segundo a referência atual; o plugin adota sempre o manifesto | Verificado |
| C-6 | "CLI antes de MCP" (V-12) contra guia de ferramentas (V-11) | Complementares; CLI simples no ciclo local, MCP onde a alternativa é pouco confiável. Timeout padrão e caminho de log fixo são sugestões da fábrica | Inferido |
| C-7 | Números Electron contra Tauri (V-65) | Nunca citar como benchmark; só a matriz qualitativa | Inferido |
| C-8 | Bubble Tea "não reporta resize no Windows" | Não afirmar; testar no Windows | Não verificável |
| C-9 | ">10 min de TTHW = 50 a 70% de abandono" (gstack) | Sem evidência: usar as faixas como heurística, sem o número | Verificado (ausência) |
| C-10 | Revisor pedido para achar lacunas tende a achá-las | Filtro "correção ou requisito", lista "não sinalizar", veredito com "sem lacunas" | Verificado |
| C-11 | Subagente "somente leitura" com `Bash` | `Bash` não é somente leitura; revisores usam `Read, Grep, Glob` | Verificado |
| C-12 | `Build` e `Deploy` em PowerShell | Só do 6 em diante; no 5.1 use `Invoke-<X>Build`, `New-`, `Publish-`, `Install-` | Verificado |
| C-13 | Auditoria em `PreToolUse` contra `PostToolUse`; `exit 1` bloqueia | Auditoria em `PostToolUse`; só `exit 2` ou JSON `deny` bloqueia | Verificado |
| C-14 | Guardrails baseados em sandbox (macOS) contra Windows nativo | Windows nativo não tem sandbox; use deny rules, hooks como camada extra e WSL2 ou contêiner | Verificado |
| C-15 | MVVM Toolkit e MAUI | Ausência na lista não é incompatibilidade nem suporte confirmado | Verificado |
| C-16 | Pester 5 `Should -Be` contra documentação nova `Should-Be` | Conferir `Get-Module Pester -ListAvailable` | Verificado |
| C-17 | `AGENTS.md` contra `CLAUDE.md` | `CLAUDE.md` importa `AGENTS.md`; leitura direta do `AGENTS.md` só sem `CLAUDE.md`, a partir da v2.1.277 | Verificado |

## 5. Lacunas conhecidas (declare quando afetarem o trabalho)

1. Comunidade real (Reddit, X, YouTube, newsletters) nunca acessada: só HN pela API Algolia e um blog de empresa (V-65).
2. Acessibilidade de TUI sem fonte oficial lida nas três bibliotecas.
3. Sintaxe de `notarytool` e `stapler` não verificada.
4. Ordem Authenticode contra assinatura do updater do Tauri sem fonte oficial.
5. Qt: obrigações detalhadas da LGPLv3 e segurança do Qt sem fonte.
6. .NET desktop: acessibilidade do WPF, MVVM do MAUI e segurança sem fonte; geradores de código do MVVM Toolkit não lidos.
7. Inno Setup e WiX: sintaxe de scripts (`[Files]`, `[Run]`, `.wxs`), WiX v3 e v4, `insignia` e timestamp não lidos.
8. Claude Code: seção de privilégios dos hooks, semântica de `defer` e campos de `components` não lidos.
9. DX: a rubrica de onboarding (TTHW) tem fonte única de classe B (gstack).
10. Pester: `-CI`, `-PassThru`, mocks, Discovery contra Run não lidos.
11. POSIX: parte final da página não lida.
12. Corpos de `plugin-validator`, `skill-reviewer`, `claude-automation-recommender`, `build-mcp-server`, `skill-creator`, `electron-pro` e `skill-based-architecture` lidos só por resumo: nenhum texto deles foi reaproveitado.
13. Linux (AppImage, glibc, WebKitGTK) só por relato do HN; nada oficial.
14. Distribuição de CLI (completions, gerenciadores de pacote, binário único, self-update, telemetria com opt-in) sem item V: o bloco F de `cli-e-agentes.md` é Inferido.
15. Crash reporting e logs de app desktop, e stacks nativas sem WebView (GTK, AppKit, SwiftUI desktop, C++ com GUI próprio) sem fonte.
16. Nenhum MCP validado para CLI ou desktop; nenhuma fonte para driver de teste de Electron (Playwright e similares são Suposição).
17. Licenciamento e ativação de app desktop sem cobertura.

## 6. Créditos e licenças de terceiros

- gstack (`devex-review`, `plan-devex-review`): MIT, Copyright (c) 2026 Garry Tan, via snapshot do brain-of-agent (versão 1.91.27, commit `c285d88b90d39116ccfa2b901f80ea0fce0b26eb`, segundo `THIRD_PARTY_NOTICES.md` do snapshot). Só a rubrica entrou, reescrita; binários, telemetria e instalador não.
- brain-of-agent (`francisco-efjr/brain-of-agent`): MIT, conteúdo do próprio autor; protocolos `FULLSTACK-COMPLETO` e `QA-COMPLETO`, modelos de handoff e ADR e a "mensagem inicial sugerida" inspiraram o modo `TOOLING-COMPLETO` e os templates.
- Google Shell Style Guide: repositório sob CC BY 3.0 Unported; usado só por destilação, com atribuição ao Google.
- ShellCheck (GPL-3.0) e Pester (Apache-2.0): ferramentas apenas citadas, nada embutido.
- Nenhum trecho literal de documentação de terceiros sem licença permissiva foi copiado; exemplos de código são de autoria da fábrica, marcados como não executados.
