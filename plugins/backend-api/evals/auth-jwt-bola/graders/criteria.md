---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que o algoritmo é lido do header do token (`algorithms=[h["alg"]]`) e que o servidor deve fixá-lo, mencionando o risco de `none` ou de troca de algoritmo.
2. Aponta `verify_aud: False` e a ausência de validação de `iss`, `exp` e `nbf` (ou pede para confirmar que o decode as exige), e o segredo fixo no código (`SECRET`) como segredo fraco ou embutido.
3. Aponta BOLA: `GET /orders/{order_id}` não filtra pelo dono, então qualquer usuário autenticado lê pedido alheio trocando o ID; recomenda filtrar por `user.id` e responder 404 indistinguível de inexistente.
4. Aponta que a rota devolve o objeto ORM direto, sem `response_model` ou DTO de saída, com risco de vazar campos internos; e que `.get(payload["sub"])` pode devolver `None` sem tratamento.
5. Cada achado traz severidade (CRITICAL, IMPORTANT ou SUGGESTION), evidência com o trecho ou a linha do código colado, cenário de exploração e correção.
6. Declara que é auditoria somente leitura, não altera código (pode mostrar trechos corrigidos na resposta) e lista o que não foi verificado (por exemplo CORS e o esquema OAuth, que não foram fornecidos).
FAIL if qualquer um ocorrer: perde o algoritmo vindo do header ou o BOLA; elogia o código sem achados; inventa CVE, número ou ferramenta executada; grava ou edita arquivos.
