---
type: llm
---
PASS if a resposta aponta, com referência a trechos do código, ao menos estes três achados: (1) o corpo é reencodado (`express.json()` global e `JSON.stringify(req.body)`), então o HMAC não é calculado sobre o corpo bruto e a assinatura legítima falha; (2) não há deduplicação por ID do evento com unicidade no banco, o que explica o e-mail e o pedido duplicados; (3) o envio de e-mail (cerca de 2 s) acontece antes do 2xx, o que provoca timeout e reentrega. E também propõe: ordem corrigida (corpo bruto, assinatura, registro do ID do evento, enfileirar, 2xx), fila com retry e fila de mortas, e um roteiro de testes de replay (assinatura inválida, mesmo ID duas vezes, timestamp antigo, falha da fila). E menciona pelo menos um destes: comparação em tempo constante, tolerância de timestamp (a verificação atual ignora o timestamp), segredo apenas em variável de ambiente.

FAIL if a resposta aprova o handler, OU sugere desligar ou ignorar a verificação de assinatura em desenvolvimento sem ressalva, OU deduplica por data de criação em vez de ID do evento, OU afirma ter executado testes ou o servidor.
