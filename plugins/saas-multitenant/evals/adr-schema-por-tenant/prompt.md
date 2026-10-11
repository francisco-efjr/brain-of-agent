---
name: adr-schema-por-tenant
description: Mede se o plugin conduz a decisão de modelo de tenancy com contexto real (200 clientes hoje, 5.000 em 3 anos, 3 com exigência contratual de dados separados) e entrega ADR híbrido, com pool e RLS como padrão e silo para os 3, sem tabela por tenant, com schema por tenant como opção rotulada de relato de praticante, mapa tenant para deployment, migração automatizada e critérios de mudança.
tags: [saas-multitenant, tenancy-model-adr, adr, architecture]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega ADR com decisão híbrida (pool com RLS e silo para os 3 clientes com exigência contratual), nunca tabela ou coluna por tenant, schema por tenant listado com trade-offs rotulados como relato de praticante, mapa tenant para deployment, migração automatizada com versão por tenant, critérios de mudança de modelo e rótulos epistêmicos, sem fonte inventada."
model: sonnet
---
Estamos começando a escalar o nosso SaaS B2B de gestão de obras (PostgreSQL, equipe de 4 desenvolvedores). Hoje são 200 clientes e a projeção é de 5.000 em 3 anos; o maior cliente tem cerca de 30 vezes o volume do cliente mediano. Três clientes enterprise já assinaram contrato exigindo que os dados fiquem separados dos demais; os outros não exigem nada. Hoje tudo está numa tabela compartilhada com `tenant_id`, sem RLS.

Estou em dúvida entre schema por tenant, banco por tenant ou continuar na tabela compartilhada. Preciso do ADR dessa decisão para apresentar ao CTO (o Rafael decide). Entregue o texto do ADR na resposta, sem gravar arquivos.
