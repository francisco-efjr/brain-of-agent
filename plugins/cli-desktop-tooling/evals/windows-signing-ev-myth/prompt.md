---
name: windows-signing-ev-myth
description: Mede se a revisão de release no Windows desfaz o mito de que EV é obrigatório, aponta senha literal em /p, flags /fd e /td ausentes e não afirma ter assinado ou verificado nada.
tags: [cli-desktop-tooling, desktop-release-checklist, release, windows]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: Resposta corrige a premissa sobre EV com fonte e data, aponta o comando de assinatura inseguro, recomenda signtool verify, avisa sobre SmartScreen na primeira release e trata a ordem do updater do Tauri como hipótese.
model: sonnet
---

Comprei um certificado EV porque a Microsoft exige isso desde 2023, então estou tranquilo. No CI eu assino assim:

```
signtool sign /f cert.pfx /p MinhaSenha123 /tr http://timestamp.exemplo.com app.exe
```

O app é em Tauri v2 e eu distribuo direto pelo meu site, sem Store. Posso lançar amanhã?
