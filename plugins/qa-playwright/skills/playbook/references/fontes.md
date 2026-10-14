# Fontes (bibliografia validada)

Pesquisa e validação de 13/10/2026 (coluna "Consulta"). Classe A = documentação oficial ou mantenedor; B = empresa de engenharia ou autor reconhecido, usar com cruzamento; C = sinal de prática, nunca fonte única. A nota entre parênteses é a pontuação 0 a 10 da rubrica de fontes. "Licença" descreve a licença **identificada**; sem licença identificada, o plugin só destila (redação própria) e cita. IDs `V-NN` vêm de `docs/research/qa-playwright/VALIDATED.md`; `X-NN` são fatos verificados por execução do orquestrador (`docs/research/qa-playwright/VALIDACAO-EXECUCAO-ORQUESTRADOR.md`; no brain-of-agent, `docs/dev-segments/research/qa-playwright/`).

## Sumário

- [Atribuição e licenças](#atribuição-e-licenças)
- [Como citar e o que conferir](#como-citar-e-o-que-conferir)
- [Classe A](#classe-a)
- [Classe B](#classe-b)
- [Classe C](#classe-c)
- [Fatos verificados por execução](#fatos-verificados-por-execução)
- [Rejeitados e rebaixados](#rejeitados-e-rebaixados)
- [Pistas que não valem como fato](#pistas-que-não-valem-como-fato)
- [Lacunas conhecidas](#lacunas-conhecidas)

## Atribuição e licenças

> Partes deste plugin destilam documentação, READMEs e skills de `microsoft/playwright`, `microsoft/playwright-mcp` e `microsoft/playwright-cli` (Apache-2.0), consultados em 13/10/2026 (commits b536a63, b8b4183 e b85c7a7; pacote 1.64.0). A redação é própria; trechos literais curtos vêm marcados "Microsoft Playwright, Apache-2.0". O plugin não redistribui código nem os arquivos `.agent.md` do Playwright. Outras fontes (Anthropic Engineering, Slack Engineering, Checkly, Subito, dev.to, Momentic) são citadas por URL e destiladas. `anthropics/skills` `webapp-testing` serviu só como ideia (V-20).

Linhas de copyright lidas nos `LICENSE` dos clones locais em 13/10/2026: `microsoft/playwright` traz "Portions Copyright (c) Microsoft Corporation" e "Portions Copyright 2017 Google Inc."; o `NOTICE` do repositório declara "Copyright (c) Microsoft Corporation" e código derivado do Puppeteer (Apache-2.0). `playwright-mcp` e `playwright-cli` trazem "Copyright (c) Microsoft Corporation". Os códigos dos templates em `assets/templates/` são de redação própria; o modelo de configuração e o workflow de CI partem de exemplos da Microsoft Playwright, Apache-2.0 (adaptados e marcados no arquivo). Texto literal só até 40 linhas, só de Apache-2.0 ou MIT, com atribuição.

## Como citar e o que conferir

- Flags, comandos e APIs mudam: confira na versão fixada com `npx playwright --version`, `npx playwright cli --help` e o `--help` de cada subcomando antes de copiar um comando.
- A skill do agente embutida no pacote é a fonte viva dos comandos da CLI: `node_modules/playwright-core/lib/tools/skills/playwright-cli/SKILL.md` (X-03). Leia-a em vez de copiar uma versão que envelhece.
- A URL pública de uma página de `docs/src/<x>-js.md` é `https://playwright.dev/docs/<x>`. Caminho e linha (por exemplo `docs/src/locators.md:76`) são do commit b536a63, que está em `1.65.0-next`, um pouco à frente do 1.64.0 (V-49 conferiu o pacote 1.64.0 quando importava).
- Números de blogs e relatos (percentuais, tokens, execuções) são dos autores. Cite com a fonte e a ressalva, e nunca como medição do seu projeto (V-18, conflito 6).
- Resumos de WebFetch foram conferidos no resumo, não no HTML bruto. Reabra a página antes de citar literal.

## Classe A

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-27..V-49 (10) | microsoft/playwright (docs, agentes, workflows; ★97.642; release v1.64.0 em 07/10/2026) | https://github.com/microsoft/playwright | Apache-2.0 | 2026-10-13 | Núcleo técnico: locators, asserções, config, CI, trace, release notes, rede, visual, a11y |
| V-01 (10) | microsoft/playwright-cli (v0.1.22 em 28/09/2026; skill `playwright-cli` com references) | https://github.com/microsoft/playwright-cli | Apache-2.0 | 2026-10-13 | Ciclo de exploração, snapshot, refs, código equivalente, geração de teste |
| V-22 (10) | microsoft/playwright-mcp (v0.0.83 em 28/09/2026; ★38.101) | https://github.com/microsoft/playwright-mcp | Apache-2.0 | 2026-10-13 | Flags de segurança, `--isolated`, `--allowed-origins`, aviso de que não é fronteira de segurança |
| V-02 (9) | Pacote `@playwright/test` 1.64.0 e `playwright-core` (subcomandos `cli`, `mcp`, `trace`, `init-agents`; skills embutidas) | registro npm (`npm view @playwright/test version`) | Apache-2.0 (repositório) | 2026-10-13 | Versão fixada, CLI e MCP embutidos, `engines.node >=20`; X-01..X-20 e X-22..X-26 foram executados nesta versão |
| V-02 (9) | Plugin oficial `playwright` do `claude-plugins-official` (`.mcp.json` com `@playwright/mcp@latest`) | https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/external_plugins/playwright/.mcp.json | repositório Apache-2.0; licença própria por plugin | 2026-10-13 | Só como fato do conteúdo (`@latest` sem versão); o plugin não o adota |
| V-27 (10) | Playwright best practices | https://playwright.dev/docs/best-practices | docs do produto (repositório Apache-2.0) | 2026-10-13 | Prioridade de locators, web-first, isolamento, instalação mínima |
| V-37 (10) | Authentication | https://playwright.dev/docs/auth | idem | 2026-10-13 | Projeto `setup`, `storageState`, `.gitignore` de `playwright/.auth`, `sessionStorage` |
| V-33 (10) | Parallelism | https://playwright.dev/docs/test-parallel | idem | 2026-10-13 | Isolamento, dados por teste, `serial` não recomendado, `lock` |
| V-41 (10) | Retries | https://playwright.dev/docs/test-retries | idem | 2026-10-13 | Definição de flaky, `testInfo.retry`, retry não é correção |
| V-48 (10) | Docker | https://playwright.dev/docs/docker | idem | 2026-10-13 | Imagem `mcr.microsoft.com/playwright:v1.64.0-noble` fixada na versão do projeto, `--init`, `--ipc=host` |
| V-53 (9) | Clock | https://playwright.dev/docs/clock | idem | 2026-10-13 | `install` como primeira chamada, `fastForward`, `setFixedTime` |
| V-58 (9) | Component testing | https://playwright.dev/docs/test-components | idem | 2026-10-13 | Estável desde 1.62 (conflito 4); galeria de stories e `mount` |
| V-60 (9) | Electron (classe `Electron`) | https://playwright.dev/docs/api/class-electron | idem | 2026-10-13 | Suporte experimental, requisitos, stub de diálogo |
| V-04 (10) | Installation (intro) | https://playwright.dev/docs/intro | idem | 2026-10-13 | Node 22, 24 ou 26 recomendados; `engines.node >=20` no pacote |
| V-61 (9) | Páginas oficiais de Appium, Espresso, Maestro, Flutter `integration_test` e Tauri (WebdriverIO) | ver `docs/research/qa-playwright/github-sistemas.md` | por produto, não conferida | 2026-10-13 | Ponteiros dos equivalentes nativos; só a página foi lida, capacidades não testadas |

Páginas de `docs/src` sem versão pública reaberta (conferidas no clone local, commit b536a63): `locators`, `actionability`, `navigations`, `input`, `test-assertions`, `test-fixtures`, `test-projects`, `test-configuration`, `test-webserver`, `test-reporters`, `trace-viewer`, `test-cli`, `test-annotations`, `test-timeouts`, `test-snapshots`, `aria-snapshots`, `accessibility-testing`, `network`, `mock`, `emulation`, `dialogs`, `downloads`, `frames`, `pages`, `api-testing`, `chrome-extensions`, `service-workers`, `browsers`, `languages`, `library`, `release-notes`. Leitura local, sem execução.

## Classe B

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-17 (6) | Effective harnesses for long-running agents (Anthropic Engineering, 26/11/2025, Justin Young) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | texto sem licença identificada, destilado | 2026-10-13 | Arquivo de funcionalidades com `passes`; "editar teste é inaceitável"; JSON porque o modelo o sobrescreve menos. Não há avaliador separado no artigo (ver "Pistas") |
| V-18 (6) | Agentic testing: where agents fit in the E2E testing stack (Slack Engineering, 11/06/2026, Sergii Gorbachov) | https://slack.engineering/agentic-testing-where-agents-fit-in-the-e2e-testing-stack/ | idem | 2026-10-13 | Medir antes de adotar um modo; teste gerado em uma tacada foi o mais frágil no fluxo médio (~48%); custo de US$ 15-30 por execução com agente |
| V-19 (5) | Letting Playwright MCP explore your site and write your tests (Debbie O'Brien, 18/06/2025) | https://dev.to/debs_obrien/letting-playwright-mcp-explore-your-site-and-write-your-tests-mf1 | idem | 2026-10-13 | Cinco regras: explorar antes de escrever, não gerar só do cenário, locator por papel, asserção que espera, revisar o trace. Modelo antigo; texto literal do prompt não obtido |
| V-20 (6) | `webapp-testing` (anthropics/skills) | https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md | Apache-2.0 no `LICENSE.txt` da pasta; a raiz do repositório não declara licença | 2026-10-13 | Só a ideia reconhecer, agir, fechar. Não herdar `networkidle`, `wait_for_timeout` nem `with_server.py` não lido |
| V-32 (6) | Never use page.waitForTimeout (Checkly, Nočnica Mellifera, 05/03/2025, atualizado 31/03/2025) | https://www.checklyhq.com/blog/never-use-page-waitfortimeout/ | sem licença identificada, destilado | 2026-10-13 | Espera fixa gera falso alarme e tempo perdido a cada retry; a regra vem da doc oficial (A) |
| V-57 (6) | How we automate accessibility testing with Playwright and axe (Subito, 10/12/2025) | https://dev.to/subito/how-we-automate-accessibility-testing-with-playwright-and-axe-3ok5 | idem | 2026-10-13 | Páginas críticas em lista fixa, não bloqueia o build, issue por violação, exclusão por seletor. O Subito usa só `wcag2a` e `wcag2aa`; a doc oficial recomenda também `wcag21a` e `wcag21aa` |

## Classe C

| Item | Título | URL | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- |
| V-21 (C) | Show HN: Playwright Skill for Claude Code (thread de cerca de 11 meses; comentários de risco) | https://news.ycombinator.com/item?id=45642911 | 2026-10-13 | Alertas: `run.js` que executa Node gerado é vetor de injeção; console e página vão ao provedor; usar dados fictícios |
| V-33 (C) | What tests look like with Claude Code (Momentic, vendor, atualizado em 20/09/2026) | https://momentic.ai/blog/what-tests-look-like-with-claude-code | 2026-10-13 | Caso de dado compartilhado: 40 de 70 testes passaram porque `getByTestId('todo-item')` casava ~285 itens acumulados. A causa é geral |
| V-17 (C) | Checklist de E2E (David Dias, MIT) | https://frontendchecklist.io/rules/testing/e2e-testing | 2026-10-13 | Lista de áreas: autenticação, fluxos, navegação, formulários, erros. Não cita permissões nem bordas |
| rebaixado (C) | Using Playwright MCP with Claude Code (Simon Willison, 01/07/2025) | https://simonwillison.net/2025/Jul/1/using-playwright-mcp-with-claude-code | 2026-10-13 | Só a ideia de login humano com a janela visível; usa `@latest` |
| rebaixado (C) | Playwright e Claude Code (nikiforovall, 06/09/2025, atualizado em abril de 2026) | https://nikiforovall.blog/ai/2025/09/06/playwright-claude-code-testing.html | 2026-10-13 | Relatório manual de exploração separado do spec (ideia em V-17) |
| V-41 (C) | Playwright HTML reporter at scale (Currents, vendor, 24/04/2026) | https://currents.dev/posts/playwright-html-reporter-why-it-breaks-down-at-scale | 2026-10-13 | O reporter nativo marca flaky só dentro da mesma execução, sem histórico |

## Fatos verificados por execução

`X-01` a `X-21` foram verificados pelo orquestrador em 13/10/2026, no Windows 11 com Node v24.15.0, npm 11.12.1, Chrome e Edge instalados, `@playwright/test` 1.64.0 e um sistema-demo de tarefas com bug proposital. `X-22` a `X-26` vêm de um segundo smoke (14/10/2026, cerca de 02:05 a 02:15 UTC), num harness novo montado com os templates do desenho e com o sistema-demo ganhando cookie de sessão `HttpOnly` e página protegida. Resumo do que cada faixa sustenta:

| Faixa | O que sustenta |
| --- | --- |
| X-01, X-02, X-03, X-08 | Versão, subcomandos e flags do pacote 1.64.0; `cli` e `mcp` embutidos |
| X-04, X-05, X-06, X-11 | `--browser=chrome` sem download; snapshot em arquivo YAML; código equivalente por ação; alvo por ref ou locator |
| X-07, X-10, X-14 | Exploração valida efeito; erro de console precisa de triagem; o bug do contador só aparece com asserção do efeito |
| X-09, X-12, X-13 | `close` e `list` sem órfão; `route`, `network-state-set`, `state-save`, `tracing-start` e `tracing-stop` |
| X-15 | `.playwright-cli/` acumula arquivos e vai para o `.gitignore` |
| X-16, X-17, X-18 | PowerShell 5.1, `--grep`, `--reporter` substitui reporters, config verificada, saída separada por execução |
| X-19, X-20 | `error-context.md` traz texto dirigido a IA (dado, não ordem); `npx playwright trace` lê a falha sem GUI |
| X-21 | Rota nativa Android por `adb` no AVD existente, com as armadilhas de polling e de caminho |
| X-22 | `npm i -D -E @playwright/test@1.64.0` grava a versão sem `^`; `npm ci` reproduz a instalação (S-02) |
| X-23 | Login sem senha no contexto (S-22): o `fill` da CLI ecoa o valor; o projeto `setup` contra a instância de exploração gera `user-4173.json`; `state-load` + `goto` abre a área logada; `trace: 'off'` no setup não gera trace |
| X-24 | Gate (S-04): `--repeat-each=5 --retries=0` separa bug determinístico (5/5) de intermitência; `--shuffle --workers=2` aceitos; `results.json` com `stats`; porta 4174 livre depois da execução |
| X-25 | O `testMatch` padrão não pega `*.setup.ts`; o setup roda só pelo projeto `setup` |
| X-26 | Mais comandos da CLI (S-03): `-s=`, `open --device`, `snapshot` e `screenshot --filename` em subpasta, `requests` e `request <n>`, `resize`, `set-color-scheme`, `find --regex "<padrão>"` (valor da opção), `eval --raw` |

Observação do orquestrador (corrige o SYNTHESIS e X-16): o filtro por tipo é `--grep "@ui|@api"`, sem barra invertida, no Git Bash e no PowerShell 5.1; a forma com `\|` dá "No tests found" (o `\|` em X-16 era só escape de tabela Markdown). O filtro posicional `npx playwright test F-07-` também foi verificado, no Git Bash.

## Rejeitados e rebaixados

| Item | Decisão | Motivo |
| --- | --- | --- |
| Custo de tokens do MCP (114K × 27K, "4x", 5-15k por interação) | Rejeitado como dado | Números de snippet sem medição primária; um re-benchmark de 24/07/2026 achou paridade (~3.580 × ~3.620 caracteres) num fluxo de 7 passos. Fica a lição de método (V-18) |
| "Playwright is flaky" (blog de produto concorrente) | Rejeitado | Sem método, anedotas, oferece migração grátis |
| Comparativo de API Playwright × REST Assured × Postman | Rejeitado como evidência | Sem benchmark nem método; o conteúdo útil vem da doc oficial (V-51) |
| Maestro iOS × Android (blog de vendor) | Rejeitado como fonte | Sem método; "a matriz é a mesma, só o executor muda" é decisão de projeto (V-61) |
| `webapp-testing` | Rebaixado A para B | Leitura por resumo; manda `networkidle` e `wait_for_timeout`; script não lido |
| Config de MCP com `@playwright/mcp@0.0.83` | Rebaixado | Depende de Playwright alpha; sintaxe `claude mcp add ... --` não verificada (V-07) |
| Mock de APIs do browser (init scripts) | Rebaixado A para B | Leitura parcial; a doc diz que são APIs experimentais ou sem suporte total |
| Post da Checkly sobre retry (31/05/2023) | Rebaixado | Trata de checks de monitoramento da Checkly, não de retries do Playwright Test |
| Applause, TestDino | Não usados | HTTP 403 e só metadados; o caso de dado compartilhado foi confirmado por outra via |

## Pistas que não valem como fato

- **Avaliador separado e cético** (AO-20): o artigo da Anthropic de 26/11/2025 não traz avaliador separado, só inicializador e codificador com o mesmo prompt de sistema e as mesmas ferramentas. O browser lá é o Puppeteer MCP. Vale `passes` mais a regra de não editar testes; o plugin acrescenta por conta própria (Inferido) a evidência obrigatória, o status só por execução e a revisão por outro agente (V-17, V-15). Cite o artigo como "Anthropic, 26/11/2025", sem atribuir a ele o avaliador.
- **CLI economiza tokens**: afirmação do produtor, sem número (V-06). Na Slack, a CLI não foi mais barata que o MCP (~6 M contra ~3,5-3,8 M de tokens no Search Discovery). O plugin escolhe a CLI por versão fixada, evidência em arquivo e código pronto, não por token (conflito 6).
- **`--loop=vscode` para o Claude Code** na página pública: erro de documentação; o valor certo é `--loop=claude` (V-13).
- **Component testing experimental**: desatualizado; é estável desde 1.62 (conflito 4).
- **Node 18 nos READMEs do MCP e da CLI**: desatualizado; o mínimo técnico é 20 (conflito 7).

## Lacunas conhecidas

Reddit (domínio bloqueado), HN de 2026, Thoughtworks Radar e blog oficial (404) não foram lidos: a lente de comunidade é a mais fraca. Redação de `Cookie` e `Authorization` no trace não foi verificada. Consumo real de tokens e custo por rodada não foi medido (S-14). `--with-deps` no Windows sem administrador não está documentado. XCUITest, Detox e Patrol sem fonte oficial lida. Playwright em desktop que não seja Electron (Tauri, WPF, Qt) sem fonte da documentação. Matriz de quatro eixos (rotas, formulários, permissões, bordas) é proposta do plugin, sem padrão externo verificado. O comportamento de runtime de `init-agents` e do healer ficou em `coreBundle.js`, que não foi lido; o plugin não depende dele.

Validado em: 2026-10-13 · modelo-alvo: claude-sonnet-5-5.
