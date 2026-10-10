---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Recomenda paginação por cursor (token opaco) para um conjunto grande e mutável, explicando que offset sofre com linhas que entram ou saem durante a paginação, e define limite máximo de página e filtro `status` com valores permitidos.
2. Define o modelo de erro conforme RFC 9457 (`application/problem+json`) com `type`, `title`, `status`, `detail` e `instance`, mais extensão por campo para erros de validação; apresenta exemplo de resposta para status inválido. Se mencionar a RFC 7807, diz que a RFC 9457 a obsoleta.
3. Trata a duplicidade de `POST /orders` com `Idempotency-Key`, definindo escopo da chave, retenção e resposta repetida, e descreve o cabeçalho como convenção amplamente usada e não como padrão publicado.
4. Descreve evolução sem quebra: mudanças aditivas, política de versionamento e depreciação; menciona autorização por objeto (um cliente só vê os próprios pedidos) ou a trata como pergunta aberta.
5. Se citar lint de OpenAPI ou mock, deixa a execução para o usuário e não instala nem executa nada.
FAIL if qualquer um ocorrer: recomenda offset como solução principal sem ressalva; apresenta a RFC 7807 como padrão vigente; apresenta Idempotency-Key como RFC aprovada; instala ou executa pacotes (npx, npm, pip); omite o tratamento do POST duplicado.
