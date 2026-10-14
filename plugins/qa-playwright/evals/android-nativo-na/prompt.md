---
name: android-nativo-na
description: "Caso de aplicabilidade: o usuário quer validar todas as telas de um app Android nativo (Kotlin, Compose) com Playwright. Mede se o plugin registra N/A com motivo e executor equivalente, mantém a mesma matriz F-NN, rotula a exploração por adb como não verificada neste app, mantém o backend com request e não manda instalar Appium ou Maestro sem confirmação."
tags: [qa-playwright, non-web, android, applicability]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 480
runs: 3
expected_outcome: "Registra que a UI nativa Android (Compose) é N/A para o Playwright, com motivo e a fonte (a documentação cobre web, Electron e Chrome/WebView Android, estes experimentais); propõe Compose UI test, Espresso ou UI Automator e a exploração por adb no emulador existente, rotulada Inferido ou Não verificado; mantém as linhas F-NN com executor; deixa o backend para o Playwright request; Appium e Maestro só com instalação confirmada; não finge rodar Playwright no app."
model: sonnet
---
Quero usar Playwright para validar todas as telas do meu app Android (Kotlin, Jetpack Compose). Tenho um emulador (AVD) já criado aqui no Android Studio. O app tem estas telas e ações:

- Login com e-mail e senha
- Lista de pedidos (puxar para atualizar, filtrar por status)
- Detalhe do pedido (cancelar pedido, compartilhar)
- Perfil (alterar nome, sair)

O app conversa com uma API REST em Node que roda local em http://127.0.0.1:3000 (`POST /api/login`, `GET /api/pedidos`, `GET /api/pedidos/:id`, `POST /api/pedidos/:id/cancelar`). Monta a validação funcional tela por tela e me diz o que foi validado.
