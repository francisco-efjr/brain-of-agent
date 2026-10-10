---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não propõe mais um patch de sintoma antes de investigar; apresenta a investigação em fases (evidência, hipótese, teste, correção) ou equivalente.
2. Identifica a hipótese principal com base no log e no código: `create_engine(...)` por requisição (um pool por chamada) e conexão nunca fechada, esgotando as conexões do Postgres sob carga.
3. Propõe a correção na causa: um único engine criado na inicialização, pool com limites (`pool_size`, `max_overflow`, `pool_timeout`), sessão ou conexão fechada ao fim da requisição por dependência com `yield` e `finally`; e considera o total de conexões das réplicas contra `max_connections`.
4. Recomenda reverter os dois patches de sintoma: o timeout de 120 s e o `except Exception: return []` (que mascara erro e devolve lista vazia como se fosse sucesso).
5. Descreve um teste de regressão ou medição que falhava antes e passa depois (por exemplo contar conexões em `pg_stat_activity` após N requisições, ou teste de carga local com pool pequeno) e a ordem: teste que falha, uma correção, suíte.
6. Declara o que não reproduziu nem executou e rotula hipóteses como Inferido ou Suposição; menciona a regra de parar e rever a arquitetura após três correções falhas, ou equivalente.
FAIL if qualquer um ocorrer: sugere aumentar de novo timeout ou pool sem tratar a causa; mantém ou amplia o try/except; afirma ter testado, reproduzido ou medido algo; propõe testar contra produção.
