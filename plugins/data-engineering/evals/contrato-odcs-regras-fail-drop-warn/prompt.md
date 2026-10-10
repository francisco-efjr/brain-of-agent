---
name: contrato-odcs-regras-fail-drop-warn
description: "Mede se o plugin redige um rascunho de contrato de dados ODCS 3.2.0 sem inventar dono nem afirmar validade, define a ação fail, drop ou warn por regra com contagem de violações e quarentena, e propõe a política block, warn e log para o agente que consulta a tabela."
tags: [data-engineering, data-contracts-quality, data-contracts, data-quality]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega rascunho de contrato ODCS 3.2.0 com dono pendente, schema com chave e SLA de frescor, matriz de regras com fail para a chave, drop com quarentena para país inválido e warn com contagem para email e segmento, mapeamento para severity do dbt, política block warn log para o agente e nota de que o contrato não foi validado."
model: sonnet
---
Preciso do contrato de dados do dataset `analytics.customers` (domínio Vendas). Usamos dbt no BigQuery. Os campos:

- `customer_id` (string): chave; nunca pode ser nula nem repetida.
- `email` (string): falta em cerca de 8% dos registros, e isso é normal.
- `country` (string): código ISO de 2 letras; aparecem valores fora da lista de vez em quando.
- `signup_date` (date).
- `segment` (string): enriquecido por outro time, chega com atraso.

A tabela é atualizada de hora em hora e os consumidores aceitam até 2 horas de atraso. O dono é o time de CRM, mas não sei o nome da pessoa responsável. Quero as regras de qualidade dizendo o que deve parar a carga, o que deve descartar e o que só deve avisar, e também uma política para o agente de IA que vai consultar essa tabela.
