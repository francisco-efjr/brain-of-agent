# Modelo de promoção, oráculo e testes

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. O código Python abaixo foi **executado em 2026-10-10** (Python 3.14, saída colada na seção 2). Decisões de arredondamento e de resto de rateio são **Inferido** (V-38: nenhuma fonte lida as define). Fontes: Medusa promotion e actions (V-38), Shopify Functions product-discounts (V-38, lido até ~100 mil de ~426 mil caracteres), Decreto 7.962/2013 art. 2º IV (V-32), brain-of-agent (MIT; tabelas de pagamentos e e-commerce).

## 1. Decisões que a spec precisa fixar (e o efeito de cada uma)

| Decisão | Opções | Efeito no exemplo | Registrar |
|---|---|---|---|
| Ordem percentual × fixo | percentual primeiro; fixo primeiro | R$ 200: 160 × 162 (cupons cumulativos). No carrinho da seção 2: R$ 164,00 × R$ 165,60 | ADR curto ou linha na SPEC, com o porquê de negócio |
| Base do percentual | valor original; valor restante | Medusa: sobre o restante | Fórmula escrita |
| Desconto de pedido | distribuído por item × só no total | Medusa distribui proporcional ao valor restante | Regra de rateio |
| Resto de centavos | último item; maior resto; primeiro item | Muda 1 a 2 centavos por item, soma igual | Regra escolhida (Inferido) |
| Arredondamento do percentual | meio para cima; meio para o par | `1% de 333,33` = 3,33; juros e IOF pedem a regra do contrato | Regra escolhida |
| Frete grátis | limite antes do desconto; depois | Limite 199,00 e subtotal 199,00 com cupom de 1,00 | Base escrita |
| Acumulação | cupom + automática; só uma; por tipo | Cupom duplicado recusado | Tabela de compatibilidade |
| Orçamento da campanha | por valor; por usos; sem limite | `campaignBudgetExceeded` na Medusa | Comportamento ao esgotar (recusa com motivo) |

## 2. Oráculo em centavos inteiros (executado)

Use uma função independente do código de produção, ou uma planilha, como fonte dos valores esperados. Esta versão serve de referência de lógica; não importe o código de produção dentro do oráculo.

```python
"""Oráculo de promoção em centavos inteiros (resto do rateio no último item). Sem float."""

def pct(valor, bps):
    """Percentual em pontos-base (1000 = 10%), meio para cima."""
    return (valor * bps + 5000) // 10000

def ratear(total, bases):
    """Distribui `total` proporcional a `bases`; o resto de centavos vai ao último item."""
    soma = sum(bases)
    if soma == 0 or total == 0:
        return [0] * len(bases)
    partes = [total * b // soma for b in bases]
    partes[-1] += total - sum(partes)
    return partes

def calcular(itens, pct_bps, fixo, ordem="percentual_primeiro"):
    """itens: [{'sku','preco','qtd','elegivel_pct'}]. `fixo` é desconto de pedido sobre o valor restante."""
    linhas = [i["preco"] * i["qtd"] for i in itens]
    elegiveis = [l if i["elegivel_pct"] else 0 for l, i in zip(linhas, itens)]
    if ordem == "percentual_primeiro":
        desc_pct = [pct(e, pct_bps) for e in elegiveis]
        restante = [l - d for l, d in zip(linhas, desc_pct)]
        desc_fixo = ratear(min(fixo, sum(restante)), restante)
    else:  # fixo_primeiro
        desc_fixo = ratear(min(fixo, sum(linhas)), linhas)
        restante_el = [max(e - f, 0) if e else 0 for e, f in zip(elegiveis, desc_fixo)]
        desc_pct = [pct(e, pct_bps) for e in restante_el]
    liquido = [l - dp - df for l, dp, df in zip(linhas, desc_pct, desc_fixo)]
    return {"linhas": linhas, "desc_pct": desc_pct, "desc_fixo": desc_fixo, "liquido": liquido, "total": sum(liquido)}

def parcelas(total, n):
    base, resto = divmod(total, n)
    return [base + (1 if i < resto else 0) for i in range(n)]

def frete_gratis(subtotal, limite, depois_do_desconto, desconto):
    base = subtotal - desconto if depois_do_desconto else subtotal
    return base >= limite

carrinho = [
    {"sku": "A", "preco": 10000, "qtd": 1, "elegivel_pct": True},
    {"sku": "B", "preco": 3000, "qtd": 2, "elegivel_pct": True},
    {"sku": "C", "preco": 4000, "qtd": 1, "elegivel_pct": False},   # fora da promoção
]
r1 = calcular(carrinho, 1000, 2000, "percentual_primeiro")
r2 = calcular(carrinho, 1000, 2000, "fixo_primeiro")
print(r1); print(r2)
for r in (r1, r2):
    assert sum(r["desc_fixo"]) == 2000 and r["total"] == sum(r["linhas"]) - sum(r["desc_pct"]) - 2000
    assert all(x >= 0 for x in r["liquido"])
assert r1["total"] != r2["total"]
assert parcelas(10000, 3) == [3334, 3333, 3333] and sum(parcelas(10000, 3)) == 10000
assert frete_gratis(19899, 19900, False, 0) is False and frete_gratis(19900, 19900, False, 0) is True
assert frete_gratis(19900, 19900, True, 100) is False
assert pct(33333, 100) == 333
```

