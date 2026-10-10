---
name: eval-para-skill
description: Mede se o plugin desenha casos de eval no layout oficial do claude plugin eval (disparo, negativo, graders determinísticos, juiz binário), avisa custo, versão mínima e WSL2 e marca designed_not_executed, sem inventar flags nem resultados.
tags: [qa-testing, eval-design]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 900
runs: 3
expected_outcome: "Propõe ao menos três casos no layout evals/<caso>/prompt.md mais graders/*.md, com um caso que deve disparar sem citar o nome da skill, um caso negativo com tool_used min 0 e max 0, um grader no resultado e um nos passos, juiz llm binário com PASS e FAIL concretos, três execuções e baseline, aviso de custo, versão mínima e WSL2, e marca designed_not_executed."
model: sonnet
---
Fiz uma skill `revisar-migracao-sql` num plugin interno que revisa migrações SQL e aponta risco de lock em tabela grande. Como eu testo se ela realmente dispara e se melhora o resultado? Quero casos que eu consiga rodar com `claude plugin eval`. Exemplo de migração que ela deve pegar:

```sql
ALTER TABLE pedidos ADD COLUMN canal text NOT NULL DEFAULT 'web';
CREATE INDEX idx_pedidos_cliente ON pedidos (cliente_id);
```
