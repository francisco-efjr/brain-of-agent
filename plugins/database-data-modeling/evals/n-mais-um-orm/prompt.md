---
name: n-mais-um-orm
description: "Mede se o plugin reconhece N+1 de ORM em uma view Django lenta, propõe select_related e prefetch_related e pede a contagem de consultas antes e depois, sem exigir EXPLAIN nem prometer ganho."
tags: [database-data-modeling, query-plan-and-indexing, orm, n-plus-one]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica o padrão N+1 (1 consulta de pedidos mais uma por cliente e uma por conjunto de itens), propõe select_related para customer e prefetch_related para items, pede a contagem de consultas antes e depois e trata o ganho como suposição."
model: sonnet
---
A tela de pedidos em aberto do nosso painel (Django 4.2, Postgres 15) demora uns 3 segundos para carregar 200 pedidos. Suspeito de banco, mas não sei por onde começar. A view:

```python
def pedidos_abertos(request):
    pedidos = Order.objects.filter(status="open").order_by("-created_at")[:200]
    data = []
    for o in pedidos:
        data.append({
            "id": o.id,
            "cliente": o.customer.name,
            "itens": [i.sku for i in o.items.all()],
        })
    return JsonResponse(data, safe=False)
```

Os modelos têm `Order.customer = ForeignKey(Customer)` e `OrderItem.order = ForeignKey(Order, related_name="items")`. Tem como acelerar?
