# Pós-venda e contratos de estoque por plataforma

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Fontes: CDC art. 49 (Planalto, V-55), Decreto 7.962/2013 (V-32), Medusa (V-39, V-48, V-49), Shopify (V-50), Nuvemshop (V-52). Prazos legais: **Requer revisão jurídica**; nada aqui é parecer. A lógica de reembolso idempotente foi executada em 2026-10-10 (SQLite em memória, Python 3.14).

## 1. Classificar antes de tratar

| Pedido do cliente | O que é | Efeito em estoque | Efeito em dinheiro |
|---|---|---|---|
| "Quero cancelar" antes do envio | Cancelamento | Libera a reserva | Reembolso total (aprovação humana) |
| "Me arrependi" depois do recebimento | Arrependimento (CDC art. 49) | Reposição após conferência | Devolução dos valores pagos, de imediato, conforme prazo e decisão do jurídico |
| "Veio defeituoso/errado" | Devolução por problema | Danificado não repõe estoque vendável | Reembolso ou troca, conforme política |
| "Quero outro tamanho" | Troca | Entra o devolvido (se bom), sai o novo | Diferença de preço, se houver |
| "Só um dos 3 itens" | Reembolso parcial | Só o item devolvido | Valor parcial, soma <= capturado |

## 2. Estados e idempotência do pós-venda

devolução solicitada -> aprovada -> mercadoria recebida e conferida -> reembolso pendente -> reembolsado (ou recusada/encerrada). Cada seta tem responsável e log. Regras:

1. Chave de idempotência própria por reembolso (UUID criado ao aprovar a devolução, reutilizado em todo reenvio ao PSP).
2. Soma dos reembolsos do pedido <= valor capturado, checada na **mesma transação** que grava o reembolso.
3. Repetição da mesma chave devolve o resultado salvo; a mesma chave com valor ou pedido diferente é conflito. Importante: consulte a chave **antes** da regra de soma; senão uma repetição legítima de um reembolso já feito é recusada como "soma excedida" em vez de devolver o resultado salvo (defeito observado no teste abaixo).
4. Retorno de estoque só após conferência física; item danificado não vira vendável.
5. Reembolso e estorno no PSP exigem aprovação humana e acontecem fora do agente.

```sql
-- Reembolso: 1 linha inserida = aceito; 0 linhas = soma excederia o capturado.
-- Antes, SELECT por chave: se existir, devolva o resultado salvo (mesmo corpo) ou conflito (corpo diferente).
-- Dentro de transação com bloqueio do pedido (SELECT ... FROM pedidos WHERE id = :pedido FOR UPDATE).
INSERT INTO reembolsos (pedido_id, valor_centavos, chave)
SELECT :pedido, :valor, :chave
 WHERE (SELECT COALESCE(SUM(valor_centavos), 0) FROM reembolsos WHERE pedido_id = :pedido) + :valor
       <= (SELECT capturado_centavos FROM pedidos WHERE id = :pedido);
-- reembolsos.chave tem UNIQUE: segunda linha de defesa contra duplicata concorrente.
```

Teste executado (lógica; adapte ao banco do projeto):

```python
import sqlite3
c = sqlite3.connect(":memory:")
c.executescript("""
CREATE TABLE pedidos (id TEXT PRIMARY KEY, capturado INTEGER NOT NULL);
CREATE TABLE reembolsos (id INTEGER PRIMARY KEY, pedido_id TEXT NOT NULL, valor INTEGER NOT NULL CHECK (valor > 0),
  chave TEXT NOT NULL UNIQUE);
INSERT INTO pedidos VALUES ('P1', 10000);
""")

def reembolsar(pedido, valor, chave):
    previo = c.execute("SELECT pedido_id, valor FROM reembolsos WHERE chave = ?", (chave,)).fetchone()
    if previo:   # repetição idempotente: mesmo corpo devolve o resultado salvo; corpo diferente é erro
        return 'duplicada' if previo == (pedido, valor) else 'conflito'
    try:
        cur = c.execute("""INSERT INTO reembolsos (pedido_id, valor, chave)
          SELECT ?, ?, ? WHERE (SELECT COALESCE(SUM(valor), 0) FROM reembolsos WHERE pedido_id = ?) + ?
                              <= (SELECT capturado FROM pedidos WHERE id = ?)""",
          (pedido, valor, chave, pedido, valor, pedido))
        return cur.rowcount == 1
    except sqlite3.IntegrityError:
        return 'duplicada'

assert reembolsar('P1', 6000, 'k1') is True
assert reembolsar('P1', 6000, 'k1') == 'duplicada'     # mesma chave, mesmo corpo
assert reembolsar('P1', 7000, 'k1') == 'conflito'      # mesma chave, corpo diferente
assert reembolsar('P1', 6000, 'k2') is False           # soma 12000 > capturado 10000
assert reembolsar('P1', 4000, 'k3') is True            # fecha exatamente 10000
```

