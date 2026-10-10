---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Pede o plano (`EXPLAIN` ou a UI de SQL do Spark) antes de mexer em configuração, em vez de sugerir parâmetros às cegas.
2. Explicita o tipo de join (`how=`) e aponta que, se `customer_id` não for único em `customers`, o join multiplica linhas de `orders`; pede para auditar unicidade da chave.
3. Aponta `mode("append")` sem idempotência como outra causa de duplicação em reexecução ou retry e propõe escrita idempotente (merge por chave com critério explícito, ou substituição determinística da partição ou do intervalo).
4. Troca a UDF Python por funções nativas (`F.upper(F.trim(...))` ou equivalente) e explica o motivo (otimizador e serialização).
5. Aponta `collect()` em volume (traz tudo ao driver e recomputa) e propõe `limit` ou `show` se a intenção for inspeção.
6. Propõe auditar unicidade e nulos da chave primária depois da escrita.
7. Ao citar defaults ou comportamentos, liga-os à versão (Spark 3.5 informada) ou rotula como Inferido; não inventa valores numéricos de configuração sem versão.
8. Não afirma ter medido ganho de desempenho nem ter executado o job.
FAIL if qualquer um ocorrer: entrega valores de configuração sem citar versão; afirma que `printSchema` executa um job; mantém `append` cego; mantém a UDF sem justificar; afirma ganho medido ou execução que não houve.
