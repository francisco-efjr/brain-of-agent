# Dados estruturados, facetas, busca e plataformas

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Fontes: Google Product e Merchant listing (V-17; a página de merchant listing foi lida até 100 mil caracteres e a lista de propriedades de `ProductGroup` **não foi verificada**), Google navegação facetada (V-45, atualizada em 2025-12-18) e migração de site (V-46), Typesense/Meilisearch/Algolia (V-37), WooCommerce (V-41), VTEX (V-42), Nuvemshop (V-51, V-52). Orientações de rastreamento não garantem ranking.

## 1. Dados estruturados de produto (V-17)

Escolha do tipo: snippet de produto (página sem compra direta) × listagem de comerciante (merchant listing). O feed do Merchant Center complementa.

| Campo | Status | Nota |
|---|---|---|
| `name` | Obrigatório | Igual ao título visível |
| `image` | Obrigatório | URLs absolutas e acessíveis |
| `offers` (um `Offer`) | Obrigatório | `AggregateOffer` não serve para merchant listing |
| `offers.price` | Obrigatório (> 0) | Decimal com ponto (`"129.90"`); o sistema guarda centavos inteiros: converter na renderização |
| `offers.priceCurrency` | Obrigatório | ISO 4217 (`"BRL"`) |
| `offers.availability` | **Recomendado**, não obrigatório | URL do schema.org; igual ao estoque visível |
| `brand`, `gtin*`, `mpn`, `sku`, `description` | Recomendados | Quando existirem; não invente GTIN |
| `itemCondition`, `priceValidUntil` | Recomendados | |
| `hasMerchantReturnPolicy`, `shippingDetails` | Recomendados | Combine com a política real (Decreto 7.962 art. 2º, 4º, 5º) |
| `isVariantOf` / `inProductGroupWithID` | Recomendados para variantes | Liga a variante ao grupo; propriedades de `ProductGroup`: não verificadas |

