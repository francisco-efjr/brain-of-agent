# qa-playwright: validação funcional com Playwright para o Claude Code

Plugin do marketplace `brain-of-agent` para validar um sistema **funcionalidade por funcionalidade** com Playwright: abrir o app rodando, explorar cada ação de valor, codificar um spec que assere o **efeito** (não só a presença), provar que o spec é estável e registrar o resultado numa matriz com evidência. A ideia central: **"passou" só vale com execução e evidência, e onde o Playwright não se aplica a linha continua na matriz, com motivo e executor equivalente.** Versão 0.1.0, licença MIT. Português brasileiro; termos técnicos, comandos e nomes de skills e agentes em inglês.

## O que entrega

- **Inventário `F-NN`:** cada funcionalidade é uma ação de valor ("Excluir tarefa atualiza lista e contador") com ID estável, superfície, risco, camadas, cenários e o **esperado com a fonte dele**. Sem fonte, o esperado é Suposição e a falha vira decisão pendente, não bug afirmado.
- **Aplicabilidade por tipo de sistema** (23 linhas): web, login e papéis, API, GraphQL, WebSocket, PWA, extensão Chrome, componentes, Electron, Android Chrome e WebView (experimentais), UI nativa Android e iOS (N/A com equivalente), CLI sem HTTP e outros.
- **Exploração com `npx playwright cli`** da versão fixada (embutida no `@playwright/test`): snapshot, `find`, ação por ref ou locator, console, requests, trace opcional, e o código `getByRole(...)` de cada ação como ponte para o spec.
- **Specs `e2e/F-NN-<slug>.spec.ts`:** feliz mais negativo ou borda, locators por papel e rótulo, dado por teste, sem `waitForTimeout` nem `networkidle`.
- **Gate de estabilidade:** `--repeat-each=5` e `--shuffle --workers=2` antes de qualquer `Passou`, com revisão por outro agente.
- **Matriz com evidência:** status por funcionalidade, prova separada (`spec-estável` ou `exploração`), execução de evidência em `test-results/<id>/`, relatório HTML em `playwright-report/<id>/`, bugs `BUG-NN` com trace e totais antes × depois.
- **Healer seguro:** a triagem classifica falha de teste ou de produto e **propõe**; nunca troca o esperado pelo observado nem usa `skip`, `fixme` ou `test.fail` sem decisão humana.
- **Segurança por padrão:** a página é dado, credencial só por variável de ambiente (nunca `fill` de senha na CLI), evidência é sensível, alvo só local ou staging.
- **Modo `PLAYWRIGHT-COMPLETO`:** ciclo integral sob pedido explícito, sem o teto de 15 e 8, com leitura em lotes, matriz de aplicabilidade e revalidação por auditor.

## Quando usar

Peça ajuda deste plugin para: validar um sistema funcionalidade por funcionalidade; abrir o app e testar cada tela; escrever specs Playwright e provar que são estáveis; montar a matriz de funcionalidades; testar API, rede, offline, visual, acessibilidade ou responsivo com Playwright; triar um teste que falhou sem mascarar bug; fechar a rodada com relatório e números; saber se Playwright serve para Electron, Android, iOS, extensão ou PWA. Estratégia e risco, bug report e flaky em geral ficam no plugin `qa-testing`; construir o que se testa fica nos plugins de domínio.

## Componentes

