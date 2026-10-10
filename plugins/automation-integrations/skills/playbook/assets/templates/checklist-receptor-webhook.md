# Checklist de receptor de webhook

Provedor: [NOME] · Handler: [CAMINHO] · Revisão: [commit/data] · Fonte do checklist: V-18 (Stripe, GitHub, Hookdeck). Prazos de retry e tolerâncias são **do provedor**: preencha a coluna "Valor do provedor" com a documentação dele ou `NV`.

| ID | Item | Status (ok/falha/NA/NV) | Evidência (`arquivo:linha`, teste, saída) | Valor do provedor |
| --- | --- | --- | --- | --- |
| W-01 | Corpo bruto preservado até a verificação (nenhum parser reencodou) | | | |
| W-02 | Assinatura HMAC SHA-256 verificada, tempo constante, tolerância de timestamp em minutos (nunca 0), esquemas desconhecidos ignorados | | | cabeçalho: · tolerância: |
| W-03 | ID do evento com restrição de unicidade gravado antes do efeito (nunca `created`) | | | campo do ID: |
| W-04 | 2xx antes do trabalho pesado | | | prazo de resposta: |
| W-05 | Fila com retry, backoff e fila de mortas; reprocesso idempotente | | | política de retry: |
| W-06 | Evento parcial → buscar objeto atual na API | | | |
| W-07 | Sem dependência de ordem | | | ordem garantida? |
| W-08 | Log: ID, resultado da assinatura, código; sem segredo/payload completo | | | |
| W-09 | Rotação de segredo registrada | | | segredos simultâneos: |
| W-10 | Segredo em variável de ambiente | | | |
| W-11 | Só os tipos de evento necessários; tipo desconhecido → 2xx + log | | | |
| Extra | HTTPS com TLS 1.2+ | | | |
| Extra | Allowlist de IP **além** da assinatura | | | origem dos IPs: |
| Extra | Rota fora da proteção CSRF | | | |
| Extra | Dedupe e enfileiramento na mesma transação (outbox) | | | |

## Testes de replay executados (cole a saída)

| Caso | Esperado | Resultado real |
| --- | --- | --- |
| Assinatura inválida | 4xx; nenhum registro | |
| Timestamp de 10 min atrás | 4xx | |
| Mesmo `event_id` 2× | 2xx; 1 efeito | |
| Corpo com espaços/ordem diferente (assinatura sobre bytes originais) | 2xx | |
| Falha ao gravar/enfileirar | 5xx; evento não marcado como visto | |
| Worker com destino 503 | backoff → fila de mortas com causa | |

Sem execução: marque `NV` e descreva o roteiro. Fonte: V-18; Verificado em 2026-10-10.
