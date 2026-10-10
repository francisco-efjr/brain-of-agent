# Stacks desktop e segurança (Electron, Tauri, .NET, Qt)

Sumário: 1. Fronteira de confiança · 2. Electron: 20 itens · 3. Electron: fuses · 4. Tauri v2 · 5. WPF, MVVM Toolkit, WinUI 3, MAUI · 6. Qt · 7. Matriz qualitativa de stack · 8. Severidade e método de auditoria · 9. Lacunas · 10. Exemplos

Fontes: V-16 (Electron, A), V-48 (fuses, B), V-19 e V-47 (Tauri, A), V-33 a V-37 (.NET, A e B), V-38 e V-39 (Qt, B), V-65 (comunidade, B, N=1). A auditoria é leitura de configuração e código: o app nunca é executado, nada é instalado e `npx @electron/fuses` não é rodado. Padrões de busca (`grep`) e severidades são da fábrica (Inferido). Confira a versão do Electron ou do Tauri antes de citar opção: `package.json`, `Cargo.lock`, `src-tauri/tauri.conf.json`.

## 1. Fronteira de confiança (comece aqui)

Antes de qualquer checklist, mapeie: (1) o processo privilegiado (main do Electron, núcleo Rust do Tauri, processo .NET); (2) o conteúdo que roda nas janelas (local empacotado ou remoto); (3) a ponte entre os dois (preload e IPC, comandos do Tauri); (4) quem pode criar janelas. Quase todo item das duas listas oficiais é uma forma de negar acesso por padrão. Saída: tabela `janela · origem do conteúdo · preload · canais IPC ou comandos · permissões` (template `relatorio-auditoria-desktop.md`).

## 2. Electron: os 20 itens da página oficial (V-16)

Numeração da página. "Detecção" é busca sugerida pela fábrica (Inferido).

| # | Recomendação | Detecção (leitura) | Sev. padrão (Inferido) |
| --- | --- | --- | --- |
| 1 | Carregar só conteúdo seguro (HTTPS/WSS) | `loadURL('http://`, `ws://` | Alta com conteúdo remoto |
| 2 | Sem `nodeIntegration` com conteúdo remoto | `nodeIntegration: true` | Crítica com conteúdo remoto |
| 3 | Ligar `contextIsolation` | `contextIsolation: false` | Crítica com conteúdo remoto |
| 4 | Ligar `sandbox` (desligar isolamento, por exemplo com `nodeIntegration: true`, também desliga o sandbox daquele processo) | `sandbox: false` | Alta |
| 5 | Tratar pedidos de permissão | ausência de `setPermissionRequestHandler` | Média |
| 6 | Não desligar `webSecurity` | `webSecurity: false` | Alta |
| 7 | Definir CSP | ausência de meta CSP ou cabeçalho | Média a alta |
| 8 | Sem `allowRunningInsecureContent` | `allowRunningInsecureContent: true` | Alta |
| 9 | Sem recursos experimentais | `experimentalFeatures: true` | Média |
| 10 | Sem `enableBlinkFeatures` | `enableBlinkFeatures` | Média |
| 11 | Sem `allowpopups` em webview | `allowpopups` | Média |
| 12 | Validar opções do webview | ausência de `will-attach-webview` se há `<webview>` | Média |
| 13 | Limitar navegação | ausência de `will-navigate` | Alta com conteúdo remoto |
| 14 | Limitar novas janelas | ausência de `setWindowOpenHandler` | Alta com conteúdo remoto |
| 15 | `shell.openExternal` nunca com conteúdo não confiável | `openExternal(` com variável | Crítica se a URL vem de conteúdo remoto |
| 16 | Electron atualizado | versão em `package.json` | Média |
| 17 | Validar o `sender` de toda mensagem IPC | `ipcMain.handle(` e `ipcMain.on(` sem checar `event.senderFrame` | Alta |
| 18 | Evitar `file://`; protocolo customizado (`protocol.handle`) | `loadFile`, `file://` | Média |
| 19 | Revisar fuses | ver seção 3 | Média |
| 20 | Não expor APIs do Electron a conteúdo não confiável | preload que expõe `ipcRenderer` cru | Alta |

A lista da página não tem prioridade própria: a severidade acima é da fábrica. Comportamento em runtime é Não verificável por leitura.