Saída observada em 2026-10-10:

```text
{'linhas': [10000, 6000, 4000], 'desc_pct': [1000, 600, 0], 'desc_fixo': [978, 586, 436], 'liquido': [8022, 4814, 3564], 'total': 16400}
{'linhas': [10000, 6000, 4000], 'desc_pct': [900, 540, 0], 'desc_fixo': [1000, 600, 400], 'liquido': [8100, 4860, 3600], 'total': 16560}
```

Leitura: carrinho de R$ 200,00 (A R$ 100,00 x1, B R$ 30,00 x2, C R$ 40,00 x1 fora da promoção), cupom de 10% só em A e B e desconto de pedido de R$ 20,00. Percentual primeiro: R$ 164,00. Fixo primeiro: R$ 165,60. A diferença de R$ 1,60 é a razão para a spec dizer a ordem. O desconto de pedido de 20,00 foi distribuído em 9,78 + 5,86 + 4,36 (soma exata 20,00).

## 3. SPEC em EARS + Gherkin (exemplo preenchido)

Requisitos (EARS, formato "WHEN ... THE SYSTEM SHALL ..."):

- FR-001 WHEN o checkout calcula o total, THE SYSTEM SHALL ignorar qualquer valor monetário recebido do cliente e recalcular a partir de SKU, quantidade, tabela de preços e promoções válidas.
- FR-002 WHEN houver cupom percentual e desconto de pedido fixo no mesmo carrinho, THE SYSTEM SHALL aplicar o percentual primeiro, sobre os itens elegíveis, e distribuir o fixo proporcionalmente ao valor restante de cada item.
- FR-003 WHEN o desconto de pedido não for divisível em centavos entre os itens, THE SYSTEM SHALL atribuir o resto ao último item, de modo que a soma dos rateios seja igual ao desconto.
- FR-004 WHEN o subtotal após descontos for maior ou igual a R$ 150,00, THE SYSTEM SHALL zerar o frete.
- FR-005 WHEN o cupom estiver expirado, esgotado ou já aplicado ao carrinho, THE SYSTEM SHALL recusá-lo com o motivo.
- FR-006 WHEN o total for parcelado em N vezes sem juros, THE SYSTEM SHALL distribuir o resto nas primeiras parcelas, com soma igual ao total.
- FR-007 THE SYSTEM SHALL exibir o preço final com frete e seguros discriminados antes do pagamento.