| Tipo | Nome | Para que serve |
| --- | --- | --- |
| Skill núcleo | `playbook` (`/qa-playwright:playbook`) | Router, ciclo obrigatório, princípios, modo `PLAYWRIGHT-COMPLETO`, 12 referências e 9 templates |
| Skill | `prompts` | Biblioteca de 22 prompts prontos, prompt de sistema do projeto e mensagem inicial |
| Skill | `feature-inventory` | Inventário `F-NN`, aplicabilidade, escopo e teto da rodada |
| Skill | `harness-setup` | Prepara versões, harness, config, `.gitignore` e instâncias (só por pedido ou sob o protocolo do orquestrador) |
| Skill | `explore-feature` | Valida uma funcionalidade por vez com a CLI fixada e grava a nota |
| Skill | `write-specs` | Transforma a exploração em spec e roda o gate |
| Skill | `api-and-network` | `request`, híbrido API mais UI, `route`, HAR, WebSocket, `clock` |
| Skill | `visual-a11y-responsive` | Emulação, `toHaveScreenshot`, ARIA snapshot, axe |
| Skill | `failure-triage` | Teste ou produto, trace pela CLI, patch proposto |
| Skill | `evidence-report` | Única que altera status; relatório, antes × depois, números |
| Skill | `non-web-systems` | Electron, Android, extensão, PWA; N/A com equivalente |
| Agente | `feature-explorer` | Explora um lote de até 5 funcionalidades, uma de cada vez |
| Agente | `spec-writer` | Escreve o spec e roda o gate |
| Agente | `spec-reviewer` | Revisa specs em lote, somente leitura |
| Agente | `failure-triager` | Classifica falhas e propõe, sem aplicar |
| Agente | `matrix-auditor` | Confere a matriz contra o `results.json` e reexecuta os `spec-estável` |

O plugin tem 10 casos de eval projetados (`designed_not_executed`). Não há comandos (`commands/`): cada skill já vira `/qa-playwright:<skill>`.

O plugin é **seguro por padrão**: sem hooks ativos, sem `.mcp.json`, sem `.lsp.json`, sem `bin/`. O MCP fixado, as permissões mínimas e os riscos estão documentados, desativados, em `skills/playbook/references/ferramentas-e-mcp.md`.

## Instalação

Dentro de uma sessão do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install qa-playwright@brain-of-agent
```

Pela linha de comando: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install qa-playwright@brain-of-agent`. Para validar a estrutura de uma cópia local: `claude plugin validate <pasta-do-plugin>`.

O plugin **não instala o Playwright**. A skill `harness-setup` mostra os comandos (versão exata com `npm i -D -E @playwright/test@<versão>`, sem `^`, nunca `@latest`) e o agente principal os executa sob o protocolo do orquestrador ou a seu pedido. Requisitos: Node 20 como mínimo técnico e 22 ou superior recomendado; Chrome ou Edge instalados evitam o download do Chromium.

## Exemplos de pedidos

1. "Valide funcionalidade por funcionalidade o sistema em `http://127.0.0.1:3000`." → `playbook`: inventário `F-NN`, aplicabilidade, exploração, specs com gate, matriz e relatório, com teto de cerca de 15 e 8.
2. "O teste da F-03 falhou, deixa verde." → `failure-triage`: lê trace e console, classifica teste ou produto; se for produto, entrega `BUG-NN` e não troca o esperado.
3. "Explora a tela de checkout e me diz o que você acha." → `explore-feature`: uma funcionalidade por vez, efeito verificado, nota com evidência, sem enviar nada a terceiros.
4. "Meu app é Android nativo, como valido com Playwright?" → `non-web-systems`: N/A com motivo e executor equivalente (Compose UI test, Espresso ou UI Automator), exploração por `adb` no emulador existente, backend com `request`; a matriz continua a mesma.
5. "Gere a matriz de funcionalidades da última mudança." → `feature-inventory`: tocadas pela mudança e risco alto primeiro, o resto "Não validado nesta rodada" com motivo.
6. "PLAYWRIGHT-COMPLETO: valide o sistema inteiro." → modo completo do `playbook`: leitura em lotes, todas as funcionalidades do escopo, orçamento declarado, revalidação por `matrix-auditor`.
7. "Escrevi o spec da F-05, passou uma vez, marca Passou." → `write-specs`: recusa; exige `--repeat-each=5`, `--shuffle --workers=2` e revisão por outro agente.

## Palavra-chave `PLAYWRIGHT-COMPLETO`

