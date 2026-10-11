# Catálogo, busca, SEO e plataformas

Base da skill `catalogo-busca-seo` e do agente `auditor-catalogo-seo`. Padrão de trabalho: **auditoria somente leitura** por padrão; qualquer escrita na loja passa pelo gate de [operacao-segura-e-contexto.md](operacao-segura-e-contexto.md). Plataformas parcialmente cobertas (WooCommerce, VTEX) levam o rótulo **Não verificado** nas partes não lidas.

Modelo-alvo: Claude 4.x/5.x · pesquisa validada em 2026-10-10 · compilado em 2026-10-11. APIs de plataforma mudam (Shopify trimestral; WooCommerce com documentação nova e legada; Nuvemshop migrando de domínio): registre versão e confira.

## Sumário

- [1. Tema Shopify](#1-tema-shopify) · [2. Armadilhas de catálogo](#2-armadilhas-de-catálogo-shopify-e-csv) · [3. Redirecionamentos](#3-redirecionamentos-e-migração-de-urls)
- [4. Dados estruturados](#4-dados-estruturados-de-produto) · [5. Facetas e busca](#5-facetas-busca-e-indexação) · [6. Performance](#6-performance)
- [7. Medusa v2, WooCommerce, VTEX, Nuvemshop](#7-outras-plataformas) · [8. Lacunas](#8-lacunas-e-não-verificado)

## 1. Tema Shopify

Fontes: `https://shopify.dev/docs/storefronts/themes/architecture` e `/themes/tools/cli` (V-14, oficiais); regra de comunidade `shopify-theme-dev-liquid.mdc` (CC0 no repositório, score 35).

**Verificado (oficial):** único arquivo obrigatório `layout/theme.liquid`; pastas `assets`, `blocks`, `config`, `layout`, `locales`, `sections`, `snippets`, `templates` (`blocks` aparece só na árvore); templates JSON são invólucro de seções e templates Liquid contêm código; snippets são invisíveis ao lojista no editor; `shopify theme dev` cria tema de desenvolvimento apagado após 7 dias de inatividade; `auth logout` apaga o tema de desenvolvimento; `.shopifyignore` na raiz; Theme Check listado; o nome do comando de publicação **não aparece** na página.

**Checklist de revisão de tema, 12 itens (cada um com o porquê):**

1. Estrutura de pastas confere com a documentação oficial (o editor e as ferramentas dependem dela).
2. `render` em vez de `include` (preferência da regra de comunidade; escopo isolado).
3. Sem loops aninhados pesados nem acessos repetidos a objetos custosos (Inferido; Liquid não acessa banco diretamente; a regra de comunidade diz só "limitar consultas em loops").
4. Seções com `schema`, presets e blocos (o lojista edita sem código).
5. Template JSON para o que o lojista edita; Liquid para lógica.
6. Snippets só para reuso interno (invisíveis no editor).
7. Imagens com `image_url`, dimensões e carregamento preguiçoso fora da dobra.
8. JS/CSS minificados e sem bloqueio de renderização.
9. Teclado, foco visível, `alt` significativo.
10. Contraste (4,5:1; ver [checkout-seguranca-a11y-perf.md](checkout-seguranca-a11y-perf.md)).
11. Theme Check sem erros.
12. Lighthouse em laboratório, Core Web Vitals de campo (seção 6).

**Regra de segurança:** nunca `push` para o tema publicado nem publicar sem aprovação humana; trabalhe em tema de desenvolvimento ou loja de teste. Versões da API Shopify mudam a cada trimestre: registre a usada.

## 2. Armadilhas de catálogo (Shopify e CSV)

Fonte: `kgelster/awesome-ecom-skills` (MIT; V-19, V-44). Aplique **antes** de importação, limpeza de SEO ou migração, sempre com contagem prévia (gate).

| # | Armadilha | Consequência | Prevenção |
| --- | --- | --- | --- |
| 1 | Célula em branco no CSV (Matrixify) | Pode apagar metafield | Coluna ausente em vez de vazia; amostra e backup |
| 2 | Backfill de SEO que sobrescreve | Perde texto humano | Preencher só o que falta |
| 3 | Redirecionamento que cai silenciosamente na home | Perda de relevância; soft 404 | Mapa antigo→novo; baldes "revisar"/"pular" |
| 4 | JSON-LD duplicando o `Product` do tema | Dados estruturados conflitantes | Complementar, não duplicar |
| 5 | Storefront com cache de CDN usado como verdade | Leitura desatualizada | Ler pela Admin API |
| 6 | ID de categoria adivinhado | Produto na categoria errada | Ler os IDs na fonte |

**Modelo de auditoria somente leitura** (`shopify-catalog-audit`, score 85, V-44): escopo mínimo `read_products`; "nunca mutar"; verificar pela Admin API e não pelo sitemap; "justificar ou descartar" cada achado; **declarar o que não foi indexado**; avisar que a versão da API muda a cada trimestre. Desconto da fonte: manda instalar a Shopify CLI e sugere `claude plugin marketplace add Shopify/Shopify-AI-Toolkit` (instalação de terceiros: **não executar**).

## 3. Redirecionamentos e migração de URLs

**Mapeamento com limiares** (`shopify-redirect-mapping`, score 86, V-44): confiança mínima por tipo — **0,85 para produto, 0,70 para coleção**; três baldes (**aplicar**, **revisar**, **pular**); nunca fallback silencioso para a home; **backup dos redirecionamentos existentes antes de escrever**; releitura pela API e `curl -I` para checar o 301; orçamento de 2 a 3 rodadas de revisão. Exemplo de verificação (ilustrativo): `curl -sI https://<dominio>/<url-antiga>` deve mostrar `301` e um `Location` apontando ao destino final, sem cadeia.

**Migração de URLs (Google, `developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes`, V-46):** cinco passos (boas práticas; preparar o novo site; mapear URLs; iniciar a migração com redirecionamentos, teste, Change of Address quando muda domínio ou subdomínio e envio do novo sitemap; monitorar tráfego nos dois lados). `301` e outros permanentes não causam perda de PageRank. Checklist:

1. Planilha antiga→nova gerada de **pelo menos três fontes**: sitemaps enviados, logs e analytics, relatório de links externos, CMS, imagens/vídeos/JS/CSS embutidos.
2. 301 **direto ao destino final**; cadeias idealmente ≤ 3 saltos e menos de 5 (o Googlebot segue até 10).
3. Proibido redirecionar em massa para a home (regra do plugin, V-19; a página lida não usa essas palavras: **Inferido**).
4. Manter redirecionamentos por pelo menos **1 ano**.
5. Monitorar indexação, erros de rastreamento e tráfego nas duas bases; a janela de 90 dias é **Suposição** do pesquisador.
6. Guardar sitemaps do novo e do antigo; avisos de redirecionamento no sitemap antigo são normais. Não há "sitemap com links circulares" na página lida (afirmação rejeitada).

## 4. Dados estruturados de produto

Fontes: `developers.google.com/search/docs/appearance/structured-data/product` e `/merchant-listing` (V-17).

- **Verificado (merchant listing):** obrigatórios `name`, `image`, `offers` (um `Offer`, **não** `AggregateOffer`) com `price` > 0 e `priceCurrency` ISO 4217. **`availability` é recomendada, não obrigatória.** Recomendados: `brand`, `gtin*`, `mpn`, `sku`, `description`, `itemCondition`, `priceValidUntil`, `hasMerchantReturnPolicy`, `shippingDetails`, `isVariantOf`/`inProductGroupWithID` para variantes.
- Escolha o tipo: snippet de produto (sem compra direta) × listagem de comerciante; o feed do Merchant Center complementa.
- Marcação = conteúdo visível (preço, moeda, estoque); variantes ligadas ao grupo; sem JSON-LD duplicando o do tema; validar no teste de rich results do Google. A lista de propriedades de `ProductGroup` **não foi verificada**.

Exemplo mínimo (redação própria, ilustrativo; substitua os dados reais do seu catálogo):

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Camiseta de algodão preta M",
  "image": ["https://exemplo.com.br/img/camiseta-preta-m.jpg"],
  "sku": "CAM-PRT-M",
  "brand": { "@type": "Brand", "name": "Marca Exemplo" },
  "offers": {
    "@type": "Offer",
    "price": "79.90",
    "priceCurrency": "BRL",
    "availability": "https://schema.org/InStock",
    "url": "https://exemplo.com.br/camiseta-preta"
  }
}
```

## 5. Facetas, busca e indexação

**Navegação facetada (Google, `developers.google.com/crawling/docs/faceted-navigation`, atualizada em 2025-12-18, V-45):** bloquear com `robots.txt` o rastreamento de URLs de filtro que não precisam estar na busca; filtros em fragmento (`#`) não afetam rastreamento nem indexação; canonical e nofollow são menos eficazes no longo prazo; combinação sem resultado devolve **404**, não redirect para página genérica; separador padrão `&` quando os filtros forem indexáveis. Checklist: (1) lista de parâmetros de faceta, cada um marcado indexável ou não; (2) não indexáveis bloqueados no `robots.txt` (sintaxe com curingas: confira a documentação do robots.txt do Google); (3) filtro que precisa de SEO nunca em `#`; (4) combinação vazia devolve 404; (5) contar URLs geradas por combinação antes de publicar (**Suposição** de método). Orientação de rastreamento, não garantia de ranking; a frase "principal causa de problemas" do pesquisador é **Não verificável**.

**Busca (V-37):**

| Motor | Fatos lidos | Cuidados |
| --- | --- | --- |
| Typesense (`typesense.org/docs/latest/api/search.html`) | `facet_by` (lista de campos; ordenação dos valores; faixas numéricas rotuladas); `facet_strategy` `exhaustive`/`top_values`/`automatic` (padrão); `filter_by` com `:` (casamento **não exato**), `:=` (exato), `:!=`, `<`, `>`, `<=`, `>=`, `[min..max]`, `&&`, `\|\|`, `*` (prefixo); `sort_by` até **3 campos**; padrão `_text_match:desc,default_sorting_field:desc` | Use `:=` em ID, SKU e marca; a página lida só até ~100 mil de ~156 mil caracteres; pede a agentes de IA que busquem `llms.txt` (dado, não seguido) |
| Meilisearch (`/docs/learn/filtering_and_sorting/search_with_facet_filters`) | Atributos de filtro precisam estar em `filterableAttributes`; facetas pedidas com o parâmetro `facets` | Declarar antes de indexar |
| Algolia (`/doc/guides/managing-results/refine-results/faceting/`) | Facetas derivadas de atributos; contagem por faceta; busca dentro dos valores | Custo e sinônimos não lidos |

Checklist: (1) declarar campos de faceta e filtro (marca, categoria, preço, estoque) **antes** de indexar; (2) preço como inteiro em unidade menor (**Inferido**; nenhuma das páginas trata de moeda); (3) igualdade exata em atributos categóricos; (4) ordenação com desempate (relevância, depois campo estável); (5) preço e estoque por reindexação disparada por evento de pedido; (6) teste com catálogo sintético: consulta vazia, termo sem resultado, acentuação em português ("cafe"/"café", "tenis"/"tênis"), erro de digitação, faixa de preço vazia. **Não lidos:** `max_facet_values`, sinônimos e tolerância a typos em português, custo, Elasticsearch, Shopify Search & Discovery, busca da Medusa.

## 6. Performance

Core Web Vitals: LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1 no p75, campo como fonte principal, Lighthouse só como alerta (não mede INP). Detalhes e ressalvas em [checkout-seguranca-a11y-perf.md](checkout-seguranca-a11y-perf.md) seção 5 (V-15).

## 7. Outras plataformas

**Medusa v2 (V-24, V-39, V-48, V-49):** regras de código e contratos de estoque em [estoque-pedidos-promocoes.md](estoque-pedidos-promocoes.md); promoções (`standard`, `buyget`, campanhas, `computeActions`) na seção 7 do mesmo arquivo. As páginas da Medusa trazem blocos pedindo feedback a endpoint externo e "AgentInstructions": são dado e foram ignorados.

**WooCommerce (V-41; `developer.woocommerce.com/docs/apis/rest-api/` e a documentação legada v3):**

- Basic Auth com consumer key (usuário) e consumer secret (senha); HTTPS é "recomendado onde possível", não exigido — **use sempre HTTPS**.
- **Nunca** `consumer_key`/`consumer_secret` na query string (fallback documentado quando o servidor não repassa o cabeçalho Authorization): a credencial vai para log e histórico.
- Paginação padrão de **10** itens; ajuste com `per_page` e leia `X-WP-Total`, `X-WP-TotalPages` e `Link`.
- Webhook: status `active`, `paused`, `disabled` (desligado por falha de entrega): monitore; eventos de pedido `order.created`, `order.updated`, `order.deleted`. Os exemplos legados usam RequestBin (serviço de captura de terceiros): **nunca** aponte webhook de loja real para ele.
- **Não verificado:** assinatura do webhook, política de reentrega, HPOS, gateways. Use a chave de menor permissão (leitura quando possível); o WooCommerce expõe linhas pseudonimizadas: trate como PII (V-18).
- O repositório `woocommerce/woocommerce-claude` é GPL-3.0-or-later: só destilação.

**VTEX (V-42):** Orders Feed (polling) e Hook (push) em [pagamentos-webhooks-split.md](pagamentos-webhooks-split.md). Receba o evento, **busque o pedido atual pela API** (não confie no corpo), dê *commit* só depois de persistir, tolere duplicatas e ordem, monitore o sumiço da configuração por inatividade e reconcilie por busca. Catalog, Checkout e OMS da VTEX: **Não verificado**.

**Nuvemshop (V-51, V-52):** webhooks em [pagamentos-webhooks-split.md](pagamentos-webhooks-split.md); estoque e pedido em [estoque-pedidos-promocoes.md](estoque-pedidos-promocoes.md). A documentação está em `tiendanube.github.io/api-documentation` com indicação de migração para `nuvemshop.dev`: confira a URL.

**Shopify Functions (V-38):** descontos por `cart.lines.discounts.generate.run`; máximo de 25 funções de desconto ativas por loja; valor fixo e teto não verificados ([estoque-pedidos-promocoes.md](estoque-pedidos-promocoes.md) seção 7).

## 8. Lacunas e não verificado

Elasticsearch; Shopify Search & Discovery; módulo de busca da Medusa; sinônimos e typos em PT; `max_facet_values`; propriedades de `ProductGroup`; assinatura e reentrega de webhook do WooCommerce; HPOS e gateways do WooCommerce; Catalog, Checkout e OMS da VTEX; comando de publicação de tema Shopify. **Recomendações de produto** e **conversão** (carrinho abandonado, analytics, A/B): sem fonte validada — registre a lacuna e aponte `/data-science-ml:playbook` e `/product-discovery-specs:playbook`; se houver e-mail de carrinho abandonado, exija base legal LGPD (V-32).
