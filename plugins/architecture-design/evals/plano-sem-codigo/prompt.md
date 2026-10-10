---
name: plano-sem-codigo
description: Mede se o plugin produz pesquisa e plano de extração com arquivo:linha, alternativas, rollback e decisões pendentes, sem implementar antes da aprovação, e sugere o fluxo com gates quando a skill manual é a mais adequada.
tags: [architecture-design, planning, decomposition, gates]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 900
runs: 3
expected_outcome: "Entrega pesquisa e plano de extração do módulo de faturamento citando arquivo:linha dos trechos fornecidos, com alternativas incluindo não mudar nada, rollback, critérios por fase e decisões pendentes, sem editar código, pedindo aprovação e sugerindo o comando manual com gates."
model: sonnet
---
Quero extrair o módulo de faturamento (`app/billing`) do nosso monólito Rails para um serviço próprio. Pesquise o código e me dê um plano; só implemente depois que eu aprovar.

Não estou com o repositório montado aqui, então colo os trechos que importam (o número à esquerda é a linha do arquivo):

```ruby
# app/billing/invoice_service.rb
 8  class InvoiceService
 9    def create_for(order)
10      invoice = Invoice.create!(order_id: order.id, total: order.total_cents)
11      PaymentGateway.charge(invoice)        # chamada HTTP síncrona ao PSP
12      order.update!(status: "invoiced")     # escreve na tabela do módulo orders
13      invoice
14    end

# app/orders/checkout.rb
31  InvoiceService.new.create_for(order)     # dentro da transação do checkout
32  Mailer.order_confirmed(order).deliver_later

# app/reports/revenue_report.rb
 5  Invoice.joins(:order).where(created_at: range)   # lê invoices e orders direto
```

Do `db/schema.rb`: `invoices.order_id` é FK para `orders.id`; `payments.invoice_id` é FK para `invoices.id`. Time de 4 devs, 2 deploys por semana, sem testes de arquitetura.
