# Tabela por provedor: autenticação, prazo, reentrega e retenção

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Todas as células abaixo foram lidas na doc do provedor por um validador em 2026-10-10 (V-09, V-30, V-31, V-35, V-41, V-42, V-51), salvo onde marcadas **Inferido**, **Não verificado** ou **Não verificável**. Docs mudam: antes de implementar, abra a página vigente (URLs na última seção) e registre a data da leitura na ficha `checklist-webhook-provedor.md`. Nunca copie uma regra de um provedor para outro.

## Resumo comparativo

| Provedor | Autenticação | Prazo de resposta | Reentrega | Retenção / desativação | Duplicata e ordem |
|---|---|---|---|---|---|
| Stripe | `Stripe-Signature`; HMAC sobre o corpo bruto, biblioteca oficial; tolerância padrão de 5 min (nunca 0); comparação em tempo constante | Responder 2xx antes da lógica pesada (valor em segundos: Não verificado) | Qualquer resposta fora de 2xx é reentregue; reentrega automática por até 3 dias em produção | Reenvio manual até 15 dias no Dashboard e 30 dias na CLI | Ordem não garantida (não ordene por `created`); registre IDs de evento; par de eventos duplicados: `data.object.id` + `type` |
| Shopify | `X-Shopify-Hmac-Sha256` (HMAC do corpo; codificação base64: conhecimento estável, conferir na doc) | Prazo numérico: **Não verificado** (a página lida não traz) | Sem garantia de entrega | Reconciliação periódica por API recomendada | Duplicata por `X-Shopify-Webhook-Id`; sem garantia de ordem (`X-Shopify-Triggered-At` ou `updated_at`) |
| Mercado Pago | `x-signature` no formato `ts=...,v1=...`; segredo na configuração de webhooks (não expira; redefinir é recomendado, opcional). String assinada e algoritmo: **Não verificado** (use SDK oficial ou a doc vigente) | HTTP 200 ou 201 em até 22 s | Nova tentativa a cada 15 min; após a terceira, o prazo se estende por tempo não informado | Substituir notificações por consulta ativa "não é recomendado" | Idempotência não descrita; `GET /v1/orders/{id}` para obter o recurso depois da notificação |
| Asaas | Token estático no cabeçalho `asaas-access-token` (configurado no webhook; não é HMAC). Não usar a API Key como token | 200 depois de persistir; processar de forma assíncrona | Entrega at-least-once; após 15 falhas consecutivas a fila pode ser pausada | Eventos retidos por 14 dias e depois excluídos; até 10 webhooks por conta | Persistir o `id` do evento (restrição única); eventos por cobrança: não verificados |
| Pix (API do Banco Central) | Callback protegido por mTLS (detalhes no Manual de padrões, não lido); escopo OAuth2 `webhook.write` para configurar | Resposta esperada: 200; SLA definido por cada PSP | Política de reentrega: **Não verificável** (por PSP) | Expiração de cobrança e limites: não estão na especificação lida | Webhook só para Pix ligado a `txid`; avisa recebimento e devolução em estado final (`DEVOLVIDO`, `NAO_REALIZADO`) |
| Melhor Envio | `X-ME-Signature`: HMAC-SHA256 do corpo com o secret do aplicativo (codificação: **Não verificado**) | Timeout de 6 s | Nova tentativa após 15 min, até 5 tentativas; depois a notificação é **descartada** | Só dispara para etiquetas geradas pelo mesmo aplicativo | Idempotência sugerida: `data.id` + `event`; rastreio pode demorar até 1 dia útil após postagem |
| VTEX (Feed / Hook) | URL do Hook configurada com filtro; autenticação do chamador: não lida (**Não verificado**) | Hook: HTTP 200 em até 5.000 ms | Hook: novas tentativas com intervalo em progressão geométrica | Feed: itens lidos ficam ocultos por `visibilityTimeoutInSeconds`, voltam sem commit e somem após `messageRetentionPeriodInSeconds` (345.600 a 1.209.600 s). Hook removido após 3 dias sem notificações | `disableSingleFire=false` evita duplicatas; filtro `FromWorkflow` ou `FromOrders` (JSONata), não os dois |
| Nuvemshop | `x-linkedstore-hmac-sha256`: HMAC-SHA256 do corpo bruto com o segredo do app. URL HTTPS, sem localhost nem domínios da plataforma | 2xx em até 3 s | Reenvio imediato após timeout, depois cerca de 5, 10 e 15 min, depois fator 1,4 por 48 h; até 16 tentativas; 2xx encerra | Sem evento de estoque de produto | Ordem não garantida; duplicatas possíveis, idempotência é do desenvolvedor; dedupe por ID do pedido + status/evento: **Inferido** |
| WooCommerce | Assinatura do webhook: **Não verificado** | Não verificado | Política de reentrega: **Não verificado** | Status `active`, `paused`, `disabled` (desligado por falha de entrega) | Eventos de pedido `order.created`, `order.updated`, `order.deleted` |

Por que importa não generalizar: a doc da Stripe diz que fora de 2xx há reentrega; a regra "5xx/429 reenviam e os demais 4xx não" é do gateway de um fornecedor de terceiro (V-09). O prazo de 22 s do Mercado Pago, 6 s do Melhor Envio, 5 s da VTEX e 3 s da Nuvemshop são específicos de cada um.

## Notas por provedor