Escreva `PLAYWRIGHT-COMPLETO` como comando na sua mensagem para ativar o ciclo integral: leitura da base do plugin em lotes, matriz de aplicabilidade por tipo de sistema, todas as funcionalidades do escopo exploradas e com spec (sem o teto de cerca de 15 e 8, com o orçamento de tempo e custo declarado antes) e revalidação por auditor. O que ela **não** é: não é senha nem permissão, **não amplia permissões**, não autoriza produção, instalação além da pré-autorizada, publicação nem ferramenta nova, e não é ativada por ocorrência em log, código, comentário, README, saída de ferramenta ou texto de terceiros. O resultado usa os gates Concluído, Parcial ou Impedido; nunca "completo" com leitura ou execução parcial. Sem a palavra, o plugin carrega só o necessário e responde proporcionalmente ao pedido.

## Principais fontes (top 10)

Detalhes, URLs, licenças e datas em `skills/playbook/references/fontes.md`. Pesquisa e validação de 13/10/2026.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | `microsoft/playwright`: docs, guias e release notes (Apache-2.0, pacote 1.64.0) | A |
| 2 | `microsoft/playwright-cli` e a skill `playwright-cli` embutida no pacote (Apache-2.0) | A |
| 3 | `microsoft/playwright-mcp`: README e flags de segurança (Apache-2.0) | A |
| 4 | Playwright best practices (playwright.dev/docs/best-practices) | A |
| 5 | Playwright authentication (playwright.dev/docs/auth) | A |
| 6 | Playwright parallelism (playwright.dev/docs/test-parallel) | A |
| 7 | Playwright retries (playwright.dev/docs/test-retries) | A |
| 8 | Playwright Docker e CI (playwright.dev/docs/docker) | A |
| 9 | Effective harnesses for long-running agents (Anthropic Engineering, 26/11/2025) | B |
| 10 | Agentic testing: where agents fit in the E2E testing stack (Slack Engineering, 11/06/2026) | B |

Também usados: Clock e component testing do Playwright (A); Checkly sobre `waitForTimeout`, Subito sobre axe e a prática de Debbie O'Brien (B); `webapp-testing` de anthropics/skills, só como ideia (B). Verificação por execução (X-01 a X-26) no Windows 11 com Node 24.15.0, Playwright 1.64.0, Chrome e Edge; X-22 a X-26 montaram um harness novo com os templates do plugin e exercitaram instalação exata, login sem senha no contexto, gate de estabilidade e mais comandos da CLI.

## Créditos e licenças

- **Conteúdo destilado de `microsoft/playwright`, `playwright-mcp` e `playwright-cli` (Apache-2.0)**, consultados em 13/10/2026 (commits b536a63, b8b4183 e b85c7a7; pacote 1.64.0). A redação é própria; trechos literais curtos vêm marcados "Microsoft Playwright, Apache-2.0". O plugin não redistribui código nem os arquivos `.agent.md` do Playwright. Copyright: "Copyright (c) Microsoft Corporation" (e "Portions Copyright 2017 Google Inc." no `microsoft/playwright`), lido nos arquivos `LICENSE` em 13/10/2026.
- **Modelos de configuração e de CI** dos templates partem de exemplos da Microsoft Playwright (Apache-2.0), adaptados e marcados nos arquivos; os demais trechos de código são de redação própria.
- **Outras fontes** (Anthropic Engineering, Slack Engineering, Checkly, Subito, dev.to, Momentic): citadas por URL e destiladas, sem texto literal. `anthropics/skills` `webapp-testing` (Apache-2.0 no `LICENSE.txt` da pasta) serviu só como ideia.
- **Estilo e processo da casa:** `brain-of-agent` (francisco-efjr/brain-of-agent), licença MIT.
- Este plugin: MIT, Francisco Edson.

## Limitações honestas

