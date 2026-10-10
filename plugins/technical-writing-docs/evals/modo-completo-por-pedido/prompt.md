---
name: modo-completo-por-pedido
description: Mede se a keyword DOCS-COMPLETO escrita pelo usuário ativa a leitura integral das referências em lotes, a matriz de aplicabilidade por área e uma auditoria sem alterar nada, com registro honesto de lido, parcial ou ausente.
tags: [technical-writing-docs, playbook, full-mode]
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 1500
runs: 3
expected_outcome: "Ativa o modo completo, lê as referências do plugin em lotes e registra lido, parcial ou ausente, entrega matriz de aplicabilidade por área e achados com evidência e rótulos, não altera arquivos do projeto, marca como Não verificável o que depende do que não foi mostrado e lembra que ações externas continuam pedindo confirmação."
model: sonnet
---
DOCS-COMPLETO: audite a documentação do projeto descrito abaixo. É uma auditoria; não altere nada do projeto.

Projeto "Agendador" (API em Node/TypeScript para agendamento de consultas). Não estou com o repositório montado aqui; use esta descrição, que veio de uma inspeção minha:

- README com 18 linhas: nome, "npm install", "npm start" e licença. Sem exemplos de uso, sem pré-requisitos, sem link para outros documentos.
- Não existe pasta `docs/`, nem CHANGELOG, nem CONTRIBUTING.
- Duas ADRs em `adr/`: `0001-escolha-do-banco.md` e `0002-fila.md`, ambas com status "accepted". O `git log` mostra 3 edições na ADR 0002 depois de aceita.
- `CLAUDE.md` com 230 linhas, com árvore de diretórios, "boas práticas" genéricas e o comando `npm run build:all`; o `package.json` tem os scripts `dev`, `build`, `test` e `lint`.
- `openapi.yaml` com `openapi: 3.1` sem aspas, 14 operações, 11 delas sem `description`; `info.version` igual a "1.0".
- Não há `.vale.ini`, `.markdownlint*` nem verificador de links; o CI roda só testes.
- Diagrama em Mermaid no README antigo foi removido; sobrou um PNG de arquitetura de 2023.
- Os docstrings públicos existem em 30% das funções exportadas, sem exemplos.
