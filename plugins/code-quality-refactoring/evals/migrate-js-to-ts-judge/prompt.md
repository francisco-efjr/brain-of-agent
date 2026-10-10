---
name: migrate-js-to-ts-judge
description: "Mede o método de migração em massa: juiz validado primeiro, rulebook, piloto descartável, fila em disco, plano aprovado antes de converter e paridade por módulo, sem começar a converter nem instalar ferramentas sem pedido."
tags: [code-quality-refactoring, migration-parity, judge-first]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Propõe juiz (tsc e jest nos dois lados) provado contra quebra proposital, rulebook, piloto de 3 a 5 arquivos, fila em disco e paridade por módulo, pede aprovação do plano antes de migrar em massa e não instala nem converte nada."
model: sonnet
---
Quero migrar nosso backend de JavaScript para TypeScript. São 180 arquivos em `src/` (Express + Sequelize), somos 2 devs e eu queria que o Claude fizesse a conversão em massa hoje à tarde, enquanto eu toco outras coisas. Dá pra fazer?

Estrutura (resumida):

```text
src/
  routes/       (24 arquivos)
  controllers/  (31)
  services/     (46)
  models/       (22)
  middlewares/  (9)
  utils/        (38)
  index.js
__tests__/      (jest, 62% de cobertura no último relatório do CI)
package.json
```

`package.json` (trecho):

```json
{
  "scripts": { "start": "node src/index.js", "test": "jest", "lint": "eslint src" },
  "dependencies": { "express": "^4.19.2", "sequelize": "^6.37.3" },
  "devDependencies": { "jest": "^29.7.0", "eslint": "^8.57.0" }
}
```

Hoje não temos `tsconfig.json` nem nenhum arquivo `.ts`.
