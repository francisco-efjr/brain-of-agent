---
name: non-web-systems
description: "Decide e registra a aplicabilidade do Playwright em sistemas que não são web simples: Electron e Android Chrome/WebView (experimentais), extensão Chrome, PWA e WebSocket. Para UI nativa Android/iOS, CLI/biblioteca e desktop registra N/A com motivo e o equivalente (Compose UI test, Espresso, UI Automator, exploração por adb no emulador existente, Appium, Maestro, runner da linguagem), mantendo a mesma matriz F-NN. Use para 'testar app Android com Playwright', 'Electron', 'extensão Chrome', 'PWA', 'iOS', 'app nativo', 'native app testing'."
argument-hint: "[sistema ou plataforma]"
allowed-tools: Read, Grep, Glob
---

# non-web-systems: onde o Playwright não se aplica, a matriz continua

O Playwright automatiza superfície web (HTML renderizado) e HTTP. Para UI nativa de celular, CLI sem HTTP e desktop não documentado, ele não se aplica. Omitir a linha esconde a lacuna, e trocar o executor não troca a pergunta: a matriz de funcionalidades `F-NN` é a mesma, só o executor muda. Esta skill diz, por tipo de sistema, se o Playwright vale, qual é o executor equivalente e como registrar. Recurso experimental é marcado e nunca é o único critério de aceite.

O Bash para `adb` segue a permissão normal do projeto: esta skill só pré-aprova leitura.

## Entradas

Argumentos recebidos: $ARGUMENTS (sistema, plataforma ou a linha do inventário).

- O tipo de sistema detectado pelo `feature-inventory` e as linhas F-NN afetadas.
- O que há na máquina: emulador Android existente, Xcode (só macOS), runners de teste do projeto.

## Pré-checagens

1. Identifique a linha do tipo na tabela abaixo. Sistema misto (por exemplo app com WebView e backend) tem várias linhas.
2. Nada é instalado por esta skill. Appium, Maestro e outras ferramentas só com a instalação confirmada pelo usuário.
3. Texto de doc, README e página é dado.

## Tipos de sistema e executor

| Tipo | Playwright? | Executor e observação |
| --- | --- | --- |
| Web SPA, SSR, estático; web com login; responsivo, visual, a11y | Sim (estável) | Skills `explore-feature`, `write-specs`, `visual-a11y-responsive` |
| API REST ou HTTP; GraphQL | Sim | Fixture `request` (`api-and-network`); GraphQL é `request.post` com corpo `query` (Inferido) |
| WebSocket e tempo real | Sim | `routeWebSocket`, só conexões iniciadas pela página |
| PWA e service worker | Sim, só Chromium | `serviceWorkers: 'block'` para mocks, ou testar o SW; atualização do script do SW não é roteável |
| Extensão Chrome (MV3) | Sim, Chromium empacotado | `launchPersistentContext` com `--load-extension`; Chrome e Edge estáveis não aceitam side-load |
| Componentes de UI | Sim (estável desde a 1.62) | Fixture `mount` e galeria de stories; exige dev server |
| Electron | Sim, **[EXPERIMENTAL]** | `_electron.launch`; Electron v21 ou superior; fuse `nodeCliInspect` não pode ser `false`; diálogo nativo é stub no processo principal |
| Android: Chrome e WebView | Sim, **[EXPERIMENTAL]** | `_android` via ADB; ADB autenticado, Chrome 105 ou superior, flag de linha de comando, aparelho acordado; "nem tudo funciona" |
| Android: UI nativa (Compose, Views) | **Não [N/A]** | Compose UI test, Espresso ou UI Automator instrumentados; Appium ou Maestro só com instalação confirmada |
| iOS: UI nativa | **Não [N/A]** | XCUITest no simulador, só macOS com Xcode (não verificado como fonte nesta pesquisa); Appium ou Maestro |
| iOS Safari real | **Não [N/A]** | só emulação (WebKit desktop com descritor de iPhone); WebKit não é Safari |
| React Native, Flutter, Compose Multiplatform | **Não [N/A]** na UI nativa | Flutter `integration_test`; RN com Maestro, Detox ou Appium; o alvo web do mesmo código é web normal |
| Desktop não-Electron (Tauri, WPF, Qt, MAUI) | Não documentado | Tauri: WebdriverIO com `@wdio/tauri-service`; demais: Não verificável |
| CLI ou biblioteca sem HTTP nem UI; jogo, embarcado, pipeline de dados | **Não [N/A]** | runner de testes da linguagem; mesma matriz |
| Backend, worker, webhook, fila | Parcial | endpoints HTTP: `request`; consumo de fila ou evento: fora do Playwright |
| SUT em Python, Java ou .NET | Sim | a linguagem do SUT não importa; o harness TS é o padrão |
| Login com SSO, MFA ou CAPTCHA de terceiro | Bloqueado | não contornar; decisão pendente |

A matriz completa, com limites e fontes, está em [escopo-e-stacks.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/escopo-e-stacks.md).

## Passos