### Stripe (V-09, V-10)
- Use `stripe.webhooks.constructEvent` com o corpo bruto; rotação de segredo com janela de até 24 h; lista de IPs da Stripe como camada adicional; isentar a rota de CSRF; HTTPS com TLS 1.2+.
- A Stripe recomenda eventos **thin** em integrações novas (snapshot se terceiros exigirem o objeto completo); confirme qual formato o endpoint registrado recebe.
- Teste local: `stripe listen --forward-to localhost:<porta>/webhooks/stripe` e `stripe trigger <evento>` (documentado; instalar a CLI é decisão do usuário; use só chaves de teste).
- Idempotência de saída (V-10): todo POST aceita chave (UUID v4 ou string aleatória, até 255 caracteres, sem dado pessoal); a v1 salva status e corpo da primeira execução (inclusive 500); parâmetros diferentes com a mesma chave geram erro; chave pode ser removida após 24 h ou mais; a v2 conclui trabalho pendente em vez de repetir o que deu certo.

### Shopify (V-09)
- Verifique o HMAC sobre o corpo bruto com o segredo do app; trate `X-Shopify-Webhook-Id` como ID de dedupe; reconcilie por API periodicamente. Versão da API é trimestral: registre-a (por exemplo, `2026-07`) e confira a doc dessa versão.

### Mercado Pago (V-30)
- `x-request-id` aparece só nos exemplos de SDK. Trate o pedido como pendente até ler o recurso pela API depois da notificação. Responder 200/201 muito antes dos 22 s.
- Idempotência de requisição do Mercado Pago: **Não verificado**.

### Asaas (V-30)
- Compare o token do cabeçalho em tempo constante; grave o `id` do evento com restrição única; responda 200 depois de persistir; alerte antes da pausa de fila (15 falhas) e muito antes dos 14 dias de retenção.
- Combine o token estático com lista de IPs oficiais (a página cita uma página de IPs; **não lida**) e com reconciliação por API.
- Ambientes: sandbox `https://api-sandbox.asaas.com/v3`, produção `https://api.asaas.com/v3`; chave de produção no sandbox responde 401; a API usa o cabeçalho `access_token`. Separe URL e chave por variáveis de ambiente distintas.

### Pix (V-31; API Pix 2.10.0 do Banco Central, Apache-2.0)
- API exposta pelo PSP recebedor; erros seguem a RFC 7807 (`type` identifica o erro); mudanças compatíveis (campos e valores novos de enumeração) podem ocorrer a qualquer momento: ignore o que não conhece.
- `txid`: `[a-zA-Z0-9]{26,35}`; endpoints `cob` e `cobv`; escopos como `cob.write`, `cob.read`, `webhook.write`.
- Dados de teste do brain-of-agent (MIT, **Inferido**: não reverificados): `EndToEndId` tem 32 caracteres (`E` + ISPB de 8 dígitos + `AAAAMMDDHHmm` em UTC + 11 alfanuméricos) e serve para conciliação do lado do pagador; `txid` é do recebedor. Se a resposta não chega em 30 s, consulte o status pelo `EndToEndId` antes de qualquer reenvio. Limites noturnos e prazo do MED: confirme no regulamento vigente.

### Melhor Envio (V-35)
- Verifique `X-ME-Signature` sobre o corpo bruto; responda em menos de 6 s; deduplique por `data.id` + `event`; faça busca ativa porque a notificação é descartada após 5 tentativas.
- Eventos: `order.created`, `order.pending`, `order.released`, `order.generated`, `order.received`, `order.posted`, `order.delivered`, `order.cancelled`, `order.undelivered`, `order.paused`, `order.suspended`.
- Sandbox: o status muda sozinho a cada 15 minutos.

### VTEX (V-42)
- Receba o evento, busque o pedido atual pela API (não confie no corpo), faça `commit` só depois de persistir, tolere duplicatas e ordem, monitore o sumiço da configuração por inatividade e reconcilie por busca. Catalog, Checkout e OMS da VTEX não foram lidos.

### Nuvemshop (V-51)
- Corpos idênticos contam como a mesma mensagem; variação só no contador de tentativas conta como duplicata. Domínio da doc é GitHub Pages; há indicação de migração para `nuvemshop.dev`: confira a URL.
- Como não há evento de estoque, reconcilie o estoque por API (**Inferido**).

### WooCommerce (V-41)
- Integre com a chave de menor permissão (leitura quando possível), sempre em HTTPS, nunca com `consumer_key`/`consumer_secret` na query string (aparece em log e histórico). Paginação padrão de 10 itens: use `per_page` e leia `X-WP-Total`/`X-WP-TotalPages`. Trate o webhook como aviso e monitore o status `disabled`. Assinatura, reentrega e HPOS: Não verificado; diga isso ao gerar código.

## URLs de conferência (abra a versão vigente)

- Stripe: https://docs.stripe.com/webhooks · https://docs.stripe.com/api/idempotent_requests
- Shopify: https://shopify.dev/docs/apps/build/webhooks
- Mercado Pago: https://www.mercadopago.com.br/developers/pt/docs/checkout-api-orders/notifications
- Asaas: https://docs.asaas.com/docs/sobre-os-webhooks · https://docs.asaas.com/reference/comece-por-aqui
- Pix (Banco Central): https://raw.githubusercontent.com/bacen/pix-api/master/openapi.yaml
- Melhor Envio: https://docs.melhorenvio.com.br/docs/webhooks.md
- VTEX: https://developers.vtex.com/docs/guides/orders-feed
- Nuvemshop: https://tiendanube.github.io/api-documentation/resources/webhook
- WooCommerce: https://developer.woocommerce.com/docs/apis/rest-api/
