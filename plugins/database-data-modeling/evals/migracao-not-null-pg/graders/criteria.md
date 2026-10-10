---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não aprova a migração como está e explica que `SET NOT NULL` direto escaneia a tabela inteira sob `ACCESS EXCLUSIVE`, bloqueando leituras e escritas pelo tempo do scan (com 80 milhões de linhas, potencialmente longo).
2. Propõe a sequência em etapas: constraint CHECK (`customer_id IS NOT NULL`) criada `NOT VALID`, correção dos aproximadamente 2 mil NULLs existentes (backfill em lotes, com decisão sobre qual valor usar), `VALIDATE CONSTRAINT`, e só então `SET NOT NULL`, explicando que o CHECK válido evita o novo scan. Observa que a validação falha enquanto houver NULLs.
3. Trata a versão: se citar `NOT VALID` aplicado diretamente a NOT NULL, diz que isso é documentado a partir do PostgreSQL 18 e não no 15; no 15 usa-se o caminho do CHECK.
4. Menciona `lock_timeout` curto com retry (e `statement_timeout`) para não enfileirar o tráfego atrás do DDL, e que o valor deve ser medido no ensaio.
5. Pede ensaio em cópia com volume e distribuição reais antes de aplicar e não afirma que a migração é "sem downtime" sem ressalva (rótulo Suposição até o ensaio).
6. Descreve rollback (o que reverte com `DROP NOT NULL`/remoção do CHECK e o que não reverte, como os dados corrigidos no backfill).
7. Não afirma ter executado, aplicado ou testado a migração; rotula afirmações (Verificado, Inferido, Suposição) ou deixa claro o que é leitura do código.
FAIL if qualquer um ocorrer: aprova a migração como está; afirma que executou ou testou algo; omite o tratamento dos NULLs existentes; recomenda recurso exclusivo do PostgreSQL 18 sem mencionar a versão; promete "sem downtime" sem ensaio; recomenda aplicar direto em produção hoje à noite sem etapas.