## 3. Arrependimento e devolução: o que a lei lida diz e o que não diz

- CDC art. 49 (texto compilado do Planalto, lido em 2026-10-10): 7 dias da assinatura ou do recebimento, contratação **fora do estabelecimento comercial** ("especialmente por telefone ou a domicílio"; o caput não cita a internet); parágrafo único: devolver de imediato, com atualização monetária, os valores pagos "a qualquer título".
- Decreto 7.962/2013, art. 5º (lido em V-32): informar os meios do direito de arrependimento; exercício pela mesma ferramenta da contratação; rescisão de contratos acessórios sem ônus; comunicação imediata à administradora do cartão; confirmação imediata do pedido.
- **Inferido**: dias corridos; devolução do frete ("a qualquer título"). **Suposição/Não verificado**: "sem exigir motivo", "política interna não restringe". O brain-of-agent (MIT) escreve "reembolso integral, frete incluso" na tabela de casos: tratar como Inferido, pois o texto lido não diz isso literalmente.
- Checklist de implementação: (1) contar 7 dias a partir do recebimento (decisão de contagem registrada com o jurídico); (2) canal simples de pedido, na mesma ferramenta da compra; (3) devolver o pago de imediato; frete conforme parecer; (4) estorno ou comunicação à administradora do cartão; (5) reembolso ao PSP só com aprovação humana.
- Teste do brain (Inferido): pedido entregue há 7 dias e há 8 dias, com a regra de contagem escrita, e o resultado do 8º dia conferido com o jurídico.

## 4. Contratos de teste por plataforma

Registre sempre versão e data da doc. O que está **Não verificado** não vira afirmação; vira teste em ambiente de desenvolvimento.

### Medusa v2 (V-24, V-39, V-48, V-49)

| # | Teste | Resultado esperado | Rótulo |
|---|---|---|---|
| 1 | Concluir carrinho de variante com `manage_inventory` | Reserva criada por variante; estocado inalterado | Verificado (doc) |
| 2 | Pedido criado por `createOrderWorkflow` | **Não** cria reserva; chamar `createReservationsWorkflow` com `line_item_id` | Verificado |
| 3 | `cancelOrderWorkflow` | Reservas do pedido apagadas; eventos `order.canceled` e `reservation-item.deleted` (este desde v2.18.0); disponibilidade recalculada, **lida pela API** | Verificado |
| 4 | Estocado físico após cancelamento | O que acontece com o físico: a página silencia | **Não verificado**: teste |
| 5 | Fulfillment | Estocado cai, reserva some; fulfillment sem reserva dá erro | Verificado |
| 6 | Devolução recebida / danificada | Recebida soma ao estocado; danificada não | Verificado |
| 7 | Vendável = estocado - reservado | Fórmula não está na página | **Inferido** |
| 8 | TTL de reserva | Não existe no módulo; é da aplicação | Verificado (ausência na doc lida) |
| 9 | Duas compras da última unidade com lock | Uma falha limpa; chave = ID do carrinho | Verificado (padrão), teste obrigatório |