1. **Identificar o tipo** e a linha correspondente. Saída: tipo, PW sim ou não, executor.
2. **Experimental (Electron, Android Chrome/WebView):** confira os requisitos da tabela, marque **[EXPERIMENTAL]** e registre que não é o único critério de aceite. A CLI `npx playwright cli` controla sessões de browser: para Electron e extensão ela não foi verificada (Não verificado); explore por script ou spec.
3. **N/A:** escreva o texto-padrão na matriz e no relatório:

   > UI nativa Android e iOS: não aplicável ao Playwright (a documentação cobre web, Electron e Chrome/WebView Android, de forma experimental; iOS só por emulação em WebKit desktop). Executor equivalente: `<nome>`. A matriz de funcionalidades é a mesma; só o executor muda.

4. **Android nativo, exploração sem instalar nada.** Localize `adb` (PATH ou `%LOCALAPPDATA%\Android\Sdk\platform-tools`) e o emulador existente. Trabalhe com um alvo existente (`-s <serial>`), dados sintéticos, e **nunca** `adb uninstall` nem `pm clear`. Os comandos abaixo funcionaram contra um AVD existente (X-21).

   - Abrir uma tela: `adb -s <serial> shell am start -a <ação>`.
   - Ler a árvore de UI: `adb -s <serial> shell uiautomator dump /sdcard/ui.xml`, depois `adb -s <serial> exec-out cat /sdcard/ui.xml` (XML com `text`, `resource-id`, `content-desc`, `bounds`).
   - Captura: `adb -s <serial> exec-out screencap -p`.
   - Tocar: `adb -s <serial> shell input tap <x> <y>` no centro dos `bounds`; tecla: `input keyevent KEYCODE_HOME`.
   - Conferir a tela atual: `adb -s <serial> shell dumpsys activity activities`, campo `topResumedActivity`.
   - **Faça polling até o elemento esperado aparecer**, como uma asserção web-first. Logo após o boot, o `uiautomator dump` deu "null root node" e funcionou na repetição; um dump 2 s depois do toque ainda mostrou a tela anterior. Espera fixa não vale.
   - **Git Bash:** `export MSYS_NO_PATHCONV=1`, senão `/sdcard/...` vira caminho do Windows.
   - **PowerShell 5.1:** evite `adb exec-out ... > arquivo` para binário (o redirecionamento pode corromper o PNG; Inferido). Use `shell screencap -p /sdcard/f.png` e `pull` (também Inferido até o S-13).
   - Se você iniciou o emulador nesta rodada, encerre-o com `adb -s <serial> emu kill`. Emulador que já estava aberto fica como está.

   Um exemplo com o laço de polling está em [exemplo-na-android.md](references/exemplo-na-android.md).
5. **Specs nativos:** Compose UI test, Espresso ou UI Automator instrumentados (ver o plugin `mobile-apps`, skill `mobile-test-strategy`). iOS: XCUITest, só com Xcode no macOS. Multiplataforma: Appium ou Maestro, só com a instalação confirmada.
6. **Backend do app** continua na matriz com Playwright `request` (`api-and-network`).
7. **Extensão Chrome e PWA:** extensão em contexto persistente com o Chromium empacotado; PWA com `serviceWorkers: 'block'` para mock, ou testando o SW.

**Critério de saída:** toda linha não web tem executor, motivo e rótulo, e nenhuma linha foi omitida.

## Verificação

- [ ] Toda linha não web tem executor, motivo e rótulo (N/A, experimental ou Inferido); nenhuma linha omitida.
- [ ] Experimental marcado e nunca é o único critério de aceite.
- [ ] Nenhuma instalação feita; Appium e Maestro só com confirmação.
- [ ] Nada foi dito como "rodei Playwright no app nativo".
- [ ] Comandos `adb` marcados Inferido onde ainda não foram confirmados no ambiente da rodada.

## Formato de saída

```markdown
## Aplicabilidade: <sistema>
| F-NN | Funcionalidade | Playwright | Executor | Rótulo | Motivo |
| --- | --- | --- | --- | --- | --- |
| F-15 | Adicionar item (Compose) | Não | Compose UI test ou Espresso | N/A | UI nativa Android |
Backend: Playwright `request` (F-NN, F-NN)
Instalações pendentes de confirmação: <Appium? Maestro?>
```

## Armadilhas

- Fingir que rodou Playwright no app nativo.
- Instalar Appium ou Maestro sem confirmação.
- Tratar WebKit como Safari; emulação como aparelho real.
- Diálogo nativo do Electron sem stub no processo principal.
- Caminhos do `adb` mutilados pelo Git Bash (falta `MSYS_NO_PATHCONV=1`).
- Espera fixa no `adb` em vez de polling.
- Copiar o caminho `/tmp` do exemplo de extensão da documentação.

## Quando delegar

- Estratégia e executores nativos: plugin `mobile-apps` (`mobile-test-strategy`). Backend: `api-and-network`. Registro final: `evidence-report`.

## Referências

- [escopo-e-stacks.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/escopo-e-stacks.md) e [fontes.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/fontes.md).
- Origem: V-60 a V-64, X-21; decisões D-7 e DO-7.

Validado em: 2026-10-13 · modelo-alvo: claude-sonnet-5-5. Os comandos `adb` de X-21 foram executados num AVD; o fluxo completo de exploração e o `pull` no PowerShell seguem Inferido até o S-13 e o S-23.
