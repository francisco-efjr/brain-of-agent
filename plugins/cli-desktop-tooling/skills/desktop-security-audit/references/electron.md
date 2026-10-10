# Electron: checklist de segurança (20 itens) e fuses

Verificado em 2026-10-10 contra V-16 (lista oficial `latest`, 20 recomendações numeradas) e V-48 (`@electron/fuses`, README). As expressões de busca, a severidade e os trechos de código são da fábrica (**Inferido**, conhecimento estável da API do Electron): confirme na documentação da versão usada (https://www.electronjs.org/docs/latest/tutorial/security). Nada aqui foi executado.

Sumário: [Itens 1 a 20](#itens-1-a-20) · [Fuses](#fuses-v-48) · [Trechos de referência](#trechos-de-referência) · [Padrões de busca](#padrões-de-busca)

## Itens 1 a 20

A numeração `#` segue a página oficial; os IDs `DSK-E` e as severidades padrão são os do `checklist-completo.md` do playbook (os itens 9 e 10 ficam em DSK-E09 e os itens 11 e 12 em DSK-E11). "Remoto" = a janela carrega conteúdo que o time não controla (site de terceiros, iframe, webview).

| ID | # | Verificar | Detectar | Sev. padrão |
| --- | --- | --- | --- | --- |
| DSK-E01 | 1 | Só conteúdo seguro (HTTPS/WSS) | `http://` ou `ws://` em `loadURL`, `src`, `connect` | Alta |
| DSK-E02 | 2 | Sem `nodeIntegration` com conteúdo remoto | `nodeIntegration: true` | Crítica se remoto; Alta se local |
| DSK-E03 | 3 | `contextIsolation` ligado | `contextIsolation: false` | Crítica se remoto; Alta se local |
| DSK-E04 | 4 | `sandbox` ligado (desligar o isolamento de contexto desliga o sandbox do processo) | `sandbox: false` | Alta |
| DSK-E05 | 5 | Pedidos de permissão tratados | ausência de `setPermissionRequestHandler` (e do verificador de permissão) | Média; Alta se remoto |
| DSK-E06 | 6 | `webSecurity` não desligado | `webSecurity: false` | Alta |
| DSK-E07 | 7 | CSP definida | ausência de `Content-Security-Policy` em HTML ou cabeçalhos de resposta | Média a Alta |
| DSK-E08 | 8 | Sem `allowRunningInsecureContent` | `allowRunningInsecureContent: true` | Alta |
| DSK-E09 | 9 e 10 | Sem recursos experimentais nem `enableBlinkFeatures` | `experimentalFeatures: true`, `enableBlinkFeatures` | Média |
| DSK-E11 | 11 e 12 | Sem `allowpopups` em `webview`; opções do `webview` validadas | `allowpopups`, `<webview` sem `will-attach-webview` | Média |
| DSK-E13 | 13 | Navegação limitada | ausência de `will-navigate` (e de `will-redirect`, quando houver redirecionamento) | Alta |
| DSK-E14 | 14 | Novas janelas limitadas | ausência de `setWindowOpenHandler` | Alta |
| DSK-E15 | 15 | `shell.openExternal` nunca com conteúdo não confiável | `openExternal(` com argumento não constante | Crítica se não validado |
| DSK-E16 | 16 | Electron atualizado | versão em `package.json`/lockfile | Média; compare com a versão atual da documentação |
| DSK-E17 | 17 | Remetente de toda mensagem IPC validado | `ipcMain.handle(`/`.on(` sem checar `event.senderFrame` | Alta |
| DSK-E18 | 18 | Evitar `file://`; preferir protocolo customizado (`protocol.handle`) | `loadFile(`, `file://` | Média |
| DSK-E19 | 19 | Fuses revistos | ver [Fuses](#fuses-v-48) | Média |
| DSK-E20 | 20 | APIs do Electron não expostas a conteúdo não confiável; preload expõe funções específicas | `exposeInMainWorld(..., ipcRenderer)`, `window.require`, objeto cru no `contextBridge` | Alta; Crítica se remoto |

Notas de leitura:

- "Alta se remoto" significa que o risco cresce quando a janela carrega conteúdo fora do controle do time. Documente o critério usado no relatório.
- A página não dá prioridade entre os 20 itens; a ordem de severidade acima é uma proposta da fábrica.
- Um preload que expõe uma função específica por `contextBridge.exposeInMainWorld` é o padrão aceito; expor `ipcRenderer` inteiro ou um `send` genérico por canal arbitrário é o achado (E20).

## Fuses (V-48)

O README lido lista nove fuses e não declara padrões. Valores recomendados são **Inferido** pelo significado de cada fuse; confirme o README da versão instalada.

| Fuse | Valor recomendado | Observação |
| --- | --- | --- |
| `RunAsNode` | desligado | Impede usar o binário do app como Node |
| `EnableCookieEncryption` | ligado | Mão única: desligar depois corrompe o cookie store (página de fuses do Electron, 2026-10-10) |
| `EnableNodeOptionsEnvironmentVariable` | desligado | |
| `EnableNodeCliInspectArguments` | desligado | |
| `EnableEmbeddedAsarIntegrityValidation` | ligado | Exige configuração de asar; a página de fuses do Electron (2026-10-10) diz que vale para macOS e Windows |
| `OnlyLoadAppFromAsar` | ligado (recomendação da fábrica, Inferido) | Restringe o carregamento ao `app.asar`; a página de fuses do Electron não dá recomendação geral e o usa junto com a validação de integridade |
| `LoadBrowserProcessSpecificV8Snapshot` | conforme a necessidade | |
| `GrantFileProtocolExtraPrivileges` | desligado | |
| `WasmTrapHandlers` | conforme a necessidade | |

Aplicação: `flipFuses` **depois** de empacotar e **antes** de assinar (gancho `afterPack` do electron-builder, `postPackage` ou `packageAfterCopy` do Forge); `strictlyRequireAllFuses` faz o build falhar se faltar algum fuse; no macOS arm64 sem assinatura logo em seguida é preciso `resetAdHocDarwinSignature: true`, senão o app falha a validação de assinatura.

Esta skill não executa `npx @electron/fuses` (código de terceiros baixado): ela só lê a configuração e recomenda. Mostre ao usuário o trecho abaixo para ele aplicar se quiser:

```js
// Ilustrativo, baseado no README do @electron/fuses; confirme nomes na versão instalada.
const { flipFuses, FuseVersion, FuseV1Options } = require('@electron/fuses');

await flipFuses(require('electron'), {
  version: FuseVersion.V1,
  strictlyRequireAllFuses: true,
  [FuseV1Options.RunAsNode]: false,
  [FuseV1Options.EnableCookieEncryption]: true,
  [FuseV1Options.EnableNodeOptionsEnvironmentVariable]: false,
  [FuseV1Options.EnableNodeCliInspectArguments]: false,
  [FuseV1Options.EnableEmbeddedAsarIntegrityValidation]: true,
  [FuseV1Options.OnlyLoadAppFromAsar]: true,
  [FuseV1Options.LoadBrowserProcessSpecificV8Snapshot]: false,
  [FuseV1Options.GrantFileProtocolExtraPrivileges]: false,
  [FuseV1Options.WasmTrapHandlers]: true, // conforme a necessidade
});
```

Em uso real, `flipFuses` recebe o caminho do binário empacotado (`require('electron')` aponta o Electron de desenvolvimento) e roda no gancho de empacotamento, antes da assinatura (Inferido; confirme no README). Com `strictlyRequireAllFuses`, todos os nove fuses precisam aparecer na lista, por isso `WasmTrapHandlers` está presente.

## Trechos de referência

Padrão de janela, preload e IPC (ilustrativo; confirme na documentação da versão).

```js
// main.js
const { app, BrowserWindow, ipcMain, session, shell } = require('electron');
const path = require('node:path');

const ORIGEM_APP = 'app://principal'; // protocolo customizado registrado com protocol.handle (item 18)

function criarJanela() {
  const win = new BrowserWindow({
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });

  win.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));          // item 14
  win.webContents.on('will-navigate', (event, url) => {                       // item 13
    if (new URL(url).origin !== ORIGEM_APP) event.preventDefault();
  });
  win.loadURL(`${ORIGEM_APP}/index.html`);
}

app.whenReady().then(() => {
  session.defaultSession.setPermissionRequestHandler(                         // item 5
    (webContents, permission, callback) => callback(false)
  );
  criarJanela();
});

ipcMain.handle('config:salvar', (event, dados) => {                           // item 17
  const origem = new URL(event.senderFrame.url).origin;
  if (origem !== ORIGEM_APP) return { ok: false, motivo: 'origem não permitida' };
  if (typeof dados?.tema !== 'string' || dados.tema.length > 32) {
    return { ok: false, motivo: 'dados inválidos' };
  }
  // ... gravar
  return { ok: true };
});

const ORIGENS_EXTERNAS = new Set(['https://docs.exemplo.com']);
function abrirExterno(urlTexto) {                                             // item 15
  const url = new URL(urlTexto);
  if (url.protocol === 'https:' && ORIGENS_EXTERNAS.has(url.origin)) shell.openExternal(url.href);
}
```

```js
// preload.js: expõe só o necessário (itens 3 e 20)
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  salvarConfig: (dados) => ipcRenderer.invoke('config:salvar', dados),
});

// Achado DSK-E20 (não faça): contextBridge.exposeInMainWorld('ipc', ipcRenderer);
```

## Padrões de busca

| Objetivo | Expressão (Grep) | Onde |
| --- | --- | --- |
| Configuração de janela | `nodeIntegration`, `contextIsolation`, `sandbox`, `webSecurity`, `allowRunningInsecureContent`, `experimentalFeatures`, `enableBlinkFeatures` | `**/*.{js,ts,mjs,cjs}` |
| Webview | `<webview`, `allowpopups`, `will-attach-webview` | `**/*.{html,js,ts}` |
| Navegação e janelas | `will-navigate`, `will-redirect`, `setWindowOpenHandler` | processo principal |
| Permissões | `setPermissionRequestHandler`, `setPermissionCheckHandler` | processo principal |
| `openExternal` | `openExternal(` e a origem do argumento | todo o código |
| IPC | `ipcMain.handle(`, `ipcMain.on(`, `senderFrame` | processo principal |
| Preload | `exposeInMainWorld`, `ipcRenderer` | `preload*` |
| CSP | `Content-Security-Policy` | `**/*.html`, código que define cabeçalhos de resposta |
| Protocolo | `loadFile(`, `file://`, `protocol.handle` | processo principal |
| Fuses | `flipFuses`, `FuseV1Options`, `afterPack`, `postPackage` | `forge.config.*`, `package.json`, `scripts/` |
| Versão | `"electron":` | `package.json`, lockfile |
