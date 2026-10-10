---
name: precedencia-sistema-vs-taste
description: "Caso de precedência de estilo: o usuário quer uma tela de Ajustes mais premium e minimalista e descreve um design system próprio (fonte do sistema, ícones Lucide, acento, raios e sombras por token). Mede se o assistente mantém o design system como autoridade, não troca fonte, ícones ou cores por sugestão das skills taste, propõe mudanças de hierarquia, espaçamento e agrupamento por token e declara a precedência."
tags: [design-engineering-kit, precedence, design-system, taste, redesign]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 420
runs: 3
expected_outcome: "Mantém fonte do sistema, ícones Lucide, acento, raios e sombras, propõe recomposição de hierarquia, agrupamento, ritmo de espaçamento e estados citando tokens por nome, declara que o design system vence as direções taste, rotula como suposição o que não viu e não escreve código nem arquivos."
model: sonnet
---
Quero deixar a tela de Ajustes do nosso app web (React) com cara mais premium e minimalista, tipo Linear ou Notion. Hoje ela parece um formulário padrão. Não tenho o projeto aberto aqui; vou descrever.

Nosso design system (já é o oficial do produto, não quero largar): fonte do sistema (`-apple-system`, sem webfont), ícones Lucide com traço de 1,6 px, acento `--accent: #C2456E` com `--on-accent: #FFFFFF`, cartões com `--radius-card: 12px` e sombra `--shadow-card`, espaçamento em grade de 4 px (`--space-1` a `--space-10`), texto secundário em `--label-secondary`.

A tela tem 4 seções (Conta, Notificações, Aparência, Privacidade), cada uma com 4 a 8 campos em uma coluna única dentro de um cartão grande. O que você mudaria? Quero a proposta, não o código.
