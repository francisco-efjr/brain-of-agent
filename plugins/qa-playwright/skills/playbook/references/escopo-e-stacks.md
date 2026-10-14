# Escopo, aplicabilidade e stacks

Onde o Playwright se aplica, onde não se aplica e qual executor equivalente entra, **mantendo a mesma matriz de funcionalidades F-NN**. Fontes: V-50, V-60..V-64, D-7, X-21. Use na etapa de aplicabilidade (passo 2 do ciclo) e para preencher a matriz de aplicabilidade do modo `PLAYWRIGHT-COMPLETO`.

## Sumário

- [Regra geral](#regra-geral)
- [Perguntas de decisão](#perguntas-de-decisão)
- [Marcação de maturidade](#marcação-de-maturidade)
- [Matriz por tipo de sistema (23 linhas)](#matriz-por-tipo-de-sistema-23-linhas)
- [Texto-padrão de N/A](#texto-padrão-de-na)
- [Equivalentes nativos e o que está verificado](#equivalentes-nativos-e-o-que-está-verificado)
- [Rota Android por `adb` (verificada)](#rota-android-por-adb-verificada)
- [Linguagens e test runners](#linguagens-e-test-runners)
- [Biblioteca contra test runner](#biblioteca-contra-test-runner)
- [Navegadores](#navegadores)

## Regra geral

Toda linha N/A mantém a mesma matriz `F-NN`; **muda o executor**. Omitir a linha não é permitido (G-28). Marcação: **[E]** estável · **[X]** experimental · **[L]** legado · **[N/A]**. O backend ou a API de um sistema nativo continua na matriz com Playwright `request` (linha 4).

## Perguntas de decisão

Fonte: V-50.

1. Há superfície web (HTML renderizado) ou HTTP? Se não, N/A.
2. Qual motor é o alvo? WebKit não é Safari; Firefox acompanha o Firefox estável.
3. Há suíte? Se sim, test runner (`@playwright/test`). Biblioteca só para script sem suíte.
4. Qual a linguagem do **sistema sob teste**? Não importa: o harness padrão é TypeScript (linha 21).

## Marcação de maturidade

Fonte: V-64. Reconfira nas release notes quando a versão mudar.

| Capacidade | Marcação | Fonte lida |
| --- | --- | --- |
| Electron | Experimental [X] | `class-electron.md:5` |
| Android (Chrome e WebView) | Experimental [X] | `class-android.md:5` |
| Selenium Grid | Experimental | `selenium-grid.md:3` |
| Integração JUnit | Experimental | `junit-java.md:3` |
| WebMCP | Recurso experimental de navegador (Chromium com `--enable-features=WebMCP`) | `class-webmcp.md:4, 9` |
| Eventos de toque | Legado [L] | `touch-events.md:3` |
| Component testing (`mount` com galeria) | Estável desde a 1.62 (pacotes `experimental-ct-*` congelados em 1.62.x) | V-58, conflito 4 |

Recurso experimental **nunca** é o único critério de aceite (G-29).

## Matriz por tipo de sistema (23 linhas)

Executor "PW" = Playwright. Exploração = como o `feature-explorer` olha o sistema.

| # | Tipo de sistema | PW? | Executor e abordagem | Exploração | Limites e pré-requisitos | Fontes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Web SPA, SSR, site estático | Sim [E] | `page`, locators e asserções web-first; `route` para estados de erro; `clock` para timers | `npx playwright cli` | Sem guia específico de SSR, SPA ou estático (Inferido). Atenção à hidratação: clique sem efeito antes dela (`navigations.md:103-121`) | V-27..V-32, V-52, V-53 |
| 2 | Web com login e papéis | Sim [E] | Projeto `setup` e `storageState` por papel; a rota que o papel **não** deve acessar entra na matriz | `state-load` do estado gerado pelo `setup`; nunca `fill` de senha | `sessionStorage` não persiste; estado vale como credencial; SSO, MFA ou CAPTCHA de terceiro: `Bloqueado` (Inferido) | V-37, V-38, V-23 |
| 3 | Responsivo, visual, acessibilidade | Sim [E] | Emulação por projeto, `toHaveScreenshot`, ARIA snapshot, axe | `open --device`, `resize`, `set-color-scheme` (exercitados, X-26) | axe não cobre tudo (teclado e leitor de tela são manuais); baseline por ambiente; `@axe-core/playwright` é dependência nova (confirmar); WebKit não é Safari | V-54..V-57 |
| 4 | API REST ou HTTP | Sim [E] | Fixture `request`; híbrido API mais UI | `curl` ou `Invoke-RestMethod` em `127.0.0.1` (Inferido) | Sem contrato, schema OpenAPI nem carga | V-51 |
| 5 | GraphQL | Sim (Inferido) | `request.post` com corpo `query` | idem | Sem guia na documentação | V-51 |
| 6 | WebSocket e tempo real | Sim [E] | `routeWebSocket` (1.48), evento `websocket` | A CLI mostra rede; o mock vai no spec | Só conexões iniciadas pela página | V-52 |
| 7 | PWA e service worker | Sim, só Chromium [E] | `serviceWorkers: 'block'` para mocks, ou testar o SW (cache, offline) | CLI com `network-state-set` | Atualização do script do SW não é roteável (issue 14711); `route` não vê requisição do SW | V-63, V-52 |
| 8 | Extensão Chrome (MV3) | Sim, Chromium empacotado [E] | `launchPersistentContext` e `--load-extension`; `extensionId` pela URL do service worker | CLI não verificada para extensão (Não verificado); explorar por script ou spec | Chrome e Edge estáveis não aceitam side-load; não copie o caminho `/tmp` do exemplo | V-62 |
| 9 | Componentes de UI (React, Vue e outros) | Sim [E] (desde 1.62) | Fixture `mount` e galeria de stories | Dev server da galeria e CLI | Exige galeria e dev server; `init-skills` não rodar sem pedido | V-58 |
| 10 | Electron | Sim **[X]** | `_electron.launch`; stub de diálogo nativo no processo principal | Por script ou spec (a CLI controla sessões de navegador; Não verificado para Electron) | Electron v21+; fuse `nodeCliInspect` não pode ser `false`; nunca único critério de aceite | V-60, V-64 |
| 11 | Android: Chrome e WebView | Sim **[X]** | `_android` via ADB | Por script ou spec | ADB autenticado, Chrome 105+, flag de linha de comando, aparelho acordado; "nem tudo funciona"; só JavaScript | V-60, V-64 |
| 12 | Android: UI nativa (Compose, Views) | **Não** [N/A] | Compose UI test, Espresso ou UI Automator instrumentados; Appium ou Maestro como multiplataforma, só com instalação confirmada | `adb` no emulador já existente, sem instalar nada: **Verificado** (X-21) | Compose e Espresso têm fonte no plugin `mobile-apps`; UI Automator como framework instrumentado e Appium e Maestro **não validados** aqui; backend e API do app vão na linha 4 | V-61, X-21, D-7 |
| 13 | iOS: UI nativa | **Não** [N/A] | XCUITest no simulador (só macOS com Xcode); Appium ou Maestro | Simulador só com Xcode; no Windows, Não verificável: entregue o comando | XCUITest, Detox e Patrol **não verificados** como fonte oficial; sem iOS na documentação do Playwright | V-61 |
| 14 | iOS Safari real | **Não** [N/A] | Só emulação (WebKit desktop mais descritor de iPhone); aparelho ou nuvem para o real | `open --device="iPhone 15"` é emulação | WebKit não é Safari (`browsers.md:590`) | V-61, V-54 |
| 15 | Híbrido (WebView dentro de app nativo) | Parcial | Parte web em Android: linha 11 [X]; parte nativa: linha 12 | idem | Sem fonte lida para iOS | V-61 |
| 16 | React Native, Flutter, Compose Multiplatform (UI nativa) | **Não** [N/A] | Flutter `integration_test`; RN com Maestro, Detox ou Appium; o alvo **web** do mesmo código vale como linha 1 | Sem exploração por Playwright | Particularidades do Flutter web (árvore semântica) Não verificadas | V-61 |
| 17 | Desktop não Electron (Tauri, WPF, WinForms, Qt, MAUI) | **Não documentado** | Tauri: WebdriverIO com `@wdio/tauri-service` (ponteiro oficial lido); os demais: Não verificável | Sem exploração por Playwright | Fora do escopo documentado do Playwright | V-61, lacuna 7 |
| 18 | CLI ou biblioteca sem HTTP nem UI | **Não** [N/A] | Runner de testes da linguagem; mesma matriz | Sem exploração por Playwright | Playwright exige superfície web ou HTTP | V-50 |
| 19 | CLI ou biblioteca **com** superfície HTTP (servidor de dev, docs, UI embutida) | Sim, para essa superfície | Linhas 1 e 4 | CLI | O resto da CLI cai na linha 18 | V-50 |
| 20 | Backend, worker, webhook, fila | Parcial | Endpoints HTTP: linha 4; consumo de fila ou evento: fora do Playwright | `curl` | Webhook duplicado e fora de ordem ficam em `backend-api` e `qa-testing` | V-51, Inferido |
| 21 | SUT em Python, Java ou .NET | Sim (a linguagem do SUT não importa) | Harness TypeScript por padrão; `pytest-playwright`, JUnit [X], MSTest ou NUnit se o projeto já usa | `npx playwright cli` exige Node | NUnit só `ParallelScope.Self`; JUnit experimental; flags de artefato só valem para as fixtures padrão | V-50 |
| 22 | Jogo ou engine, embarcado ou IoT, pipeline de dados ou ML sem UI web | **Não** [N/A] | Runner do segmento; mesma matriz | Sem exploração por Playwright | Sem superfície web (Inferido) | V-50 |
| 23 | Login com SSO, MFA ou CAPTCHA de terceiro | Bloqueado | Conta de teste do staging sem MFA, ou fixture de auth fornecida pelo dono; **não contornar** | Sem exploração | Decisão pendente; nunca burlar CAPTCHA (Inferido) | V-37, G-33 |

## Texto-padrão de N/A

Use como está, trocando o executor (V-61):

> UI nativa Android e iOS: não aplicável ao Playwright (a documentação cobre web, Electron e Chrome/WebView Android, de forma experimental; iOS só por emulação em WebKit desktop). Executor equivalente: `<nome>`. A matriz de funcionalidades é a mesma; só o executor muda.

Registre na matriz: motivo, executor, rótulo (Verificado, Inferido, Não verificado) e a fonte. A busca por `iOS`, `iPadOS`, `Xcode`, `Safari on` e `simulator` em `docs/src` (exceto release notes) não achou ocorrência, e `AndroidSelector` é usado mas não definido em `docs/src` (V-61).

## Equivalentes nativos e o que está verificado

| Equivalente | Estado da verificação |
| --- | --- |
| Compose UI test, Espresso | Têm fonte no plugin `mobile-apps` (`mobile-test-strategy`); não reverificados nesta pesquisa |
| UI Automator (framework instrumentado) | Não validado aqui. A **rota por `adb`** (dump, screencap, input) foi **Verificada** por execução (X-21) |
| Appium, Maestro | Página oficial lida (V-61); capacidades **não testadas**. Só com instalação confirmada pelo usuário (G-11) |
| Flutter `integration_test` | Página oficial lida (`flutter drive`, aparelho ou emulador; também desktop e web) |
| Tauri (WebdriverIO e `@wdio/tauri-service`) | Página oficial lida; `tauri-driver` direto só em Windows e Linux |
| XCUITest, Detox, Patrol | **Não verificados** como fonte oficial |

Híbridos têm parte web que o Playwright cobre apenas em Android; sem fonte lida para iOS (V-61).

## Rota Android por `adb` (verificada)

Fonte: X-21. Verificada por execução em Windows com o AVD existente Pixel_10 (Android 17), sem instalar nada. Use quando o app é nativo, há emulador e a linha da matriz é N/A de Playwright. Exploração, não spec: o spec nativo é Compose UI test, Espresso ou UI Automator instrumentado (`mobile-apps:mobile-test-strategy`).

1. Localize `adb` e o emulador sem instalar: SDK em `%LOCALAPPDATA%\Android\Sdk`. Inicie o AVD existente com o `emulator.exe` do SDK (`Start-Process`, desacoplado) e chame o `adb` com `-s emulator-5554`. Não suba AVD novo, não use `adb uninstall` nem `pm clear`; dados sintéticos.
2. O que funcionou: `am start -a android.settings.SETTINGS`; `uiautomator dump /sdcard/ui.xml` seguido de `exec-out cat` (XML com `text`, `resource-id`, `content-desc`, `bounds`); `exec-out screencap -p` (PNG 1080×2424); `input tap <x> <y>` no centro dos `bounds`; `dumpsys activity activities` e a linha `topResumedActivity` (confirmou `com.android.settings/.SubSettings`); `input keyevent KEYCODE_HOME`; `emu kill`.
3. **Armadilhas:** (a) logo após o boot, `uiautomator dump` deu "null root node returned by UiTestAutomationBridge" e funcionou na repetição; (b) um dump 2 s depois do tap ainda mostrou a tela anterior. **Faça polling até o elemento esperado aparecer, como uma asserção web-first, nunca com espera fixa.** (c) No Git Bash, use `MSYS_NO_PATHCONV=1` para `/sdcard/...` não virar caminho do Windows.
4. No PowerShell 5.1, evite `adb exec-out ... > arquivo` para binário: o redirecionamento pode corromper o PNG (Inferido; use `adb pull` depois de gravar em `/sdcard`, S-13).
5. A asserção do efeito vale igual: o esperado vem de fonte (requisito, doc, teste, UI) e o veredito é `Passou por exploração` com a prova `exploração`, até existir spec nativo.

## Linguagens e test runners

Fonte: V-50. JS e TS são o padrão do plugin.

| Stack do SUT ou do harness | Runner e observações |
| --- | --- |
| JavaScript e TypeScript | `@playwright/test` (padrão); asserções web-first só aqui |
| Python | `pytest-playwright` é o recomendado (`languages.md:19`); flags `--browser`, `--headed`, `--tracing`, `--video`, `--screenshot` valem **só** para as fixtures padrão (`test-runners-python.md:29-41`); o exemplo de `browser_context_args` com marker é inconsistente (V-26) |
| Java | Integração JUnit é experimental (`junit-java.md:3`); TestNG citado sem guia (`languages.md:26`) |
| .NET | MSTest sem paralelismo por método; NUnit só `ParallelScope.Self`; xUnit citado (`test-runners-csharp.md:62-75`) |
| Qualquer SUT, harness TS | A linguagem do sistema não importa; `npx playwright cli` exige Node (V-50) |

Java e .NET: só os guias de runner foram lidos (lacuna 14).

## Biblioteca contra test runner

A biblioteca (`playwright` sem `@playwright/test`) exige criar navegador, contexto e página e fechar tudo, e **não tem asserções web-first**; elas só existem no test runner (`library-js.md:106-109`, V-50). Para o plugin, que exige efeito assertado e gate, use o test runner.

## Navegadores

Firefox alinhado ao Firefox estável, sem build de marca (`browsers.md:584`). WebKit derivado do WebKit main, com codecs que variam por SO (`browsers.md:590-592`): não é Safari. Chrome e Edge instalados entram por `channel` (X-04). Chromium baixado por `install chromium` serve a extensão e à CI.
