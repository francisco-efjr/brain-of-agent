---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. A decisão é híbrida e coerente com o contexto: pool (tabela compartilhada com `tenant_id`) com RLS como segunda barreira para a maioria dos clientes, e silo (banco ou deployment dedicado) para os 3 clientes com exigência contratual de separação; diz que "dados separados" por contrato precisa ser conferido no texto do contrato (o que exatamente é separação exigida), tratando isso como Suposição ou pendência.
2. Diz que tabela por tenant e coluna por tenant são antipadrões e não são recomendadas.
3. Lista schema por tenant como opção com prós e contras, rotulando os contras e prós vindos de discussões de praticantes como "relato de praticante" (e não como norma): por exemplo apagar e restaurar por tenant e índices menores de um lado; custo de migração em muitos schemas, extensões, limite de locks e memória do outro; considera o tamanho do time (4 pessoas) e 5.000 tenants na avaliação.
4. Inclui o mapa tenant para deployment e como a requisição é mapeada para o tenant (a partir de credencial validada, não de parâmetro livre), migração de schema automatizada com versão registrada por tenant, e critérios para mudar de modelo (por exemplo, quando um novo cliente exigir silo) com plano de migração entre modelos.
5. Trata o maior cliente (cerca de 30 vezes o mediano) com noisy neighbor: rate limit por tenant e plano, métricas por tenant, ou silo/shard dedicado como opção; sem inventar números de capacidade ou custo (estimativas só com premissa declarada e rotuladas Suposição).
6. O ADR tem status coerente com o pedido (proposto, com decisor Rafael, ou rascunho), usa rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável) e não cita fonte, estudo ou número inexistente.
FAIL if qualquer um ocorrer: recomenda tabela ou coluna por tenant; recomenda schema por tenant para 5.000 tenants sem discutir o custo de migração; ignora os 3 clientes com exigência contratual; apresenta relato de fórum como fato verificado; inventa números de custo, desempenho ou fontes; decide em nome do Rafael (marca como aprovado); omite os rótulos epistêmicos.
