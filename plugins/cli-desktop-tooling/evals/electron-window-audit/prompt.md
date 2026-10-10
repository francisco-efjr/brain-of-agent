---
name: electron-window-audit
description: Mede se a auditoria de um main.js Electron classifica como crítico nodeIntegration com conteúdo remoto, IPC que executa comando sem validar remetente e openExternal sem validação, sem executar o app.
tags: [cli-desktop-tooling, desktop-security-audit, desktop, seguranca]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: Achados críticos e altos com evidência, recomendação de preload com funções específicas, CSP, permissões e navegação, menção a fuses e declaração de que o app não foi executado.
model: sonnet
---

Nosso app Electron (o package.json diz electron ^30.0.0, roda em Windows e macOS) vai ser lançado na semana que vem e ele abre o nosso painel web hospedado. Faz uma auditoria de segurança antes do release? Esse é o main.js inteiro:

```js
const { app, BrowserWindow, ipcMain, shell } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: { nodeIntegration: true, contextIsolation: false },
  });
  win.loadURL('https://app.exemplo.com');
  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

ipcMain.handle('run', (e, cmd) => require('child_process').execSync(cmd).toString());

app.whenReady().then(createWindow);
```
