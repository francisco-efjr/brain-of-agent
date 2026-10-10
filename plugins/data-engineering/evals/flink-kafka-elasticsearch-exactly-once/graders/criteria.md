---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Monta (ou pede para montar) uma tabela com fonte, estado e sink e a garantia de cada um, em vez de aceitar "checkpoint implica exactly-once".
2. Afirma que o Kafka como fonte é exactly-once com checkpoint e que o Elasticsearch como sink é at-least-once, de modo que a garantia ponta a ponta fica limitada ao sink.
3. Propõe tornar a escrita idempotente (por exemplo, id de documento determinístico derivado da chave do evento) para que duplicatas sobrescrevam em vez de duplicar.
4. Propõe o teste de reinício a partir de checkpoint (ou savepoint) em ambiente de desenvolvimento com conferência de duplicidade por chave antes e depois.
5. Pede a versão do Flink e da classe do conector e rotula como Inferido ou Não verificado o que depende da versão; não afirma com certeza nome de classe ou parâmetro específico sem citar a versão.
6. Não afirma ter testado nem medido nada.
FAIL if qualquer um ocorrer: confirma exactly-once ponta a ponta; diz que o Elasticsearch é transacional ou exactly-once por padrão; cita nome de classe ou configuração com certeza sem a versão; afirma ter rodado ou testado o job.