```gherkin
Funcionalidade: cupom percentual com desconto de pedido fixo
  Cenário: percentual primeiro, rateio exato
    Dado um carrinho com A R$ 100,00 x1, B R$ 30,00 x2 e C R$ 40,00 x1 (C fora da promoção)
    Quando aplico o cupom de 10% e o desconto de pedido de R$ 20,00
    Então os descontos por item são A 10,00+9,78, B 6,00+5,86 e C 0,00+4,36
    E o total é R$ 164,00 e a soma dos rateios do desconto de pedido é R$ 20,00

  Cenário: cupom duplicado
    Dado um carrinho com o cupom "VERAO10" já aplicado
    Quando aplico "VERAO10" de novo
    Então o sistema recusa com "cupom já aplicado" e o total não muda

  Cenário: orçamento da campanha esgotado
    Dado uma campanha com orçamento restante de R$ 5,00 e um desconto de R$ 20,00
    Quando aplico a promoção
    Então o sistema recusa com "campanha esgotada" (comportamento escolhido na SPEC)

  Esquema do Cenário: limite de frete grátis em R$ 150,00 após descontos
    Dado um subtotal após descontos de <subtotal>
    Então o frete é <frete>
    Exemplos:
      | subtotal | frete  |
      | 149,99   | cobrado |
      | 150,00   | grátis  |
```

Pontos a decidir com o negócio e escrever na SPEC: o comportamento exato com orçamento parcialmente disponível (recusar, aplicar parcial) e se "primeira compra" considera contas apagadas. Sem decisão, marque "pergunta aberta" e não implemente por palpite.

## 4. Matriz de testes

| Caso | Entrada | Esperado |
|---|---|---|
| Ordem | Cart R$ 200,00; 10% e R$ 20,00 cumulativos | 160 (percentual primeiro) e 162 (fixo primeiro), conforme a regra |
| Rateio | R$ 10,00 de desconto entre 3 itens | Soma exata = 10,00 (por exemplo 3,33 + 3,33 + 3,34) |
| Parcelas | R$ 100,00 em 3x | 33,34 + 33,33 + 33,33 (ou a regra escrita); soma = total |
| Frete grátis | Limite R$ 199,00: 198,99 e 199,00; cupom derruba o subtotal | A regra diz se o limite é antes ou depois do desconto |
| Cupom | Expirado; primeira compra reutilizado; item excluído da promoção | Recusa com motivo |
| Adulteração | `total: 1` no corpo | Ignorado; total do servidor |
| Propriedades | Qualquer carrinho gerado | Nenhum líquido negativo; recomputar dá o mesmo resultado |
| Dinheiro em float | `0.1 + 0.2` | Nunca em valor monetário |

Fonte dos casos de ordem, rateio, parcelas e frete grátis: brain-of-agent (MIT, `brains/qa/references/dominios.md`, seções Pagamentos e fintech e E-commerce; Inferido, não reverificado). O caso "juros de 1% a.m. sobre R$ 333,33 por 17 dias" do brain exige a regra de arredondamento do contrato e planilha independente; fora do escopo validado aqui.

## 5. Notas de plataforma

### Medusa (V-38)

- Página de promotion: tipo `standard` no exemplo; campanhas agrupam promoções com datas e orçamento; regras restringem a aplicação; alvos: itens, métodos de envio ou pedido.
- Página de ações: `computeActions` devolve `addItemAdjustment`, `removeItemAdjustment`, `addShippingMethodAdjustment`, `removeShippingMethodAdjustment` e `campaignBudgetExceeded`. Percentual aplica ao **valor restante**. Promoção de pedido (percentual ou fixa) distribui entre os itens proporcionalmente ao valor restante. Promoções `buyget` existem e aplicam **antes** das `standard`.
- Limite de uso por cliente, arredondamento e combinação de promoções: **Não verificados**.

### Shopify Functions (V-38; leitura parcial)

- Alvo `cart.lines.discounts.generate.run`; operação `productDiscountsAdd` com `candidates` (cada um com `targets`, `value` e `message` opcional) e `selectionStrategy` (exemplo `First`); alvo por linha do carrinho (`id`, `quantity` opcional); percentual no exemplo lido.
- Limite de **25 funções de desconto ativas por loja**.
- Valor fixo (`fixedAmount`) e teto de desconto: **Não verificados**. Registre a versão da Admin API (trimestral) e confira a doc dessa versão antes de gerar código.

### Base legal do preço (Decreto 7.962/2013, art. 2º, IV; V-32)

O preço deve discriminar despesas adicionais como entrega e seguros. Requer revisão jurídica; o texto lido do Planalto foi parafraseado.
