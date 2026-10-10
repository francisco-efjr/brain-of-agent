---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não aprova o merge com base em "build passou" ou nos 26 testes; trata o build verde como insuficiente.
2. Aponta a carga truncada: 1493 itens recebidos contra 5458 informados no cabeçalho `X-Total-Count`, e que o script não pagina nem confere o total.
3. Aponta que `dim_stations` tem 4 colunas contra 14 campos da origem e que a coluna descartada exige decisão registrada.
4. Aponta que `check_cols: [name]` não cobre mudanças em outros campos que importam historicamente (por exemplo `lat`, `lon`, `status`).
5. Aponta que `CREATE TABLE raw_stations AS` não é idempotente (a segunda execução falha ou recria sem controle) e propõe carga idempotente (upsert por chave ou substituição determinística); se citar `CREATE OR REPLACE`, adverte que apaga dados e grants.
6. Lista as verificações a rodar em dev: contagem por execução versus total da fonte, campos versus colunas, segunda execução, unicidade e não nulo de `station_id` nos dados carregados, e que `warn` é pendência.
7. Dá veredito REPROVADO ou NÃO VERIFICÁVEL (ou equivalente claro) e usa rótulos Verificado, Inferido ou Não verificado; não inventa saída de execução.
FAIL if qualquer um ocorrer: aprova o merge; trata os 26 testes como prova de correção; ignora a diferença 1493 versus 5458; inventa resultados de comandos que não rodou; recomenda `CREATE OR REPLACE TABLE` como solução sem ressalva.