Padrão seguro (exemplo da fábrica, não executado; APIs conhecidas do Electron, confira a doc da versão):

```js
// main.js
const win = new BrowserWindow({
  webPreferences: { contextIsolation: true, sandbox: true, nodeIntegration: false, preload: path.join(__dirname, 'preload.js') }
});
ipcMain.handle('arquivo:abrir', async (event) => {
  if (new URL(event.senderFrame.url).origin !== 'app://principal') throw new Error('remetente não autorizado');
  return dialog.showOpenDialog(win, { properties: ['openFile'] });
});
win.webContents.setWindowOpenHandler(({ url }) => {
  if (url === 'https://exemplo.com/ajuda') shell.openExternal(url);  // URL fixa
  return { action: 'deny' };
});

// preload.js: função específica, nunca ipcRenderer cru
contextBridge.exposeInMainWorld('api', { abrirArquivo: () => ipcRenderer.invoke('arquivo:abrir') });
```

## 3. Electron: fuses (`@electron/fuses`, V-48)

Nove fuses no README: `RunAsNode`, `EnableCookieEncryption`, `EnableNodeOptionsEnvironmentVariable`, `EnableNodeCliInspectArguments`, `EnableEmbeddedAsarIntegrityValidation`, `OnlyLoadAppFromAsar`, `LoadBrowserProcessSpecificV8Snapshot`, `GrantFileProtocolExtraPrivileges`, `WasmTrapHandlers`. O README não declara padrões.

| Fuse | Valor recomendado | Rótulo |
| --- | --- | --- |
| `RunAsNode` | desligado | Inferido |
| `EnableNodeOptionsEnvironmentVariable` | desligado | Inferido |
| `EnableNodeCliInspectArguments` | desligado | Inferido |
| `GrantFileProtocolExtraPrivileges` | desligado | Inferido |
| `EnableCookieEncryption` | ligado (a página do Electron avisa que a mudança é de mão única: desligar depois corrompe o cookie store) | Inferido |
| `OnlyLoadAppFromAsar` | ligado (restringe o carregamento ao `app.asar`). A página de fuses do Electron, lida em 2026-10-10, não dá recomendação geral para este fuse e o associa à validação de integridade; "ligado" é a recomendação da fábrica | Inferido |
| `EnableEmbeddedAsarIntegrityValidation` | ligado (exige configuração de asar; a página do Electron de 2026-10-10 diz que vale para macOS e Windows) | Inferido |
| `LoadBrowserProcessSpecificV8Snapshot`, `WasmTrapHandlers` | conforme a necessidade | Inferido |

Procedimento: aplicar com `flipFuses` depois de empacotar e antes de assinar (gancho `afterPack` do electron-builder, `postPackage` ou `packageAfterCopy` do Forge); `strictlyRequireAllFuses` falha o build se faltar fuse; macOS arm64 sem assinatura logo em seguida exige `resetAdHocDarwinSignature: true`. A fábrica lê e recomenda; quem roda a ferramenta é o usuário.

## 4. Tauri v2 (V-19, V-47)

| Controle | Regra | Fonte |
| --- | --- | --- |
| Fronteira | Núcleo Rust com acesso irrestrito; o WebView só vê o que o IPC expõe; inspecione e defina fortemente todos os dados que cruzam a fronteira | V-19 |
| Capabilities | Arquivos em `src-tauri/capabilities` (JSON ou TOML) com `identifier`, `description`, `windows`, `platforms`, `permissions`, `remote.urls`; se `tauri.conf.json` listar capabilities, só elas entram no build | V-19 |
| Uma capability por janela | `windows` explícito; a fronteira segue o rótulo da janela, não o título; controle quem pode criar janelas | V-19 |
| `remote` | Nenhum `remote.urls` sem justificativa escrita; curinga `https://*` é achado | V-19 (Inferido para a severidade) |
| Comandos | Por padrão todos os comandos registrados em `invoke_handler` são chamáveis por todas as janelas, a menos que `AppManifest::commands` em `build.rs` restrinja | V-19 |
| Entrada | Validar e tipar a entrada de cada comando Rust | V-19 |
| Isolation | `app.security.pattern` com `"use": "isolation"` e `options.dir`; um `<iframe>` em sandbox intercepta a mensagem IPC (cifrada com AES-GCM, chave de runtime); manter a isolation app mínima; no Windows arquivos externos não carregam no iframe e módulos ES não funcionam; ligar quando o frontend usa dependências de terceiros | V-47 |
| CSP | Só ativa se estiver na configuração; `default-src` restrito (exemplo da página: `'self' customprotocol: asset:`); `connect-src` com `ipc: http://ipc.localhost`; hashes e nonces são acrescentados no build; `'wasm-unsafe-eval'` para WebAssembly; sem CDN | V-47 |
| Isolation e CSP não substituem capabilities | Camadas diferentes | V-47 |
| WebView do sistema | Atualizações de segurança mais rápidas, sem garantia de compatibilidade | V-19, V-65 |

