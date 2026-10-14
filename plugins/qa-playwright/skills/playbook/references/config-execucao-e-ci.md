# Configuração, execução e CI

Config modelo, saídas por execução, sintaxe de execução no Windows, projetos, autenticação, paralelismo, retries, timeouts, trace, gate de estabilidade e CI. Fontes: V-34..V-48, X-16, X-17, X-18, X-20, X-22..X-25. O arquivo de config pronto está em `assets/templates/playwright.config.ts`; esta referência explica as escolhas. O smoke de X-22..X-25 montou um harness novo com esses templates e os exercitou no sistema-demo.

## Sumário

- [Config modelo e webServer](#config-modelo-e-webserver)
- [Saídas por execução](#saídas-por-execução)
- [Reporters](#reporters)
- [Sintaxe de execução, bash e PowerShell](#sintaxe-de-execução-bash-e-powershell)
- [Projects, dependências e teardown](#projects-dependências-e-teardown)
- [Autenticação](#autenticação)
- [Fixtures e Page Object Model](#fixtures-e-page-object-model)
- [Parametrização](#parametrização)
- [Paralelismo, locks e shard](#paralelismo-locks-e-shard)
- [Retries e flaky](#retries-e-flaky)
- [Timeouts](#timeouts)
- [Tags e `--grep`](#tags-e---grep)
- [Trace e `npx playwright trace`](#trace-e-npx-playwright-trace)
- [UI mode, codegen e debug](#ui-mode-codegen-e-debug)
- [CLI de execução e gate de estabilidade](#cli-de-execução-e-gate-de-estabilidade)
- [CI e Docker](#ci-e-docker)

## Config modelo e webServer

O núcleo foi verificado por execução (X-17): `channel: 'chrome'`, `trace: 'retain-on-failure'`, `retries: 0`, reporters `list` e `html` com `open: 'never'`, `webServer` com `env: { PORT }`, `url` de health em `127.0.0.1` e `reuseExistingServer: false`. O Playwright subiu e derrubou o servidor sozinho; um teste de API (`request`) e um de UI (`getByLabel`, `getByRole`, `toHaveText`) passaram.

| Escolha | Porquê |
| --- | --- |
| `channel` por variável `PW_CHANNEL`, padrão `chrome` | Navegador instalado, sem download (X-04). `chromium` exige `install chromium` |
| `retries: 0` local, `1` na CI | Rodada local sem retry: a falha aparece como falha (V-41). Com retries 0, `trace: 'on-first-retry'` não grava nada (V-39) |
| `trace: 'retain-on-failure'` | Guarda o trace só de quem falhou (V-45) |
| `webServer` em `127.0.0.1` com `url` de health | Servidor só local (G-22). `url` aceita 2xx, 3xx, 400, 401, 402 e 403 como pronto; `timeout` padrão 60 s; `stdout` padrão `ignore`; `port` está deprecado (V-39) |
| `reuseExistingServer: false` por padrão | A instância de teste não herda o estado da exploração. `E2E_REUSE=1` só para gerar o estado de login da exploração (X-17, G-32) |
| `globalTimeout` no config | O relatório sai mesmo se a execução travar; `timeout-minutes` do job de CI mataria antes (V-42) |
| `gracefulShutdown` | **Ignorado no Windows**: o processo do servidor é encerrado à força (V-39). No smoke, a porta 4174 ficou livre depois da execução (X-24); em outro projeto, confira a porta (S-08) |
| Config e `package.json` na **mesma pasta** | Com a config numa subpasta sem `package.json`, o `playwright-report/` foi gravado na pasta do `package.json` (X-17). Em projeto existente, fixe `outputFolder` e `outputFile` |

Em projeto que já tem `playwright.config.*`, o plugin respeita o `testDir` e os projetos dele e só acrescenta o que falta. O comportamento do `webServer` com `reuseExistingServer: false` quando a porta está ocupada pela instância de exploração **não foi verificado** (L-6): use portas distintas.

## Saídas por execução

Fonte: X-18, DO-12, `class-testconfig.md:338`.

- O `outputDir` é **limpo no início de cada execução**. Uma execução sem cuidado apagaria o trace da anterior. Por isso cada execução grava na própria pasta:
  - `outputDir: test-results/${E2E_RUN ?? 'local'}`
  - HTML em `playwright-report/${E2E_RUN ?? 'local'}`
  - JSON em `test-results/${E2E_RUN ?? 'local'}/results.json`
- Verificado (X-18): uma execução `E2E_RUN=r2` **não apagou** o `trace.zip` da `r1`. Teste que falha gera `trace.zip` e `error-context.md` na pasta do teste. O JSON dentro do `outputDir` da própria execução existe depois dela (a limpeza vem antes).
- **Execução de evidência:** `E2E_RUN=<AAAAMMDDThhmm>-<escopo>`. Gate e execuções locais caem em `local/` e não tocam a evidência.
- Bash: `E2E_RUN=20261013T1030-evidencia npx playwright test --grep "F-01|F-02"`.
- PowerShell: a variável fica na sessão, e a execução seguinte **limparia a mesma pasta**. Remova depois:

```powershell
$env:E2E_RUN='20261013T1030-evidencia'; npx playwright test --grep "F-01|F-02"; Remove-Item Env:E2E_RUN
```

- `.playwright-cli/` fica só para a exploração. Triagem usa `E2E_RUN=triagem-<F-NN>-<hhmm>` para preservar o trace (SK-07 passo 1). A auditoria usa `E2E_RUN=auditoria-<id>`.
- As pastas são ignoradas pelo git e lidas pelos agentes, nunca commitadas (G-20, G-21). Relatório HTML: o humano o abre com `npx playwright show-report playwright-report/<id>`; o agente lê `results.json` e usa `npx playwright trace`.

## Reporters

Fonte: V-44, X-16.

- `dot` é o padrão na CI, `list` no local. O HTML abre sozinho só em falha; `open: 'never'` impede isso. `PLAYWRIGHT_HTML_OPEN` aceita `always`, `never` e `on-failure`. O agente **sempre** roda sem abrir o relatório, para não ficar preso no servidor (`playwright-tests.md:3`).
- **Não passe `--reporter` na linha de comando** quando quiser HTML e JSON: ele **substitui** os reporters da config e o HTML não é gerado (X-16).
- `doNotInlineAssets` serve a CSP. O reporter `github` multiplica anotações em matriz. JUnit separa `<error>` de `<failure>` desde a 1.59.
- Para sharding use `reporter: 'blob'` na CI e `merge-reports` (V-34).
- O `results.json` é a fonte do `evidence-report` e do `matrix-auditor`. Verificado (X-24): `test-results/<id>/results.json` é parseável e traz `stats` = `{ expected, unexpected, flaky, skipped }`. Os campos por teste (status, retentativa, anexos, caminho do trace) seguem como item de smoke (S-07): parseie por chave e trate campo ausente como Não verificado.

## Sintaxe de execução, bash e PowerShell

Verificado no PowerShell 5.1 (X-16 e a nota de correção do orquestrador): `--grep "F-02"`, `--grep-invert "@ui"` e `--grep "@ui|@api"` funcionam. **Sem barra invertida**: a forma `--grep "@ui\|@api"` dá "No tests found" (o `\|` visto em X-16 era escape de tabela Markdown). O `--grep "@ui|@api"` também funciona no Git Bash. O filtro posicional `npx playwright test F-07-` (regex sobre o caminho do arquivo) foi verificado no Git Bash; no PowerShell, prefira `--grep "F-07"`.

```bash
npx playwright test --grep "F-07"                    # uma funcionalidade pelo ID no título
npx playwright test F-07-                            # filtro posicional pelo nome do arquivo (verificado no Git Bash)
npx playwright test --grep "@ui|@api"                # por tipo (OU de tags; sem barra invertida)
npx playwright test --grep "F-01|F-02|F-03"          # várias funcionalidades
npx playwright test --grep-invert "@ui"              # exclui por tipo
npx playwright test --list                           # lista; NÃO é execução
```

PowerShell, para variável de ambiente:

```powershell
$env:PLAYWRIGHT_HTML_OPEN='never'; npx playwright test --grep "@ui|@api" --repeat-each=2   # verificado: 4 passed, exit 0 (X-16)
```

- **Não use `--%` com `npx`**: `npx playwright test --% --grep "F-02"` falhou ("Make sure that arguments are regular expressions matching test files", X-16). A doc oficial mostra `--grep --% "@fast^|@slow"` para PowerShell (`test-annotations-js.md:143`); com `npx` ele não funciona.
- Variáveis: bash `VAR=x comando`; PowerShell `$env:VAR='x'; comando; Remove-Item Env:VAR`.
- ID de largura fixa: o filtro é por substring, então `F-07` casaria `F-070`. Com mais de 99 funcionalidades use três dígitos desde o início.
- Rode o `npx playwright test` na pasta do config.

## Projects, dependências e teardown

Fonte: V-40. Um projeto por navegador, dispositivo (`devices['Pixel 5']`, `devices['iPhone 12']`) ou canal (`channel: 'chrome'`, `'msedge'`).

- Projeto `setup` com `testMatch: /.*\.setup\.ts/` autentica; projetos de teste usam `dependencies: ['setup']`. Projeto dependente **não roda** se a dependência falha. `--no-deps` pula as dependências.
- O `testMatch` padrão não pega `*.setup.ts`: sem login, `npx playwright test --list` listou só os specs ("Total: 4 tests in 2 files"). O setup roda só pelo projeto `setup`, e o projeto sem login dispensa `testIgnore` (X-25).
- Project dependencies são preferidas a `globalSetup` (`test-global-setup-teardown-js.md:8-10`). `teardown` para limpar dados.
- 1.64: `TestProject.default: false` mantém um projeto na config sem rodar por padrão; `--project="*"` roda todos.
- A UI mode não roda o `setup` por padrão (`test-ui-mode-js.md:33`).

## Autenticação

Fonte: V-37, V-38, V-23.

1. Projeto `setup` autentica, espera a URL final **e** um elemento de sessão, e grava `page.context().storageState({ path })`. Credenciais por variável de ambiente (template `assets/templates/auth.setup.ts`).
2. Projetos de teste usam `use: { storageState }`. `sessionStorage` **não** é persistido (snippet manual em `auth.md:589-606`); IndexedDB entra.
3. Estado por **porta**: `playwright/.auth/user-<porta>.json`. Verificado (X-23): `E2E_AUTH=1 E2E_PORT=4173 E2E_REUSE=1 npx playwright test --project=setup` contra a instância de exploração gerou `user-4173.json`, o `state-load` da CLI abriu a área logada e, com `trace: 'off'` no setup, nenhum `trace.zip` foi gerado. Que a sessão de uma instância não valha na outra é Inferido (R-29).
4. Vários papéis: um arquivo de estado por papel e `test.use({ storageState })` por arquivo ou `describe`; dois contextos no mesmo teste para fluxo multiusuário. A rota que o papel **não** deve acessar entra na matriz (V-38).
5. Conta por worker: `test.info().parallelIndex` no nome do arquivo de estado; `browser.newPage({ storageState: undefined })` na fixture de worker (`auth.md:172`); reset com `storageState: { cookies: [], origins: [] }` (`auth.md:691`).
6. Expiração: apague o arquivo e gere de novo. Mantenha ao menos **um** teste de login real pela UI fora do setup (prática de guias; Não verificado como fonte oficial).
7. `request.storageState()` exporta cookies de sessão de API; `context.request` compartilha cookies, `playwright.request.newContext()` isola (V-51).
8. Login em `beforeEach` aparece na doc como exemplo; a recomendação do setup project vem logo depois ("so you can log in only once") (`best-practices-js.md:20-42`). Preferir o setup é Inferido a partir disso (V-37).

## Fixtures e Page Object Model

Fonte: V-35.

- Fixture é o **ambiente mínimo do teste**: código antes de `use()` é setup, depois é teardown. Fixture de worker com `{ scope: 'worker' }`; fixture automática (`auto: true`) para anexar log só na falha; `option: true` para opções por projeto; `mergeTests` para combinar módulos; `box: true` ou `'self'` esconde passos internos do relatório.
- **Timeout de fixture** (conflito 5, código do 1.64.0): fixture de **teste** divide os 30 s do teste ("Test timeout of Xms exceeded while setting up..."); fixture de **worker** tem 30 s próprios (o `timeout` do projeto); ambas aceitam `{ timeout: N }`. A linha "Fixture timeout: no timeout" da tabela oficial só significa "sem timeout dedicado por padrão".
- POM: locators no construtor (`readonly`), métodos de fluxo terminando em `await expect(...)`; quando usado em muitos testes, vira fixture. O exemplo de POM da doc usa CSS (`pom.md:38`); no plugin, prefira `getByRole`.
- O `fixtures.ts` do plugin (`assets/templates/fixtures.ts`) é o estado inicial único e substitui o `seed.spec.ts` do `init-agents`.

## Parametrização

Fonte: V-36. `forEach` gera um teste por caso e os **títulos precisam ser únicos**. Hooks fora do `forEach`, salvo necessidade (`test-parameterize-js.md:25-27`). Variáveis de ambiente para dados e URL; segredo fora do código (`:202`). Opção de fixture por projeto para variar papel ou idioma. PowerShell: `$env:USER_NAME='me'`. O exemplo CSV com `__dirname` pode não existir em ESM (Suposição da pesquisa).

## Paralelismo, locks e shard

Fonte: V-34, V-33.

- Arquivos rodam em paralelo; testes de um arquivo rodam em ordem (`fullyParallel: true` os paraleliza). Worker é reiniciado após falha (`test-parallel-js.md:8, 22`).
- **`lock`** para recurso global (conta, configuração): por nome, entre arquivos, workers e projetos (1.63); `lock` em `describe.configure` (1.64).
- Dado por `testInfo.testId`; saída por `testInfo.outputPath`; `TEST_WORKER_INDEX` e `TEST_PARALLEL_INDEX` disponíveis. `serial` só se o fluxo for de fato dependente ("Using serial is not recommended").
- Test lists são "discouraged… best-effort" (`:311`).
- Shard: com `fullyParallel` divide por teste, sem ele por arquivo (`test-sharding-js.md:36-47`); `reporter: 'blob'` na CI e `merge-reports`; merge entre SOs exige config explícita (`:187`).
- CI: `workers: 1` e `globalTimeout` no config (V-39).

## Retries e flaky

Fonte: V-41. Definição oficial: flaky = "failed on the first run, but passed when retried". Por padrão, teste que falha não é repetido. `testInfo.retry` existe.

- "Passou na retentativa" **nunca** vira verde sem abrir a tentativa que falhou. `--fail-on-flaky-tests` no gate deve fazer o processo sair com código diferente de zero quando algum teste só passa na retentativa: a flag existe em `program.js` do 1.64.0, e o comportamento ainda é o item de smoke S-05 (**Não verificado**).
- `retries` na CI, zero local. `testInfo.retry` para limpar estado do servidor antes da nova tentativa.
- `--repeat-each` **mede** flakiness, não a corrige (Inferido). Retry não é correção.
- O reporter nativo marca flaky só dentro da mesma execução, sem histórico entre execuções (fonte C, Currents).
- Triagem de flaky geral: plugin `qa-testing`, skill `flaky-triage`.

## Timeouts

Fonte: V-42, conflito 5.

| Camada | Padrão e regra |
| --- | --- |
| Teste | 30 s, incluindo fixtures e `beforeEach`; janela extra do mesmo tamanho para teardown e `afterEach` |
| `expect` | 5 s, separado do teste |
| `beforeAll` e `afterAll` | Timeout próprio, igual ao do teste |
| Ação e navegação | Sem limite por padrão: defina `actionTimeout` e `navigationTimeout` para falhar mais cedo |
| `globalTimeout` | Sem limite por padrão: defina no config |

Diagnóstico: "Test timeout of 30000ms exceeded" é sinal para **rever o fluxo** antes de ampliar o limite. "expect.toHaveText with timeout 5000ms" é sinal para rever o estado esperado. Timeout de ação é actionability (veja `checklist-completo.md`, C-D). `toPass` tem timeout padrão 0 e **não respeita** o timeout de `expect`: passe sempre `timeout` (V-31).

## Tags e `--grep`

Fonte: V-43, X-16. A convenção do plugin: `F-NN` abre o título do `describe` e `@ui` ou `@api` vai no título. Assim `--grep "F-07"` roda uma funcionalidade e `--grep "@ui|@api"` filtra por tipo (verificado, X-16). A tag nativa `{ tag: '@F-07' }` (`test-annotations-js.md:68-177`) é **opcional** e fica para depois do S-17 (L-4: sintaxe no 1.64.0 não conferida).

- `skip`, `fail`, `fixme`, `slow` (`test-annotations-js.md:11-14`): `test.fail` **roda** e exige que falhe; `test.fixme` não roda; `test.skip` é para configuração em que o teste não se aplica. Toda exceção leva motivo em texto e `annotation: { type: 'issue', description: 'BUG-NN' }`; só com decisão registrada (V-15, V-43).
- Funcionalidade com bug de produto conhecido e sem correção na rodada: o spec fica vermelho em commit próprio; a alternativa registrada é `test.fail()` com a anotação do bug (DO-6).

## Trace e `npx playwright trace`

Fonte: V-45, X-20.

- Sete modos válidos: `off`, `on`, `retain-on-failure`, `retain-on-first-failure` (1.43), `retain-on-failure-and-retries` (1.59), `on-first-retry`, `on-all-retries`. Use a tabela de `test-use-options-js.md`; a lista curta do `trace-viewer.md` é resumo, não conflito.
- Rodada de QA com `retries: 0`: `retain-on-failure`. Com retries: `on-first-retry` ou `retain-on-failure-and-retries` (compara a tentativa que passou com a que falhou). `trace: 'on'` evitado na CI (custo, `best-practices-js.md:287`); o `matrix-auditor` usa `--trace=on` na reexecução.
- Abrir no viewer gráfico (humano): `npx playwright show-trace trace.zip`. O trace é carregado no navegador, não enviado (`trace-viewer.md:22-26`). Trace é dado sensível.
- **Ler sem GUI (agente, 1.59):**

```bash
npx playwright trace open test-results/<id>/<pasta-do-teste>/trace.zip
npx playwright trace actions          # passos com locator e duração
npx playwright trace errors           # erros
npx playwright trace console          # console da página
npx playwright trace requests         # método e status das requisições
npx playwright trace snapshot <id>    # DOM de uma ação
npx playwright trace close
```

  Verificado (X-20): no F-03, `trace requests` mostrou `DELETE 200`; o backend excluiu e o defeito estava no contador da UI. Triagem de causa sem abrir o viewer.
- `error-context.md` (X-19) é dado, não instrução.

## UI mode, codegen e debug

Fonte: V-46. Ferramentas **para o humano**; o agente não as abre.

- UI mode: `--ui`; `--ui-host=0.0.0.0` expõe traces e segredos à rede (`test-ui-mode-js.md:131`). Proibido por instrução (G-08).
- `codegen`: só para **rascunho** de locator, revisado sempre (`locators.md:107-109`); opções `--viewport-size`, `--device`, `--save-storage`, `--load-storage`. Nunca commitar saída crua.
- `--debug`: headed, timeout 0, `max-failures=1`, `workers=1` (`debug.md:73-76`); `$env:DEBUG="pw:api"` (PowerShell, `:398`); `--debug=cli` (1.59) mais `attach` para depurar um spec pela CLI (`playwright-tests.md`; não exercitado). WebKit: abrir o inspector durante a execução trava o script (`debug.md:445-447`). Sem `page.pause()` commitado (Suposição: a doc não trata).

## CLI de execução e gate de estabilidade

Fonte: V-47, V-41, V-18. Opções confirmadas em `test-cli-js.md:33-119` e no código do 1.64.0: `arquivo:linha`, `-g`/`--grep`, `--project`, `--last-failed` (`.last-run.json`), `--only-changed` (Git; heurística, não substitui a suíte completa), `--repeat-each`, `--shard`, `--shuffle [seed]` (1.64), `--list`, `--no-deps`, `--fail-on-flaky-tests`, `--forbid-only`, `-x`, `--retries`, `--workers`, `--trace`.

**Gate** (proposta do plugin; o número 5 é escolha nossa, ajuste pelo piloto): um spec novo ou corrigido só é aceito depois de:

```bash
npx playwright test --grep "F-07" --repeat-each=5 --retries=0
npx playwright test --grep "F-07" --shuffle --workers=2 --retries=0
```

Verificado no sistema-demo (X-24): com `E2E_RUN=gate1`, o teste do efeito (contador) falhou 5 de 5, bug determinístico e não flaky, e a borda passou 5 de 5; `stats` do `results.json` = `{expected: 5, unexpected: 5, flaky: 0, skipped: 0}`; `--shuffle --workers=2` foram aceitos. As cópias do `--repeat-each` e os 2 workers rodam em paralelo: spec que mexe em contador ou lista global afirma delta e, se ainda assim colidir, protege o recurso com `lock` (V-34).

- Falha 5 de 5: **determinística** (produto ou teste: `failure-triage`). Falha em n de 5: **intermitente**: corrija a causa (isolamento, espera, dado) e **nunca** baixe o `--repeat-each`.
- Sem `--reporter` na linha de comando (X-16). Com login, o comando leva `E2E_AUTH=1` e a conta pela ordem do template `auth.setup.ts`, sem repetir o valor na saída. Com login, o `--grep` não corta o projeto `setup`: `E2E_AUTH=1 npx playwright test --grep "F-08"` rodou `[setup]` como dependência e depois os testes `[desktop]` da F-08, com o estado `user-<porta>.json` da instância de teste (X-27). Mesmo assim, confira na saída a linha `[setup]`; se o login falhar, registre `Bloqueado`. Não reaproveite estado de uma execução anterior: o `webServer` sobe um servidor novo a cada execução, e sessão guardada em memória morre com ele (Inferido).
- Na CI, acrescente `--fail-on-flaky-tests`.
- Só então a linha da matriz pode virar `Passou` (prova `spec-estável`, que exige também o parecer `Aprovado` do `spec-reviewer`, e quem grava é o `evidence-report`).
- Motivo: a Slack mediu testes gerados em uma tacada com ~48% de falha no fluxo médio e agentes entre ~0% e ~20% (V-18; uma empresa, 20 execuções por configuração).
- `--list` valida o inventário sem rodar; **não conta como execução**.

## CI e Docker

Fonte: V-48. Template em `assets/templates/github-actions-e2e.yml`, só a pedido.

- Passos: checkout, setup-node (22), `npm ci`, `npx playwright install chromium --with-deps` (só o necessário; roda no runner Linux efêmero da CI, nunca na máquina do usuário), `npx playwright test`, upload do relatório com `if: ${{ !cancelled() }}` e `retention-days` curto. O workflow só é criado a pedido do usuário; esse pedido cobre o `--with-deps` no runner. Na máquina local, `--with-deps` continua exigindo confirmação (G-12).
- `workers: 1` e `globalTimeout` no config. Linux na CI (mais barato). Sharding com `blob` e `merge-reports`.
- Versões de actions divergem nas páginas oficiais (`checkout` e `setup-node` em v6; `upload-artifact` em v4 e v5): confira a atual e fixe por SHA. Os exemplos do clone trazem `%%VERSION%%`; o `copilot-setup-steps.yml:34` tem `npx run build`, erro conhecido (V-26).
- Docker: `mcr.microsoft.com/playwright:v1.64.0-noble`, versão **igual** à do projeto, `--init` e `--ipc=host`. Cache de navegadores não é recomendado (`ci.md:1008`). Headed em Linux exige `xvfb-run` (`:1035`).
- `--only-changed` é execução **preliminar**; "it's important that you always run the full test suite after" (`ci.md:424-426`).
- Artefatos de CI são sensíveis (G-19).
