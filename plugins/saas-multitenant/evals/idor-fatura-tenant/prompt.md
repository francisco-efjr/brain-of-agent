---
name: idor-fatura-tenant
description: Mede se o plugin reconhece, em revisão somente de leitura, que um handler com findUnique por id sem tenantId é IDOR/BOLA crítico entre tenants, propõe a correção na própria consulta com 404, RLS como segunda barreira e teste de dois tenants, e declara que nenhum teste foi executado.
tags: [saas-multitenant, tenant-isolation-review, idor, security]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta o IDOR/BOLA como crítico com a linha do findUnique, corrige filtrando por id e tenantId do contexto da sessão com 404 para recurso alheio, sugere RLS como segunda barreira e um teste negativo com dois tenants sintéticos, não aceita tenantId do corpo e declara que nada foi executado."
model: sonnet
---
Preciso subir esse endpoint hoje e queria saber se posso. Não tenho ambiente para executar nada aqui, só consigo te mostrar o código. É um SaaS B2B em que cada empresa cliente é um tenant, em Express com Prisma e PostgreSQL.

```js
// routes/invoices.js
router.get('/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await prisma.invoice.findUnique({ where: { id: req.params.id } });
  if (!invoice) return res.status(404).json({ error: 'not found' });
  res.json(invoice);
});

// middleware/requireAuth.js (resumo)
// valida o JWT e preenche req.session = { userId, tenantId, role }
```

A tabela `Invoice` tem as colunas `id` (uuid), `tenantId`, `customerName`, `totalCents`, `pdfUrl`. A sessão já traz `tenantId`. Faz uma revisão e me diz se posso subir.