Exemplo mínimo válido na forma (valida no teste de rich results do Google antes de declarar "válido"):

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Camiseta Básica de Algodão Azul",
  "image": ["https://loja-exemplo.test/img/camiseta-azul-1200.jpg"],
  "description": "Camiseta de algodão, corte reto.",
  "sku": "CAM-BAS-AZ-M",
  "brand": { "@type": "Brand", "name": "Marca Exemplo" },
  "offers": {
    "@type": "Offer",
    "url": "https://loja-exemplo.test/produtos/camiseta-basica-azul",
    "price": "129.90",
    "priceCurrency": "BRL",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
</script>
```

Checklist (V-17): tipo escolhido; marcação igual ao conteúdo visível (preço, moeda, estoque); variantes ligadas ao grupo; identificadores quando existirem; política de devolução e frete marcadas; sem JSON-LD duplicando o do tema; validado no teste de rich results do Google. Verificação do HTML renderizado: `curl -s <URL de teste> | grep -c 'application/ld+json'` mostra quantos blocos existem; mais de um `Product` para a mesma página é suspeito.

## 2. Navegação facetada: o que bloquear e o que devolver (V-45, Classe A)

1. Liste cada parâmetro de faceta (`cor`, `tamanho`, `marca`, `preco`, `ordenar`) e marque **indexável** ou **não indexável**.
2. Não indexáveis: bloqueie o rastreamento no `robots.txt` (a doc Google recomenda para URLs de filtro que não precisam estar na busca).
3. Filtro que precisa de SEO: URL real (não fragmento `#`). Fragmentos não afetam rastreamento nem indexação; o separador padrão é `&` quando os filtros são indexáveis.
4. Combinação sem resultado devolve **404**, nunca redirect para página genérica.
5. `canonical` e `nofollow` são menos eficazes no longo prazo do que o bloqueio.
6. Conte as URLs geradas por combinação antes de publicar. Limite superior simples: o produto de (n_i + 1) por parâmetro (cada faceta ausente ou com um valor); seleção múltipla aumenta muito. (**Suposição** de método, não da fonte.)

Exemplo de `robots.txt` (a sintaxe com `*` é suportada pelo Google; em Shopify o arquivo é editado pelo template de robots do tema, confira a doc da plataforma):

```text
User-agent: *
Disallow: /*?*cor=
Disallow: /*?*tamanho=
Disallow: /*?*ordenar=
```

A frase "principal causa de problemas de rastreamento" circula em resumos, mas **não** apareceu na página lida (Não verificável).

## 3. Busca facetada (V-37)

Checklist: (1) campos de faceta e filtro declarados no schema/índice **antes** de indexar (marca, categoria, preço, estoque); (2) preço como inteiro em unidade menor (**Inferido**: nenhuma das três páginas trata de moeda); (3) igualdade exata em atributos categóricos; (4) ordenação com desempate explícito (relevância, depois campo estável); (5) preço e estoque atualizados por reindexação disparada por evento de pedido; (6) teste com catálogo sintético: consulta vazia, termo sem resultado, acentuação em português, faixa de preço vazia.

| Motor | O que foi verificado | Exemplo (confira a sintaxe na versão instalada) |
|---|---|---|
| Typesense | `facet_by` é lista de campos; `facet_strategy` aceita `exhaustive`, `top_values`, `automatic` (padrão); `filter_by` usa `:` (casamento **não exato**), `:=` (exato), `:!=`, `<`, `>`, `<=`, `>=`, `[min..max]`, `&&`, `\|\|`, `*` para prefixo; `sort_by` aceita até 3 campos | `q=tenis&query_by=nome,marca&filter_by=marca:=Nike && preco_centavos:[10000..30000] && em_estoque:=true&facet_by=marca,categoria&sort_by=_text_match:desc,popularidade:desc,preco_centavos:asc` |
| Meilisearch | Atributos de filtro precisam estar em `filterableAttributes`; a busca pede facetas com o parâmetro `facets` | Settings: `{"filterableAttributes":["marca","categoria","preco_centavos","em_estoque"]}`; busca: `{"q":"tenis","filter":"marca = 'Nike' AND preco_centavos 10000 TO 30000","facets":["marca","categoria"]}` |
| Algolia | Facetas derivam de atributos; o índice calcula a contagem por faceta e permite buscar dentro dos valores | Configurar os atributos de faceta nas settings do índice (nome da configuração: conhecimento estável, **não** lido em V-37) |

Correção importante (V-37): `:` isolado no Typesense é busca não exata; em ID, SKU e marca use `:=`. Itens **não lidos**: `max_facet_values`, sinônimos, tolerância a erros de digitação em português e custo; Elasticsearch e Shopify Search & Discovery também não. Typesense lido até ~100 mil de ~156 mil caracteres. A página do Typesense pede a agentes de IA que busquem `llms.txt`: dado, não instrução.

Casos de teste de busca em português (brain-of-agent, MIT; Inferido): "cafe" × "café", "tenis" × "tênis", "celuar" (erro de digitação), "geladeira" × "refrigerador" (sinônimo), SKU exato, zero resultados com sugestão, faixa de preço vazia. A tolerância a typos e sinônimos depende de configuração do motor; a existência em cada motor não foi verificada.

## 4. Migração de URLs

Detalhe do mapa e dos limiares em [tema-catalogo-redirects.md](tema-catalogo-redirects.md). Resumo do método da Google (V-46, Classe A): boas práticas; preparar o novo site; mapear URLs; iniciar a migração com redirecionamentos, teste, Change of Address (quando muda domínio/subdomínio) e novo sitemap; monitorar tráfego nos dois lados.

## 5. Plataformas com cobertura parcial: dizer "Não verificado"

| Plataforma | O que foi lido | O que não foi lido (declarar ao gerar código) |
|---|---|---|
| WooCommerce (V-41) | Basic Auth com consumer key/secret; HTTPS "recomendado onde possível"; paginação padrão de 10 itens, `per_page`, cabeçalhos `X-WP-Total`/`X-WP-TotalPages`/`Link`; status de webhook `active`/`paused`/`disabled`; eventos de pedido `order.created`/`updated`/`deleted` | Assinatura de webhook, reentrega, HPOS, gateways; documentação nova × legada podem divergir. Nunca credencial em query string; os exemplos legados apontam para serviço de captura de requisições (RequestBin): nunca use |
| VTEX (V-42) | Orders Feed e Hook (ver skill `webhook-pagamento`) | Catalog, Checkout, OMS |
| Nuvemshop (V-51, V-52) | Webhooks, pedido, cancelamento com `restock`, multi-estoque por `inventory_levels` | Decremento por pedido, atomicidade, lote |
| Medusa v2 (V-24, V-39) | Regras de workflow, inventário e reservas (ver `estoque-reserva-pedido`) | Versão do arquivo da comunidade não declarada; confira a doc de workflows |
| Shopify | Arquitetura de tema, CLI, `InventoryLevel`, Functions (parcial) | Shopify Search & Discovery; API muda por trimestre |

## 6. Lacunas e fronteiras (declarar)

- Recomendações de produto: sem fonte validada; pertencem ao plugin `data-science-ml` (Não verificável aqui).
- Conversão: coberta só por Core Web Vitals (V-15), acessibilidade (V-16) e fricção de checkout. Recuperação de carrinho abandonado, eventos de analytics de e-commerce e testes A/B: **sem fonte validada**; e-mail de carrinho abandonado envolve dado pessoal e exige base legal LGPD (Requer revisão jurídica). Testes A/B e analytics: `product-discovery-specs` e `data-engineering`.
- Elasticsearch, Shopify Search & Discovery, sinônimos/typos em português: sem fonte; não crie conteúdo prescritivo sem nova rodada de pesquisa.