Exemplo de capability (da fábrica, ilustrativo; nomes de permissão variam por plugin e versão, confira a doc):

```json
{
  "identifier": "janela-principal",
  "description": "Permissões mínimas da janela principal",
  "windows": ["main"],
  "permissions": ["core:default"]
}
```

`window.__TAURI_ISOLATION_HOOK__` aparece só em código de exemplo da página: trate como detalhe de implementação a conferir na versão usada. A URL correta da isolation é `/concept/inter-process-communication/isolation/`.

## 5. .NET: WPF, MVVM Toolkit, WinUI 3, MAUI

- **WPF (V-33):** só Windows, inclusive sobre .NET moderno. XAML para aparência, code-behind para comportamento (`x:Class`, `InitializeComponent`). Prefira comandos a handlers de clique para ações reutilizáveis; `Binding` e `DataContext`; `ControlTemplate` para aparência. A página recomenda migrar de .NET Framework para .NET. Não cita MVVM, acessibilidade, segurança nem empacotamento.
- **MVVM Toolkit (V-34, MIT):** `ObservableObject`, `ObservableRecipient`, `ObservableValidator`, `RelayCommand` e `AsyncRelayCommand`, `IMessenger` (`WeakReferenceMessenger`, `StrongReferenceMessenger`), `Ioc`. ViewModel sem referência a controles. A página não trata de geradores de código e não lista MAUI: não afirme compatibilidade nem incompatibilidade.
- **WinUI 3 (V-35):** framework nativo recomendado para novos apps desktop, parte do Windows App SDK, C# ou C++, Windows 10 1809 (build 17763) ou posterior. Acessibilidade por UI Automation. Sete itens: (1) nome acessível em todo controle interativo; (2) ordem de Tab revisada; (3) alto contraste sem cor fixa; (4) texto escala com o sistema sem cortar; (5) `AutomationPeer` em controle customizado; (6) fluxo crítico com Narrator (verificação humana); (7) checagem automática no CI. Conteúdo DirectX em `SwapChainPanel` ou `SurfaceImageSource` não é acessível por padrão.
- **MAUI (V-37, B):** projeto único para Android, iOS, macOS (Mac Catalyst) e Windows (WinUI 3); iOS e macOS exigem um Mac para compilar. Só vale com alvo mobile ou macOS além do Windows.
- **Empacotamento (V-36):** framework-dependent (padrão: pequeno, atualizável pelo sistema, depende do runtime) contra self-contained (controle de versão, maior); `PublishSingleFile` só para não empacotado e self-contained (Windows App SDK 1.5 ou posterior); publicar por RID (`win-x64`, `win-arm64`) ou bundle MSIX; Arm64EC para bases C/C++ grandes. Detalhe de instaladores em `distribuicao-assinatura-update.md`.

## 6. Qt (V-38, V-39; não é aconselhamento jurídico)

- Implantação: `windeployqt` (`--release`, `--qmldir <dir>` para QML, `--no-translations`, `--no-compiler-runtime`); o instalador inclui o VC++ Redistributable oficial; dependências de terceiros à mão; build não relocável pede `qt.conf`. macOS: `macdeployqt` (`-dmg`, `-qmldir=`); a assinatura padrão é ad hoc, então use `-codesign=<identidade>`; `-sign-for-notarization=<identidade>` liga Hardened Runtime, timestamp e `-codesign`; no máximo um `.entitlements` em `Contents/Resources/`.
- Licença: comercial, ou LGPLv3/GPLv3 se cumprir os termos. **14 módulos** não estão disponíveis sob LGPLv3 (Canvas Painter, CoAP, Graphs, GRPC, HTTP Server, Lottie Animation, MQTT, Network Authorization, Qml Compiler, Quick 3D, Quick 3D Physics, Quick Timeline, Virtual Keyboard, Wayland Compositor). Passo: liste os módulos do projeto e cruze com a lista na página de licenciamento. As obrigações detalhadas da LGPLv3 não foram lidas; encaminhe a assessoria jurídica.
- Segurança do Qt e acessibilidade de Qt: sem fonte (lacuna).

