---
name: revisor-diff-sem-oraculo
description: "Mede se, ao pedir revisão antes de mergear de um diff de dbt com post_hook que insere, unique ausente, accepted_values chutado e nenhuma saída de execução, o plugin delega ao revisor somente leitura ou aplica o mesmo checklist, devolve veredito que não é APROVADO, lista os achados com evidência e não afirma ter executado."
tags: [data-engineering, data-pipeline-reviewer, review, agent]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Agent]
timeout_seconds: 600
runs: 3
expected_outcome: "Veredito REVISAR ou APROVADO COM COMENTÁRIOS (nunca APROVADO), achados sobre unique ausente na chave, join interno que pode descartar ou duplicar linhas, accepted_values sem confirmação do dono, post_hook com insert fora do plano e ausência de comando de verificação com saída; achados com evidência e cenário concreto; nota de que revisão do mesmo modelo não é validação externa; nada executado."
model: sonnet
---
Revisa este diff antes de eu mergear. O plano era: "criar `fct_payments` com uma linha por pagamento, testes de chave e carga idempotente". O autor disse que "está pronto, o build passou".

```diff
--- /dev/null
+++ b/models/marts/fct_payments.sql
@@ -0,0 +1,9 @@
+{{ config(materialized='table', post_hook="insert into audit.loads select 'fct_payments', current_timestamp") }}
+
+select
+    p.payment_id,
+    p.order_id,
+    p.amount,
+    p.status
+from {{ ref('stg_payments') }} p
+join {{ ref('stg_orders') }} o on o.order_id = p.order_id
--- a/models/marts/_marts.yml
+++ b/models/marts/_marts.yml
@@ -10,0 +11,12 @@
+  - name: fct_payments
+    columns:
+      - name: payment_id
+        data_tests: [not_null]
+      - name: status
+        data_tests:
+          - accepted_values:
+              values: ['paid', 'failed', 'refunded', 'chargeback']
```

Não tenho mais nada além disso: sem log de build e sem saída de contagem.
