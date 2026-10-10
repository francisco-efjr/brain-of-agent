---
name: tauri-capabilities
description: Mede se a revisão de configuração Tauri v2 aponta CSP nula, capability única compartilhada, remote com curinga, AppManifest::commands e validação nos comandos Rust, sem inventar nomes de permissão.
tags: [cli-desktop-tooling, desktop-security-audit, desktop, seguranca]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: Achados por severidade com evidência, recomendação de uma capability por janela, remote justificado, CSP restrita, isolation e AppManifest, e aviso de que nomes de permissão variam por versão.
model: sonnet
---

Tenho um app Tauri v2 de anotações com duas janelas: a principal e uma de configurações, que carrega uma página de ajuda do nosso site. Dá uma olhada na segurança dessa configuração, por favor.

src-tauri/tauri.conf.json (trecho):

```json
{
  "productName": "notas",
  "version": "0.3.0",
  "app": {
    "windows": [
      { "label": "main", "title": "Notas", "url": "index.html" },
      { "label": "settings", "title": "Configurações", "url": "settings.html" }
    ],
    "security": { "csp": null }
  }
}
```

src-tauri/capabilities/default.json:

```json
{
  "identifier": "default",
  "description": "tudo que o app precisa",
  "windows": ["main", "settings"],
  "remote": { "urls": ["https://*"] },
  "permissions": ["core:default", "fs:default", "shell:default"]
}
```