## 7. Matriz qualitativa de stack (sem números; V-65 é N=1)

| Critério | Electron | Tauri v2 | WinUI 3 | WPF | MAUI | Qt |
| --- | --- | --- | --- | --- | --- | --- |
| Plataformas | Win, macOS, Linux | Win, macOS, Linux | Windows | Windows | Win, macOS, Android, iOS | Win, macOS, Linux |
| Linguagem | JS/TS (Chromium + Node) | Rust + WebView do sistema | C#/C++ | C# | C# | C++/QML |
| MSIX e Store | Possível (Inferido; V-65 trata a falta de MSIX como bloqueio de migração para Tauri) | Só MSI e NSIS; a Store aceita EXE ou MSI (V-46) | Sim (V-36, V-40) | Inferido: MSIX é possível em apps .NET | Windows via WinUI 3 (V-37) | Instalador próprio (V-38) |
| Updater | `autoUpdater`/Squirrel (V-18) | Plugin com assinatura obrigatória (V-20) | App Installer (V-40) | App Installer ou terceiros | por plataforma | sem fonte |
| Segurança padrão | Checklist oficial de 20 itens (V-16) | Capabilities por janela (V-19) | sem fonte lida | sem fonte lida | sem fonte lida | sem fonte lida |
| Acessibilidade | sem fonte | sem fonte | Oficial (V-35) | sem página localizada | sem fonte | sem fonte |
| Linux sério | Chromium consistente | Testar WebKitGTK cedo (HN, Não verificado) | n/a | n/a | n/a | Sim |
| Licença | Inferido: código aberto | Apache-2.0 (repositório, V-46) | Inferido: código aberto | Código aberto em dotnet/wpf (V-33) | Inferido: código aberto | Comercial ou LGPLv3/GPLv3; 14 módulos só-GPL (V-39) |

Filtros duros em ordem (o ADR registra cada um): MSIX ou identidade de pacote exigidos; alvo mobile; só Windows moderno; Node completo no processo principal; licença de código fechado com Qt; Linux sério. Protótipo obrigatório antes de decidir: assinar, instalar, atualizar e desinstalar em máquina limpa; WebView em Linux; ordem de assinatura do updater do Tauri.

## 8. Severidade e método de auditoria (Inferido, da fábrica)

Crítica: conteúdo remoto com `nodeIntegration` ou sem `contextIsolation`; `openExternal` com URL não validada. Alta: IPC sem validação de remetente; `sandbox` ou `webSecurity` desligados; `remote` com curinga no Tauri. Média: CSP ausente (média a alta), fuse fora do recomendado, versão desatualizada. Baixa: higiene. Cada achado leva `arquivo:linha` ou "não encontrado em [lista de arquivos pesquisados]". Segredos de assinatura e updater são assunto de `distribuicao-assinatura-update.md`.

## 9. Lacunas que afetam a auditoria

Segurança e acessibilidade de Qt e de .NET desktop; acessibilidade de Electron e Tauri; crash reporting; runtime (CSP efetiva, comportamento de janelas) só por teste manual. Declare-as no relatório como Não verificável.

## 10. Exemplo de achados

| ID | Severidade | Evidência | Correção |
| --- | --- | --- | --- |
| DSK-E02 | Crítica | `main.js:12` `nodeIntegration: true`, `contextIsolation: false`, `loadURL('https://app.exemplo.com')` | Ligar isolamento e sandbox; preload com função específica; CSP |
| DSK-E17 | Alta | `main.js:30` `ipcMain.handle('run', (e, cmd) => execSync(cmd))` sem checar remetente | Remover o canal; se necessário, lista fechada de ações e validação de `senderFrame` |
| DSK-T08 | Média | `tauri.conf.json` `"csp": null` | Definir CSP com `default-src` restrito |