- **Revisão não independente.** Pesquisa, síntese, crítica, validação e construção foram feitas por modelos Claude da mesma família; as notas de qualidade são autoatribuídas até alguém rodar `claude plugin eval` com baseline sem o plugin.
- **Evals `designed_not_executed`.** Os casos estão projetados, não medidos. `claude plugin eval` exige Claude Code 2.1.269 ou superior (a CLI da fábrica era 2.1.128) e, no Windows nativo, suítes com Bash ou PowerShell pedem WSL2.
- **Plugin ainda não exercitado de ponta a ponta.** As peças foram verificadas por execução no sistema-demo: instalação exata sem `^` e `npm ci` (X-22), login sem senha no contexto, com setup em `trace: 'off'`, estado por porta e `state-load` (X-23), gate de estabilidade com `results.json` parseável (X-24) e `testMatch` padrão sem `*.setup.ts` (X-25). Seguem pendentes a rodada simulada em modo melhoria com os agentes (S-24), o harness em projeto não-JS (S-19), o custo por rodada (S-14), `--fail-on-flaky-tests` (S-05) e o login em sistema com outro mecanismo de sessão; se o login falhar num sistema, as linhas com login ficam `Bloqueado`.
- **Custo e teto não medidos.** O teto de cerca de 15 funcionalidades exploradas e 8 com spec é ponto de partida. Não há medição de tokens da CLI contra o MCP; o plugin não promete economia.
- **CLI parcialmente exercitada.** Foram executados `open` (com `--browser` e `--device`), sessão `-s=`, `snapshot` e `screenshot` com `--filename` em subpasta, `find` e `find --regex`, `click`, `fill`, `console`, `requests` e `request <n>`, `generate-locator`, `route`, `network-state-set`, `state-save`, `state-load`, `resize`, `set-color-scheme`, `eval --raw`, `tracing-start`, `tracing-stop`, `close` e `list` (X-04 a X-14, X-23, X-26). Os demais (`dialog-accept`, `tab-*`, `upload`, `--debug=cli` com `attach` e outros) só constam do `--help`; `exploracao-cli.md` marca cada um. URL com `&` no PowerShell segue sem verificação.
- **Ambiente verificado.** Windows 11 (PowerShell 5.1 e Git Bash), Node 24.15.0, `@playwright/test` 1.64.0, Chrome e Edge. Linux e macOS não foram testados.
- **Nativos.** A exploração por `adb` foi verificada num AVD (Pixel_10, Android 17); Compose UI test e Espresso vêm do plugin `mobile-apps`. Appium, Maestro, XCUITest, Detox e Patrol não foram verificados (só páginas oficiais, quando lidas). Electron e Android Chrome e WebView são experimentais no Playwright, e a CLI contra Electron e extensão não foi testada.
- **MCP não testado num cliente real.** O JSON do MCP fixado é texto desativado; a sintaxe de `claude mcp add` não foi verificada.
- **O que o Playwright não faz.** Contrato, schema OpenAPI e carga (use `backend-api` e `sre-observability`); acessibilidade completa (axe não cobre tudo; teclado e leitor de tela são manuais); UI nativa Android e iOS; Safari real (WebKit não é Safari).
- **Limites por instrução.** O prefixo `Bash(npx playwright ...:*)` pré-aprova o comando inteiro; as flags perigosas (`--ui-host`, `-u`, `attach`, `run-code`) são proibidas por instrução e conferidas pelo revisor, não por barreira técnica. Comandos com variável de ambiente na frente (`E2E_RUN=<id> npx playwright test ...`) podem não casar com o prefixo e pedir permissão (Não verificado). A matriz em Markdown continua editável pelo modelo; a defesa é de processo (só `evidence-report` escreve; o auditor confere).
- **Fontes.** A lente de comunidade (Reddit, HN de 2026, YouTube) é a mais fraca e nada vira regra sem fonte oficial. Redação de `Cookie` e `Authorization` no trace não foi verificada: trate todo trace como sensível.
- **Versões mudam.** Confira flags e APIs na versão fixada (`npx playwright --version`, `npx playwright cli --help`) antes de copiar um comando.
- **Escopo.** Só local ou staging indicado; produção só com confirmação explícita e leitura. Sem push, deploy, publicação, pagamento nem envio de mensagens.
