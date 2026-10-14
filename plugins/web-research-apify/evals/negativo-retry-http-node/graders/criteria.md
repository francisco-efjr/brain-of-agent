---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Resposta técnica direta e correta para Node 22 com `fetch` nativo: backoff exponencial com jitter, respeito ao cabeçalho `Retry-After` (em segundos ou como data HTTP) quando presente, limite máximo de tentativas e de espera, e tratamento de 429 (e de 503 ou outros 5xx transitórios).
2. Diz que o retry vale para métodos idempotentes (GET, PUT, DELETE, HEAD) ou exige chave de idempotência para os demais, e que erros 4xx que não sejam 429 (ou 408) não devem ser repetidos.
3. Traz um exemplo curto de código JavaScript (função com `fetch`, `AbortSignal.timeout` ou equivalente) e é proporcional à pergunta, sem relatório extenso.
4. Não trata o pedido como pesquisa na web, não menciona Apify, Actors, orçamento ou scraping.
FAIL if qualquer um ocorrer: aciona qualquer skill ou agente do plugin; propõe usar o Apify; retry sem limite de tentativas; ignora `Retry-After`; repete métodos não idempotentes sem ressalva.
