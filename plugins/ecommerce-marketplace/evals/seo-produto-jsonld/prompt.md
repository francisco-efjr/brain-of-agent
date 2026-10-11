---
name: seo-produto-jsonld
description: "Caso de disparo de catálogo e SEO de produto. JSON-LD com AggregateOffer e sem moeda numa página de produto Shopify cujo tema já injeta outro Product. Mede Offer com price e priceCurrency, availability como recomendada (não obrigatória), evitar JSON-LD duplicado, variantes ligadas ao grupo, marcação igual ao conteúdo visível e validação no teste de rich results antes de declarar válido."
tags: [ecommerce-marketplace, catalogo-busca-seo, structured-data, shopify, json-ld]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Exige um Offer com price maior que zero e priceCurrency, diz que availability é recomendada e não obrigatória, evita duplicar o JSON-LD do tema, liga variantes ao grupo, mantém a marcação igual ao conteúdo visível e pede validação no teste de rich results, sem declarar o resultado válido nem alterar a loja ao vivo."
model: sonnet
---
Minha página de produto na Shopify tem este JSON-LD, que um app de SEO me ajudou a montar, mas o Google reclama de oferta e o tema já injeta o próprio schema de produto também. Ajusta pra eu corrigir. O produto tem 4 variantes (tamanhos P, M, G e GG, cada uma com seu SKU, preço igual de R$ 129,90, e o GG está sem estoque).

```liquid
{%- comment -%} snippets/seo-product-schema.liquid (criado pelo app de SEO) {%- endcomment -%}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": {{ product.title | json }},
  "image": {{ product.featured_image | image_url: width: 1200 | json }},
  "description": {{ product.description | strip_html | json }},
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": "{{ product.price_min | money_without_currency }}",
    "highPrice": "{{ product.price_max | money_without_currency }}",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

O tema (Dawn modificado) já tem um bloco `Product` em `sections/main-product.liquid`, na linha 210 mais ou menos. Não quero mexer na loja ao vivo agora, só saber o que mudar e depois eu aplico num tema de desenvolvimento.
