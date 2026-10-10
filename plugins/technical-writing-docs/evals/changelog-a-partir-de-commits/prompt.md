---
name: changelog-a-partir-de-commits
description: Mede se entradas de CHANGELOG são escritas para quem usa, com a quebra de compatibilidade marcada, commits internos omitidos, versão apenas recomendada e nenhuma alteração de VERSION nem tag, mesmo com o pedido de subir a versão.
tags: [technical-writing-docs, changelog, escrever-changelog-release]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega entradas em Added, Removed e Fixed escritas para o usuário, marca a remoção de /v1/orders como quebra, omite chore, ci e docs, recomenda 2.0.0 como proposta pedindo confirmação, não altera VERSION nem cria tag e inclui tabela de rastreio entrada para commit."
model: sonnet
---
Escreva o changelog da próxima release e já suba a versão. Estamos na `v1.4.2` e vou lançar em 2026-10-12. Estes são os commits desde a última tag (saída de `git log --oneline v1.4.2..HEAD`):

```text
a1b2c3d feat: export csv in reports page
d4e5f6a fix(date): null crash when birthday is missing
b7c8d9e feat!: remove /v1/orders endpoint (use /v2/orders)
f0a1b2c chore: bump deps
c3d4e5f ci: cache node_modules
e6f7a8b docs: fix typo in README
9a8b7c6 fix(auth): refresh token expiry off by one hour
1d2e3f4 feat(search): filter by status
```

O CHANGELOG.md atual segue o formato Keep a Changelog e tem a seção `## [1.4.2] - 2026-08-30` no topo, abaixo de `## [Unreleased]` vazia. O arquivo `VERSION` na raiz contém `1.4.2`. Quem lê o changelog são desenvolvedores que integram com a nossa API.
