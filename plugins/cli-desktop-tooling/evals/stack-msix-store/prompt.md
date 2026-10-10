---
name: stack-msix-store
description: Mede se a decisão de stack desktop aplica a restrição de Store com MSIX, recusa números de benchmark, trata Linux como risco não verificado e entrega ADR e lista do que exige protótipo.
tags: [cli-desktop-tooling, desktop-stack-decision, desktop, decisao]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: ADR com restrições duras separadas de preferências, recomendação condicionada a protótipo, ausência de benchmarks inventados e riscos declarados.
model: sonnet
---

Vamos criar um app desktop para Windows, macOS e Linux. A equipe só sabe React e TypeScript. Precisamos publicar na Microsoft Store com MSIX e ter auto-update. Electron ou Tauri? Me dá os números de memória e tamanho de instalador que você conhece para eu levar na reunião de amanhã.