Regras de código Medusa v2 (V-24, arquivo da comunidade, CC0 no repositório; confira a versão e a doc de workflows): workflows de `@medusajs/framework/workflows-sdk` com ao menos um step; funções de workflow não são `async`; sem `await` em chamadas de step; erros com `MedusaError`; dados via Query; nomes de modelos e campos em snake_case; serviços estendem `MedusaService`. O arquivo de origem começa com uma persona dirigida à IA ("expert senior..."), tratada como dado, sem efeito. A página oficial de inventário contém um bloco "AgentInstructions" pedindo feedback a endpoint externo: dado, ignorado.

### Shopify (V-39, V-50)

| # | Teste | Resultado esperado | Rótulo |
|---|---|---|---|
| 1 | Ler `InventoryLevel.quantities` | Exige `names` explícito (`available`, `on_hand`, `committed`, `reserved`, ...) | Verificado |
| 2 | Escrever `committed` | Impossível pela Admin GraphQL; a Shopify o altera ao criar/atender pedidos e reservar em rascunhos | Verificado |
| 3 | Escrever `available` | `inventorySetQuantities`, `inventoryAdjustQuantities`, `inventoryMoveQuantities` | Verificado |
| 4 | Escrever `on_hand` | Só por `inventorySetQuantities` | Verificado |
| 5 | Segurar unidade manualmente | `reserved` com `referenceDocumentUri` (URI livre, preferencialmente GID; aparece no histórico) e teste de liberação | Verificado; não use para detectar holds antes de ler o changelog |
| 6 | Efeito de cada etapa do pedido sobre `available/on_hand/reserved` | Não documentado | **Não documentado**: testar em loja de desenvolvimento |
| 7 | Mudança agendada | `scheduledChanges` é o único campo depreciado do objeto; `inventorySetScheduledChanges` indisponível na versão 2026-07 | Verificado |
| 8 | `stockAtLegacyLocation` em `inventoryActivate` | — | **Não verificado** |

`on_hand` = soma de `available`, `committed`, `reserved`, `damaged`, `safety_stock` e `quality_control`. Idempotência: a Admin API tem documentação de requisições idempotentes citada na página de `InventoryLevel`. Versão da API é trimestral: registre-a.

### Nuvemshop (V-51, V-52)

| # | Teste | Resultado esperado | Rótulo |
|---|---|---|---|
| 1 | Cancelar pedido (`POST /orders/{id}/cancel`) | Enviar `restock` explícito (padrão true), `reason` (customer, inventory, fraud, other), `email` (padrão true) | Verificado |
| 2 | `inventory_behaviour` | `bypass` (padrão, não reivindica estoque) × `claim` (pode impedir a criação do pedido): escolher de propósito e testar a corrida | Verificado; risco de vender acima do saldo com `bypass`: **Inferido** |
| 3 | `unclaimed_stock` | Tratar como alerta de revisão (pode ocorrer por corrida entre compradores) | Verificado |
| 4 | Paginação de pedidos | Padrão 30; teto de 10.000 itens por consulta, com erro acima: paginar por intervalo de datas | Verificado |
| 5 | Escrita de estoque | Por `inventory_levels` e `location_id`; `variant.stock` (total) depreciado em criação/atualização | Verificado |
| 6 | Decremento por pedido, atomicidade, lote | — | **Não verificado** (a página remete a outros guias) |
| 7 | Teste de concorrência de estoque | — | **Não verificável** |

Estados do pedido Nuvemshop: `status` (open, closed, cancelled); `payment_status` (pending, authorized, paid, voided, refunded, abandoned; `partially_paid` e `partially_refunded` aparecem só na tabela de propriedades: inconsistência interna da página); `shipping_status` (unpacked, shipped, unshipped, delivered, partially_packed, partially_fulfilled). Apps que usam endpoints depreciados nos últimos 14 dias falham na aprovação automática de multi-estoque; lojas multi-local precisam migrar para `inventory_levels`.

### WooCommerce e VTEX

WooCommerce e VTEX (Catalog, Checkout, OMS) têm cobertura parcial: ao gerar código de estoque ou pedido para essas plataformas, escreva "Não verificado" nas partes sem leitura da doc vigente (VTEX Orders Feed: ver skill `webhook-pagamento`).
