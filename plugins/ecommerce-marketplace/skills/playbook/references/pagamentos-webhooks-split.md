# Pagamentos, webhooks, idempotência, Pix e split

Base das skills `webhook-pagamento` e `marketplace-split` e do agente `auditor-pagamentos-integracoes`. O plugin trata o **recorte de loja/marketplace**: "o pedido pode ser liberado?" fica aqui; "o dinheiro fechou com o extrato do adquirente?" (ledger, conciliação, chargeback em profundidade, Pix como PSP, regulação do Banco Central, PCI de quem processa cartão) vai para `/fintech-payments:playbook`.

Modelo-alvo: Claude 4.x/5.x · pesquisa validada em 2026-10-10 · compilado em 2026-10-11. Prazos, cabeçalhos e limites mudam por provedor e por versão da API: confira a página do provedor (coluna Fonte) antes de codificar. Nunca crie cobrança, conta conectada, reembolso ou repasse reais; use sandbox e dados sintéticos.

## Sumário

- [1. Checklist de 10 itens para webhook](#1-checklist-de-10-itens-para-webhook)
- [2. Tabela por provedor](#2-tabela-por-provedor)
- [3. Idempotência de requisição](#3-idempotência-de-requisição)
- [4. Criação segura de pedido e retenção por divergência](#4-criação-segura-de-pedido-e-retenção-por-divergência)
- [5. Pix](#5-pix) · [6. Boleto e cartão](#6-boleto-e-cartão)
- [7. Marketplace: cobrança, KYC, split e canais](#7-marketplace-cobrança-kyc-split-e-canais)
- [8. Riscos de pagamento e casos de teste (brain)](#8-riscos-de-pagamento-e-casos-de-teste-brain)
- [9. Testes que provam o handler](#9-testes-que-provam-o-handler)

## 1. Checklist de 10 itens para webhook

Fonte: V-09 (Stripe, Shopify, exemplo Hookdeck), com acréscimos de V-30. Cada item vale para o provedor da tabela da seção 2, que prevalece sobre qualquer regra geral.

1. **Assinatura sobre o corpo bruto antes de parsear.** Middleware que reescreve o corpo (`express.json()` global) invalida a assinatura.
2. **Tempo constante** na comparação; assinatura de formato inválido é falha limpa (400/401), não exceção. Compare bytes: o exemplo Python do Hookdeck levanta `TypeError` com cabeçalho não ASCII.
3. **Recência:** rejeitar timestamp fora da tolerância (Stripe: padrão de 5 minutos, nunca 0).
4. **`event_id` único no banco;** duplicata responde 2xx sem reprocessar. A restrição cobre duas entregas simultâneas. Para pares de eventos duplicados, a Stripe sugere `data.object.id` + `type`.
5. **2xx rápido** (regra do plugin: < 5 s) e processamento em **fila**.
6. **Sem dependência de ordem:** não use o campo `created` para ordenar; busque o estado atual na API do provedor antes de agir.
7. **Pedido só após evento verificado;** valor ou moeda divergentes do carrinho ⇒ retido para revisão humana (seção 4).
8. **Reconciliação periódica por API:** a entrega não é garantida.
9. **Rotação de segredo** com janela de sobreposição (Stripe: até 24 h); segredos distintos para teste e produção, por variável de ambiente.
10. **Teste local** com o encaminhador oficial do provedor e dados sintéticos (T-03 de [ferramentas-e-mcp.md](ferramentas-e-mcp.md)).

Isente a rota do webhook de CSRF (a assinatura é a defesa), use HTTPS com TLS 1.2+ e, quando o provedor publicar lista de IPs, combine IPs **e** assinatura (Stripe).

## 2. Tabela por provedor

Leitura em 2026-10-10 pelo validador. Célula vazia ou "Não verificado" = a fonte lida não diz. Copie para [checklist-webhook-provedor.md](../assets/templates/checklist-webhook-provedor.md) e preencha para o provedor do projeto.

| Provedor | Autenticação | Prazo de resposta | Reentrega | Retenção / descarte | Dedupe / idempotência | Fonte |
| --- | --- | --- | --- | --- | --- | --- |
| **Stripe** | `Stripe-Signature` (HMAC) sobre corpo bruto; biblioteca oficial; IPs publicados | 2xx antes da lógica pesada; prazo numérico não lido | Qualquer não-2xx é reentregue; automática por até 3 dias em produção | Reenvio manual até 15 dias (Dashboard) e 30 dias (CLI) | ID do evento; `data.object.id` + `type` em pares duplicados; eventos *thin* recomendados em integrações novas | V-09 · docs.stripe.com/webhooks |
| **Shopify** | `X-Shopify-Hmac-Sha256` | "200 em 5 s" **Não verificado** (vem de SKILL de terceiros sem fonte) | Não verificado | Não verificado | `X-Shopify-Webhook-Id`; ordem por `X-Shopify-Triggered-At` ou `updated_at`; sem garantia de entrega nem de ordem; reconciliar por API | V-09 · shopify.dev/docs/apps/build/webhooks |
| **Mercado Pago** | `x-signature` no formato `ts=...,v1=...` (HMAC; usar SDK oficial ou a doc vigente; algoritmo e string assinada **não estão na página lida**); segredo na configuração de webhooks, não expira | **HTTP 200 ou 201 em até 22 s** | Nova tentativa a cada **15 min**; após a 3ª, prazo estendido por tempo não informado | Não informado | Idempotência **não verificada**; tratar o pedido como pendente até `GET /v1/orders/{id}` (usar o GET como substituto de notificações "não é recomendado") | V-30 · mercadopago.com.br/developers/pt/docs/checkout-api-orders/notifications |
| **Asaas** | **Token estático** no cabeçalho `asaas-access-token` (não é HMAC do corpo); **não usar a API Key como token**; cabeçalho `access_token` para a API | Responder 200 **depois de persistir** e processar de forma assíncrona | *At least once*; após **15 falhas consecutivas** a fila pode ser pausada | Eventos retidos por **14 dias**, depois excluídos; até 10 webhooks por conta | Persistir o `id` do evento; sandbox `https://api-sandbox.asaas.com/v3`, produção `https://api.asaas.com/v3` (chave de produção no sandbox responde 401) | V-30 · docs.asaas.com/docs/sobre-os-webhooks |
| **Melhor Envio** | `X-ME-Signature`: HMAC-SHA256 do corpo com o secret do aplicativo | Timeout de **6 s** | Nova tentativa após 15 min, até **5 tentativas**, depois **descartada** | Descarte após 5 | Idempotência por `data.id` + `event` (regra do plugin); só dispara para etiquetas geradas pelo mesmo aplicativo; reconciliar por busca ativa; rastreio pode demorar até 1 dia útil após a postagem; sandbox muda status a cada 15 min | V-35 · docs.melhorenvio.com.br/docs/webhooks.md |
| **VTEX (Hook)** | Não lido | **HTTP 200 em até 5.000 ms** | Falhas geram novas tentativas com intervalo em progressão geométrica | Hook removido após **3 dias** sem notificações | `disableSingleFire: false` evita duplicados; filtro `FromWorkflow` (padrão) ou `FromOrders` (JSONata), sem combinar | V-42 · developers.vtex.com/docs/guides/orders-feed |
| **VTEX (Feed)** | Polling pela API | n/a | Item lido fica oculto por `visibilityTimeoutInSeconds` e volta sem *commit* | Descartado após `messageRetentionPeriodInSeconds` (345.600 a 1.209.600 s); configuração some sem eventos no período | *Commit* só depois de persistir | V-42 |
| **Nuvemshop** | `x-linkedstore-hmac-sha256`: HMAC-SHA256 do corpo bruto com o segredo do app; URL HTTPS sem localhost nem domínios da plataforma | 2xx em até **3 s** | Imediata após o timeout, depois ~5/10/15 min, depois fator 1,4 por 48 h; até **16 tentativas**; 2xx encerra | Não informado | Ordem não garantida; duplicatas possíveis (idempotência é sua); dedupe por ID do pedido + status/evento (**Inferido**); **sem evento de saldo de estoque** ⇒ reconciliar estoque por API (**Inferido**) | V-51 · tiendanube.github.io/api-documentation/resources/webhook (domínio em migração para nuvemshop.dev: confira) |
| **Pix (BCB)** | Callback do PSP protegido por **mTLS** (detalhes no Manual de padrões, não lido) | Resposta esperada 200; SLA definido por cada PSP | Política de reentrega **não está na especificação lida** | Não informado | Só notifica Pix associados a `txid`; dispara no recebimento e quando a devolução chega a estado final (`DEVOLVIDO` ou `NAO_REALIZADO`) | V-31 · raw.githubusercontent.com/bacen/pix-api/master/openapi.yaml (versão 2.10.0) |
| **WooCommerce** | Assinatura **não verificada**; Basic Auth com consumer key/secret na API REST, em HTTPS | Não verificado | Não verificado | Status do webhook: `active`, `paused`, `disabled` (desligado por falha de entrega) | Eventos de pedido `order.created`, `order.updated`, `order.deleted`; tratar como aviso e reconciliar | V-41 · developer.woocommerce.com/docs/apis/rest-api/ |
| **Mercado Livre** | A ler na documentação | A descobrir | A descobrir | Notificações são a única forma de conhecer alguns eventos; tópicos `orders_v2`, `messages`, `items`, `questions`, `stock-location`, `user_products` | A descobrir | V-36 |
| **Amazon SP-API** | A ler | A descobrir | A descobrir | Notifications API v1 com Amazon EventBridge (`createDestination`/`getDestinations`) | A descobrir | V-36 |

Regra: o que a tabela marca como Não verificado fica assim até leitura da documentação; não complete de memória.

## 3. Idempotência de requisição

Fontes: V-10 (Stripe, `docs.stripe.com/api/idempotent_requests`; Fowler, *Idempotent Receiver*).

- Todo POST aceita chave; GET/DELETE não. Chave: UUID v4 ou string aleatória, até 255 caracteres, sem dado pessoal.
- A v1 da Stripe salva status e corpo da **primeira** execução (inclusive 500) e devolve nas retentativas; parâmetros diferentes com a mesma chave geram erro; falha de validação ou conflito concorrente não salva resultado; a chave pode ser removida após ≥ 24 h; a v2 conclui trabalho pendente em vez de repetir o que deu certo. Confira se o provedor usa v1 ou v2.
- Fowler: ID único por cliente e número da requisição; o servidor devolve a resposta salva. A página não trata de limpeza nem de duplicatas concorrentes.

**Regras do plugin (V-10):** (1) uma chave por **intenção de compra**, criada ao iniciar o checkout e reusada em todo reenvio; (2) gravar chave + hash do corpo + resposta; corpo diferente com a mesma chave é erro; (3) restrição única no banco para requisições simultâneas (**Inferido**: Stripe e Fowler não cobrem o caso concorrente em detalhe); (4) política de retenção documentada. Idempotência de requisição do Mercado Pago: **Não verificada**.

## 4. Criação segura de pedido e retenção por divergência

Padrão (V-20, fonte C: **padrão, não evidência**; consistente com V-09/V-10):

1. O pedido nasce **uma vez**, no evento de pagamento verificado (assinatura + confirmação pela API do provedor).
2. Compare valor pago, moeda e hash do carrinho com o registro do servidor. Divergência ⇒ estado **"retido para revisão"**: não entrega, não reembolsa sozinho.
3. Falha, timeout ou exceção na confirmação **nunca** libera pedido (OWASP A10, falhar fechado).
4. Mudanças em lote da loja passam por ledger (estado por item, checagem de frescor, aplicação idempotente, desfazer).
5. Reembolso/estorno no PSP sempre com aprovação humana (V-04).
6. Pagamento tardio (após liberar a reserva de estoque): reabrir se houver saldo; senão reter para revisão (ver [estoque-pedidos-promocoes.md](estoque-pedidos-promocoes.md)).

## 5. Pix

Fonte primária: especificação `openapi.yaml` do `bacen/pix-api` (V-31; Apache-2.0 declarado no YAML; API Pix 2.10.0; último commit 2026-08-19). A página institucional do BCB exige JavaScript e não foi lida.

- A API é exposta pelo **PSP recebedor**; o usuário recebedor acessa só o que o contrato permitir. Erros seguem a RFC 7807 (`type` identifica o erro).
- **Mudanças compatíveis** (campos novos, valores novos de enumeração) podem ocorrer a qualquer momento: o cliente ignora o que não conhece.
- `txid` segue `[a-zA-Z0-9]{26,35}`; endpoints `cob` e `cobv`; escopos OAuth2 como `cob.write`, `cob.read`, `webhook.write`.
- O webhook Pix **só notifica Pix associados a um `txid`**; cobrança sem `txid` não gera aviso ⇒ prever consulta de reconciliação.

**Regras do plugin:** (1) `txid` único por cobrança, guardando a associação cobrança↔pedido; (2) o aviso **não é prova de liquidação final**: conferir pela API (valor, `txid`, devoluções); (3) tolerar campos e valores novos; (4) devolução é evento próprio com estado final; (5) confirmar com o PSP o SLA do callback, a reentrega e o certificado mTLS; (6) testar sempre no ambiente de homologação do PSP. Política de expiração de cobrança e limites: **fora da especificação lida**.

## 6. Boleto e cartão

Conteúdo do brain-of-agent (MIT, próprio; **Inferido**, "conferido em 2026", não reverificado nesta rodada). Confirme no regulamento vigente antes de usar um número como resultado esperado.

| Tema | O que testar | Esperado |
| --- | --- | --- |
| Formatos de boleto | Código de barras (44 posições) × linha digitável (47 dígitos em cobrança; 48 em arrecadação/convênio, que começa com 8) | Aceita os dois; converte um no outro sem perder dígito |
| Dígitos verificadores | Alterar um dígito de cada campo | Linha digitável usa módulo 10 por campo; DV geral do código de barras, módulo 11; erro aponta o campo |
| Fator de vencimento | Boletos vencendo em 21/02/2025 e 22/02/2025 | O fator conta dias desde 07/10/1997; chegou a 9999 em 21/02/2025 e reiniciou em 1000 em 22/02/2025 |
| Ambiguidade | Fator 1000 | Pode ser 03/07/2000 ou 22/02/2025; resolver para o ciclo mais próximo da data atual |
| Valor | R$ 0,01; R$ 99.999.999,99; boleto sem valor | Campo de valor com 10 posições; sem valor (zeros) pede digitação |
| Vencimento | Sábado ou feriado da praça | Pago no próximo dia útil sem multa |
| Luhn | `4242 4242 4242 4241` | Recusado no cliente, sem chamar o gateway |
| Parcelamento | Valor mínimo de parcela; loja (sem juros) × emissor (com juros); trocar parcelas depois do cupom; estorno parcelado | Soma das parcelas = total |
| Cartão salvo | Expirado, removido, token de outro usuário (IDOR) | Recusa e autorização por objeto |

Armadilha: guardar a linha digitável como número (perde zeros à esquerda) ou calcular a data do fator com a base antiga sem o reinício (boleto aparece vencido há 25 anos).

## 7. Marketplace: cobrança, KYC, split e canais

Decisões completas em [decisoes-e-tradeoffs.md](decisoes-e-tradeoffs.md) (D-01 a D-03, D-09, D-10). Resumo operacional:

- **Tipos de cobrança (Stripe Connect, V-11):** direct (reembolso e contestação debitam a conta conectada), destination (debitam a plataforma, que pode reverter a transferência), cobranças + transferências **separadas** (carrinho multi-seller; transferência antes da liquidação). Monitorar saldo quando a transferência puder exceder a cobrança. Contas legadas Express/Custom v1: direct charges não recomendadas.
- **KYC (V-29):** hospedado, embutido ou via API (revisão de requisitos ao menos a cada 6 meses). Coleta antecipada (`eventually_due`) × incremental (`currently_due`). Antes de liberar repasse, ler o estado de requisitos; sem dados verificados a Stripe suspende cobranças e repasses. KYC do provedor não substitui LGPD, fiscal e antifraude.
- **Mercado Pago Split 1:1 (V-47, `mercadopago.com.br/developers/pt/docs/split-payments/split-1-1/integration-configuration/integrate-marketplace`):** taxa `marketplace_fee` (Checkout Pro, `/checkout/preferences`) ou `application_fee` (Checkout Transparente, `/payments`); **a comissão do Mercado Pago é descontada primeiro e a do marketplace incide sobre o restante** (registre a base de cálculo e confira em sandbox); estorno dividido proporcionalmente; sem saldo do vendedor, o marketplace estorna sua parte e decide se cobre o restante: **defina antes do go-live quem cobre saldo negativo**; só saldo entre contas Mercado Pago (instituições externas não); token do vendedor via OAuth no backend; `public_key` do integrador no frontend. Vale só para 1:1. A página não menciona KYC nível 6 nem parâmetro `marketplace`.
- **Canais (V-36):** classificar o canal (loja própria, marketplace de terceiros, plataforma multi-seller própria); por canal listar autenticação, tópicos/eventos de pedido, reentrega ("a descobrir"), comissão e quem emite a NF-e. Mercado Livre: horário em UTC, `orders_v2` recomendável para vendas. Mirakl: só a página inicial lida.
- **Frete por vendedor:** o Melhor Envio cota um frete por requisição ([fiscal-frete-br.md](fiscal-frete-br.md)).
- **Split tributário (IBS/CBS)** é assunto à parte (LC 214 arts. 31–35): ver [fiscal-frete-br.md](fiscal-frete-br.md); o plugin não calcula nem recolhe.

## 8. Riscos de pagamento e casos de teste (brain)

Tabela incorporada do domínio "Pagamentos e fintech" do brain-of-agent (`brains/qa/references/dominios.md`, MIT, conteúdo do próprio autor; **Inferido**, conferido em 2026). O oráculo é sempre um cálculo independente ou o extrato da outra ponta, nunca o valor que o sistema mostra.

| Risco | Caso que não pode faltar | Esperado |
| --- | --- | --- |
| Cobrança dupla | Duplo clique em "Pagar"; mesma requisição com a mesma `Idempotency-Key`; timeout do gateway seguido de retry | Uma cobrança só; a segunda chamada devolve o resultado da primeira |
| Chave mal escopada | Mesma chave com corpo diferente (R$ 100,00 e depois R$ 150,00) | Recusa explícita (conflito), nunca reaproveita |
| Arredondamento | R$ 100,00 em 3 parcelas; R$ 10,00 rateado entre 3 itens | 33,34 + 33,33 + 33,33 (ou a regra escrita); soma igual ao total |
| Ponto flutuante | `0.1 + 0.2` | Centavos inteiros ou decimal exato; nunca `float` |
| Regra de arredondamento | Juros de 1% a.m. sobre R$ 333,33 por 17 dias | Conferido por planilha independente (meio para cima × meio para o par) |
| Conciliação | Pedido pago × liquidação no extrato do adquirente/PSP | Casa por ID; divergência gera alerta, não ajuste silencioso |
| Estorno | Total, parcial, dois parciais somando mais que o original | Parcial reduz o saldo estornável; soma acima do original recusada |
| Chargeback | Contestação depois do repasse ao lojista | Débito registrado, pedido marcado, disputa com prazo visível |
| Limites | Limite diário R$ 5.000,00: 4.999,99 + 0,01; depois mais 0,01 | Aceita até 5.000,00; recusa 5.000,01 com mensagem do limite |
| Virada do limite | 23:59:59 e 00:00:00 no fuso do cliente | Contador zera no fuso da regra (em geral `America/Sao_Paulo`) |
| Antifraude | 10 tentativas em 1 minuto com cartões diferentes no mesmo dispositivo | Bloqueio ou desafio; caminho de recuperação ao cliente legítimo |
| Concorrência de saldo | Dois débitos de R$ 80,00 em conta com R$ 100,00 | Um aprova, outro recusa; saldo nunca negativo |

Armadilhas: testar o retry sem verificar o efeito no banco (conte as linhas, não a resposta); usar `float` no próprio teste e "acertar" o erro do sistema; esquecer que o webhook do gateway chega duplicado e fora de ordem (`pagamento.aprovado` antes de `pagamento.criado`).

**Pix, casos do brain (Inferido; confirme no regulamento vigente):**

| Tema | O que testar | Dados e esperado |
| --- | --- | --- |
| Chaves | CPF, CNPJ, e-mail, telefone, aleatória | CPF 11 dígitos; CNPJ 14 posições sem máscara; e-mail até 77 caracteres; telefone `+5511987654321`; aleatória é UUID de 36 caracteres. Teste chave com máscara colada, e-mail com maiúsculas, telefone sem `+55`; CNPJ alfanumérico (`12ABC34501DE35`) é aceito |
| QR estático × dinâmico | Mesmo QR pago duas vezes; expirado | Estático aceita vários pagamentos; `txid` de até 25 caracteres (ou `***`); dinâmico: payload por URL, expirado é recusado, `txid` de 26 a 35 |
| Devolução | Total, parcial, várias, após 90 dias | Iniciada pelo recebedor em até 90 dias; soma das devoluções ≤ valor original |
| MED | Pagador contesta por golpe | Contestação em até 80 dias; bloqueio cautelar; confirme prazos no regulamento vigente (o MED 2.0 rastreia contas intermediárias) |
| Limites | Noturno e dispositivo novo | Padrão de R$ 1.000,00 entre 20h e 6h; dispositivo novo: R$ 200,00 por transação e R$ 1.000,00 por dia até cadastrar (valores do brain; confirmar) |
| Timeout | Resposta não chega em 30 s | Consultar o status pelo EndToEndId antes de qualquer reenvio; reenviar às cegas gera Pix em dobro |
| Casos hostis | QR adulterado (CRC inválido), QR de outro recebedor, valor alterado entre leitura e confirmação, app fechado no meio | Recusar CRC inválido; conferir recebedor e valor na confirmação |

O **EndToEndId** tem 32 caracteres: `E` + 8 dígitos do ISPB de quem gerou + `AAAAMMDDHHmm` em UTC + 11 alfanuméricos; hora em UTC, não em Brasília. O `txid` é do recebedor; não confunda os dois.

Atribuição: tabelas adaptadas de `brains/qa/references/dominios.md` (`francisco-efjr/brain-of-agent`, MIT).

## 9. Testes que provam o handler

Evidência colada (comando + saída) de cada um:

- (a) assinatura inválida é rejeitada; (b) corpo reescrito por middleware é detectado; (c) o mesmo `event_id` duas vezes ⇒ **1 efeito** (contar linhas no banco, não olhar a resposta); (d) entregas simultâneas ⇒ a restrição única segura; (e) divergência de valor ⇒ pedido retido; (f) falha na fila não perde o evento; (g) reconciliação encontra um evento que nunca chegou.
- Para Asaas: token errado rejeitado, `id` repetido ⇒ 1 efeito, alerta de fila pausada. Para Melhor Envio: `X-ME-Signature` sobre o corpo bruto, resposta < 6 s, idempotência por `data.id` + `event`.
