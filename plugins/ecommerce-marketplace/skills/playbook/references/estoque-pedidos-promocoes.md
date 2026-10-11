# Estoque, reservas, pedidos, devoluções e promoções

Base das skills `estoque-reserva-pedido` e `precos-promocoes` e do agente `arquiteto-loja`. Padrões marcados **Inferido** são engenharia estável do domínio, sem norma ou documentação de plataforma que os fixe: apresente-os como proposta, não como regra do provedor.

Modelo-alvo: Claude 4.x/5.x · pesquisa validada em 2026-10-10 · compilado em 2026-10-11. Versões das plataformas mudam (Shopify a cada trimestre, Medusa v2.x): registre a versão e confira a documentação dela.

## Sumário

- [1. Escritor único e estados de estoque](#1-escritor-único-e-estados-de-estoque)
- [2. Reserva com expiração](#2-reserva-com-expiração) · [3. Locks](#3-locks)
- [4. Contratos por plataforma](#4-contratos-por-plataforma-medusa-shopify-nuvemshop-outras)
- [5. Estados do pedido](#5-estados-do-pedido) · [6. Pós-venda: devolução, troca, arrependimento, reembolso](#6-pós-venda)
- [7. Modelo de promoção, rateio e arredondamento](#7-modelo-de-promoção-rateio-e-arredondamento)
- [8. Casos de e-commerce do brain](#8-casos-de-e-commerce-do-brain) · [9. Testes obrigatórios](#9-testes-obrigatórios)

## 1. Escritor único e estados de estoque

**Escritor único (V-12; aplicação a estoque é Inferido):** reserva e baixa passam só por `<InventoryService>`; qualquer outro código chama o serviço. Verificação: (1) `grep` pelo nome do método de escrita e pelo SQL de `UPDATE` na tabela de estoque; (2) um teste que falha se a chamada vier de outro módulo (teste de origem da chamada). Se houver duas rotas, proponha consolidação via serviço antes de qualquer outra mudança.

**Estados separados** (V-39 Shopify, V-50): disponível (`available`), reservado/comprometido (`committed`/`reserved`), em mãos (`on_hand`), a caminho (`incoming`). Tratar "estoque" como um número só esconde a diferença entre o que existe, o que está prometido e o que pode ser vendido. Na Medusa, "vendável = estocado − reservado" é **Inferido** (a página não escreve a fórmula).

## 2. Reserva com expiração

Padrão da **aplicação** (V-39; **Inferido**: nenhuma fonte lida define TTL de reserva; o módulo de inventário da Medusa não tem expiração, V-24, V-48).

Modelo ilustrativo (PostgreSQL; não executado):

```sql
CREATE TABLE stock_reservations (
  id uuid PRIMARY KEY,
  cart_id text NOT NULL, order_id text, sku text NOT NULL,
  qty integer NOT NULL CHECK (qty > 0),
  status text NOT NULL CHECK (status IN ('held','confirmed','released','expired','review')),
  expires_at timestamptz NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now());
```

Fluxo:

1. **Reservar** na conclusão do carrinho (não ao adicionar: adicionar ao carrinho só confere saldo na Medusa), com `expires_at` = agora + prazo do meio de pagamento (cartão: minutos; Pix/boleto: o prazo da cobrança + folga). A reserva e a decisão "há saldo?" ocorrem na mesma transação do serviço único.
2. **Confirmar** no evento de pagamento verificado: adquira lock pela chave do carrinho, mude `held → confirmed`, vincule o `order_id`.
3. **Liberar** por job periódico: para cada `held` com `expires_at` vencido, **sem pagamento confirmado**, adquira o mesmo lock, releia o estado e mude para `expired`, devolvendo o saldo. O lock evita colidir com a confirmação do pagamento no mesmo instante.
4. **Pagamento após a liberação:** com o lock, se houver saldo, reabrir (`expired → confirmed`); se não houver, `review` (retenção para revisão humana) e **sem reembolso autônomo** (V-20).
5. **Cancelamento e devolução** também liberam reserva; na Medusa o cancelamento apaga as reservas (Verificado), o efeito sobre o estocado físico é **Não verificado**: teste.

Testes: dois checkouts pela última unidade (um falha limpo); pagamento após o TTL; falha do job no meio (idempotente; retomar sem duplicar); transição inválida; reserva duplicada com a mesma chave ⇒ 1 efeito.

## 3. Locks

Fonte: documentação de locks de workflow da Medusa (V-39, V-49, **Verificado** em 2026-10-10); o raciocínio vale para qualquer stack.

- `acquireLockStep`: `key` (ex.: ID do carrinho), `timeout` (espera máxima, em segundos; sem default declarado para o step), `ttl` (posse máxima, em segundos, contra travamento). Exemplo da documentação: `timeout` 30 e `ttl` 120 ao redor de `completeCartWorkflow`, chave do carrinho. A compensação libera o lock se o workflow falha depois.
- Regras: chave = ID do carrinho para a seção de reserva; `ttl` acima do **pior caso medido**; `timeout` vencido é falha recuperável (a compra pode tentar de novo), não erro fatal; **em workflow aninhado, `acquireLockStep` não adquire lock: o workflow pai adquire e libera, com a mesma chave**; não adquirir lock no workflow e em um step na mesma execução (deadlock). O default de 5 s do provedor Redis vale quando o lock é adquirido por um step via serviço do módulo de locking, com backoff exponencial, e é separado do `timeout` do step.
- **TTL de lock (segundos) ≠ TTL de reserva (minutos).** Confundir os dois é erro comum.

## 4. Contratos por plataforma (Medusa, Shopify, Nuvemshop, outras)

**Medusa v2** (V-24, V-39, V-48, V-49; conferir a versão):

| Cenário | Esperado | Rótulo |
| --- | --- | --- |
| Pedido criado | Estocado igual; reserva existe por variante com `manage_inventory` ativo (criada na conclusão do carrinho, `completeCartWorkflow`). `createOrderWorkflow` **não** cria reservas: chamar `createReservationsWorkflow` com `line_item_id` | Verificado |
| `cancelOrderWorkflow` | Valida (erro se houver fulfillment não cancelado ou pedido já cancelado) → apaga reservas dos itens → cancela pagamentos → emite eventos (`order.canceled`, `reservation-item.deleted` desde v2.18.0) → cancela o pedido; hook `orderCanceled`; entradas `order_id`, `no_notification`, `canceled_by`. Disponibilidade recalculada: leia pela API | Verificado; estocado físico: **Não verificado** |
| Fulfillment | A quantidade reservada sai do estocado e a reserva é apagada; fulfillment sem reserva gera erro | Verificado |
| Devolução | Recebida repõe o estocado; danificada não | Verificado |
| Reserva manual | Criação, edição e exclusão existem na administração; exclusão é irreversível e pode exigir realocar itens | Verificado |
| Regras de código | Workflows de `@medusajs/framework/workflows-sdk` com ao menos um step; funções de workflow não são `async`; sem `await` em chamadas de step; erros com `MedusaError`; dados via Query; modelos em snake_case; um `id` como `primaryKey()`; serviços estendem `MedusaService`; **conferir a versão** | Verificado (arquivo de comunidade, CC0) |
| TTL de reserva | Não existe no módulo: é da aplicação | Verificado (silêncio da doc) |

**Shopify** (V-50, `shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps/manage-quantities-states` e objeto `InventoryLevel`): `available` é escrito por `inventorySetQuantities`, `inventoryAdjustQuantities` e `inventoryMoveQuantities`; `on_hand` (soma de available, committed, reserved, damaged, safety_stock e quality_control) só por `inventorySetQuantities`; `committed` **não pode ser ajustado nem movido** pela Admin GraphQL (a Shopify o altera ao criar e atender pedidos e ao reservar em rascunhos); `reserved`, `damaged`, `safety_stock`, `quality_control` por ajuste ou movimento. `referenceDocumentUri` explica a mudança (preferencialmente um GID) e aparece no histórico. `InventoryLevel.quantities` **exige o argumento `names`**. `scheduledChanges` é o único campo depreciado (o estado `incoming` não está depreciado). Como `available`, `on_hand` e `reserved` mudam em cada etapa do pedido: **não documentado**. `stockAtLegacyLocation` em `inventoryActivate`: **Não verificado**. Para segurar unidade manualmente, use `reserved` com `referenceDocumentUri` e teste de liberação.

**Nuvemshop** (V-52): `status` (`open`, `closed`, `cancelled`); `payment_status` (`pending`, `authorized`, `paid`, `voided`, `refunded`, `abandoned`; `partially_paid` e `partially_refunded` aparecem só na tabela de propriedades: inconsistência interna da página); `shipping_status` (`unpacked`, `shipped`, `unshipped`, `delivered`, `partially_packed`, `partially_fulfilled`). Cancelamento `POST /orders/{id}/cancel`: `reason` (`customer`, `inventory`, `fraud`, `other`), `email` (padrão true), **`restock` (padrão true: envie explícito)**. `inventory_behaviour`: `bypass` (padrão, não reivindica estoque) ou `claim` (pode impedir a criação): escolha de propósito e teste a corrida; `unclaimed_stock` por corrida entre compradores é alerta de revisão. Paginação padrão 30; teto de 10.000 itens por consulta (erro acima): paginar por intervalo de datas. Multi-estoque: `inventory_levels` por `location_id`; `variant.stock` é o total, mas **depreciado** em criação e atualização; apps que usam endpoints depreciados nos últimos 14 dias falham na aprovação de multi-estoque. Decremento por pedido, atomicidade e lote: **Não verificável**; risco de venda acima do saldo com `bypass` é **Inferido**. Não há evento de saldo de estoque nos webhooks: reconcilie por API.

**WooCommerce e VTEX:** estoque e pedidos (HPOS, gateways; Catalog, Checkout e OMS) **não foram lidos**: diga "Não verificado" ao gerar código dessas partes. VTEX Orders Feed/Hook: ver [pagamentos-webhooks-split.md](pagamentos-webhooks-split.md).

## 5. Estados do pedido

Máquina proposta (**Inferido**, derivada do brain; adapte à plataforma):

| De | Para | Disparo | Condição |
| --- | --- | --- | --- |
| criado | aguardando_pagamento | Cobrança emitida | Reserva criada |
| aguardando_pagamento | pago | Evento de pagamento **verificado** | Valor/moeda/hash conferem |
| aguardando_pagamento | cancelado | Expiração ou desistência | Libera reserva |
| aguardando_pagamento / pago | retido_para_revisao | Divergência ou pagamento tardio sem saldo | Humano decide |
| pago | em_separacao → enviado → entregue | Fulfillment / etiqueta | Etiqueta só após pagamento confirmado |
| criado / aguardando / pago / em_separacao | cancelado | Cliente ou loja | Libera reserva; reembolso com aprovação humana |
| entregue | devolucao_solicitada → devolvido → reembolso_pendente → reembolsado | Arrependimento/troca | Seção 6 |
| entregue | cancelado | **Inválida** | Teste: cancelar pedido entregue pela API é recusado |

Cada transição tem responsável (serviço único), idempotência e log estruturado sem PII. Diagrama em [diagrama-estados-reserva.md](../assets/templates/diagrama-estados-reserva.md).

## 6. Pós-venda

Classificar antes de tratar (roteamento, V-04): **troca**, **devolução**, **arrependimento**, **reembolso parcial** têm fluxos diferentes.

- Transições explícitas: devolvido → reembolso pendente → reembolsado.
- **Chave de idempotência própria por reembolso;** soma de reembolsos ≤ valor capturado (reembolsos parciais cuja soma excedesse o capturado são rejeitados); reembolso duplicado com a mesma chave ⇒ 1 efeito.
- Retorno ao estoque **só após conferência** (devolução danificada não repõe).
- **Reembolso/estorno no PSP sempre com aprovação humana** (efeito em pagamento ⇒ ponto de parada).
- **Arrependimento (V-55, V-32):** CDC art. 49 — 7 dias do recebimento, contratação fora do estabelecimento (a internet não é citada no caput); devolução imediata, com atualização monetária, dos valores pagos a qualquer título; Decreto 7.962 art. 5º: meio na mesma ferramenta da compra, confirmação imediata, comunicação à administradora do cartão. "Dias corridos", "frete devolvido", "sem exigir motivo" = **Inferido/Suposição**. **Requer revisão jurídica**; use [tabela-conformidade-br.md](../assets/templates/tabela-conformidade-br.md).
- Nota fiscal: pagamento confirmado, cancelamento e devolução geram documento no evento certo (cancelamento dentro do prazo da SEFAZ ou nota de devolução depois; brain, **Inferido**); o plugin não emite.

## 7. Modelo de promoção, rateio e arredondamento

**Quatro partes (V-38, Medusa):** **alvo** (itens, métodos de envio ou pedido), **regra** (quando vale), **campanha** (período e orçamento) e **ordem de aplicação**. Na Medusa: `computeActions` devolve `addItemAdjustment`, `removeItemAdjustment`, `addShippingMethodAdjustment`, `removeShippingMethodAdjustment` e `campaignBudgetExceeded`; promoção percentual incide sobre o **valor restante**; promoção de pedido (percentual ou fixa) é distribuída proporcionalmente ao valor restante dos itens; `buyget` existe e é aplicado **antes** das `standard`. Limite de uso por cliente: não descrito (só o orçamento da campanha). Shopify Functions (`cart.lines.discounts.generate.run`, `productDiscountsAdd` com `candidates`, `targets`, `value`, `selectionStrategy`): limite de **25 funções de desconto ativas por loja** (Verificado); valor fixo e teto **Não verificados**.

**Regras que o plugin exige escritas e testadas:**

1. Valores em **inteiros de unidade menor**; moeda ISO 4217 junto. Nunca `float` (S-13).
2. **Ordem percentual × fixo:** R$ 200,00 com 10% e R$ 20,00 ⇒ percentual primeiro: 200 → 180 → 160; fixo primeiro: 180 → 162 (brain). Escolha, escreva e teste as duas.
3. **Frete grátis:** o limite (ex.: R$ 199,00) vale antes ou depois do desconto? Teste subtotal 198,99 e 199,00 e um cupom que derruba o subtotal abaixo do limite.
4. **Rateio:** exemplo em centavos — itens 3333, 3333, 3334 (soma 10000) e desconto de pedido de 1000: parte de cada item = ⌊1000 × preço / 10000⌋ = 333, 333, 333 (soma 999); o centavo restante vai ao último item ⇒ 333 + 333 + 334 = 1000. A regra "resto no último item" é **Inferido** (nenhuma fonte lida a define); escreva a sua.
5. **Parcelamento:** 100,00 em 3x = 33,34 + 33,33 + 33,33 (brain; resto na primeira parcela) ou a regra escrita; a soma é exatamente o total. A regra de resto das parcelas e a do rateio podem diferir: documente ambas.
6. O servidor **recalcula tudo**; o cliente só exibe.
7. Preço final discrimina frete e seguros (Decreto 7.962 art. 2º, IV).
8. Cupom: expirado, de primeira compra reutilizado e aplicado a item excluído ⇒ recusa com motivo; cupom duplicado; orçamento da campanha esgotado.

Testes: parametrizados, com **oráculo independente** (planilha ou cálculo separado), carrinho sintético com **3 itens de preços diferentes e um fora da promoção**, soma dos rateios = total. Entregue `SPEC.md` ([plano-feature-loja.md](../assets/templates/plano-feature-loja.md)) com requisitos EARS ("QUANDO … O SISTEMA DEVE …", V-22) e Gherkin.

## 8. Casos de e-commerce do brain

Tabela incorporada do domínio "E-commerce" do brain-of-agent (`brains/qa/references/dominios.md`, MIT, conteúdo do próprio autor; **Inferido**, "conferido em 2026", não reverificado nesta rodada).

| Área | Casos | Esperado |
| --- | --- | --- |
| Carrinho | Anônimo com 2 itens faz login em conta que já tinha 1 item | Mescla (3 itens) ou regra escrita; nunca perde os itens anônimos |
| Carrinho | Item fica sem estoque ou muda de preço no carrinho | Aviso claro antes do pagamento; preço cobrado é o confirmado na revisão |
| Estoque | Último item: dois clientes finalizam ao mesmo tempo | Um compra, outro recebe "esgotado"; estoque nunca negativo |
| Estoque | Pix gerado e não pago até expirar | Reserva liberada no fim do prazo |
| Cupons | R$ 200,00 com 10% e R$ 20,00 cumulativos | 10% antes: 200 → 180 → 160; fixo antes: 180 → 162. A regra diz a ordem; teste as duas |
| Cupons | Expirado, primeira compra reutilizado, item excluído da promoção | Recusa com motivo |
| Frete grátis | Limite R$ 199,00: subtotal 198,99 e 199,00; cupom que derruba o subtotal abaixo do limite | A regra diz se o limite é antes ou depois do desconto |
| Frete por CEP | CEP inexistente, rural, com zero à esquerda (01310-100) | Mensagem clara; CEP salvo como texto de 8 dígitos |
| Checkout | Abandonar no pagamento e voltar; pagamento recusado | Carrinho preservado; nova tentativa não duplica pedido |
| Estados do pedido | criado → aguardando pagamento → pago → em separação → enviado → entregue; cancelado; devolvido | Cada transição válida e tentativas inválidas (cancelar pedido entregue pela API) |
| Arrependimento | Pedido entregue há 7 e há 8 dias | CDC art. 49: 7 dias do recebimento em compra fora da loja física; reembolso integral, frete incluso, estorno no cartão (**o plugin rotula "frete incluso" como Inferido**; ver seção 6) |
| Nota fiscal | Pagamento confirmado, cancelamento, devolução | NF-e/NFC-e no evento certo; cancelamento dentro do prazo da SEFAZ ou nota de devolução depois |
| Busca | "cafe" × "café", "tenis" × "tênis", "celuar", "geladeira" × "refrigerador", SKU, zero resultados | Acento e caixa ignorados; tolerância a erro; página de zero resultados com sugestão |
| Pico | Black Friday, lançamento | Teste a fila de checkout e o gateway lento (detalhe em `/qa-testing:playbook`) |

Armadilha: testar promoção só com um item. Defeitos de rateio aparecem com 3 itens de preços diferentes e um fora da promoção.

Atribuição: tabela adaptada de `francisco-efjr/brain-of-agent` (MIT).

## 9. Testes obrigatórios

Estoque: concorrência (última unidade), pagamento após TTL, falha do job no meio, cancelamento/devolução liberando reserva, transição inválida. Pedido: reembolso duplicado com a mesma chave ⇒ 1 efeito; reembolsos parciais cuja soma excederia o capturado ⇒ rejeitado; contagem de linhas no banco (não a resposta). Promoções: seção 7. Contagens e logs são a evidência; resposta HTTP 200 não prova o efeito.
