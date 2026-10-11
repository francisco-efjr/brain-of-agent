# Tema Shopify, armadilhas de catálogo e redirects

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Fontes: Shopify theme architecture e CLI (V-14, B7/B6, lidas), regra comunitária de tema (awesome-cursorrules, CC0 no repositório, 80 linhas; só o padrão), `awesome-ecom-skills` (MIT) e `shopify-admin-skills` (MIT) via V-19 e V-44. Versão da API da Shopify é trimestral: registre-a e confira a doc.

## 1. Estrutura oficial do tema (Verificado, V-14)

Único arquivo obrigatório: `layout/theme.liquid`. Pastas: `assets`, `blocks` (aparece só na árvore da página), `config`, `layout`, `locales`, `sections`, `snippets`, `templates`. Templates JSON são apenas invólucro de seções; templates Liquid contêm código. Snippets são invisíveis ao lojista no editor. `.shopifyignore` na raiz. O nome do comando de publicação não aparece na página lida (não escreva de memória).

## 2. Checklist de revisão de tema (12 itens, com motivo)

| # | Verificar | Motivo | Detecção |
|---|---|---|---|
| 1 | Estrutura de pastas confere com a doc oficial | Editor e CLI dependem dela | `ls` da árvore do tema |
| 2 | `render` em vez de `include` | `include` é legado; `render` isola escopo | Buscar `{% include` |
| 3 | Sem loops aninhados pesados ou acessos repetidos a objetos custosos | Liquid não acessa banco; custo vem de varrer coleções. A regra da fonte diz só "limitar consultas em loops" (Inferido) | Buscar `{% for` dentro de `{% for` |
| 4 | Seções com `schema`, presets e blocos | Lojista edita sem código | Buscar `{% schema %}` ausente |
| 5 | Template JSON para o que o lojista edita; Liquid para lógica | Separação de responsabilidades | Listar `templates/` |
| 6 | Snippets só para reuso interno | Não aparecem no editor | Revisar `snippets/` |
| 7 | Imagens com `image_url`, dimensões e carregamento preguiçoso fora da dobra | LCP e CLS | Buscar `<img` sem `width`/`height`/`loading` |
| 8 | JS/CSS minificados e sem bloqueio de renderização | LCP e INP | Buscar `<script src=` sem `defer`/`async` |
| 9 | Teclado, foco visível, `alt` significativo | WCAG 2.4.7, 1.1.1 | Buscar `outline: none`, `alt=""` em produto |
| 10 | Contraste adequado | WCAG 1.4.3 | Ferramenta de contraste |
| 11 | Theme Check sem erros | Lint oficial do tema | Comando do Shopify CLI sob permissão do usuário |
| 12 | Lighthouse em laboratório e Core Web Vitals de campo | Regressão × realidade | Relatar a fonte do número |

Regra de segurança: trabalhar em tema de desenvolvimento ou loja de teste; nunca `push` no tema publicado nem publicar sem aprovação humana.

Trechos Liquid corretos para os itens 2 e 7:

```liquid
{%- comment -%} item 2: render isola variáveis; passe o que o snippet precisa {%- endcomment -%}
{% render 'product-card', product: product, mostrar_preco: true %}

{%- comment -%} item 7: image_url com largura e image_tag com loading lazy (fora da dobra) {%- endcomment -%}
{{ product.featured_image | image_url: width: 600 | image_tag: loading: 'lazy', widths: '300, 600', sizes: '(min-width: 750px) 25vw, 50vw', alt: product.featured_image.alt }}
```

Para a primeira imagem visível (candidata a LCP) use `loading: 'eager'` e `fetchpriority: 'high'`; `lazy` na primeira imagem piora o LCP. Confira os parâmetros do filtro `image_tag` na doc do Liquid da sua versão.

## 3. Armadilhas de dados de catálogo (V-19, 6 pontos)

| # | Armadilha | Consequência | Defesa |
|---|---|---|---|
| 1 | Célula em branco no CSV (Matrixify) | Pode apagar o metafield | Validar colunas vazias antes; contagem prévia; backup |
| 2 | Backfill de SEO sobrescrevendo texto humano | Perda de conteúdo editado | Preencher só o que falta |
| 3 | Redirecionamento que cai na home silenciosamente | Perda de relevância e UX ruim | Sem fallback para a home; revisão humana |
| 4 | JSON-LD que duplica o `Product` do tema | Rich result inelegível/ambíguo | Um bloco só; complementar |
| 5 | Storefront com cache de CDN | Leitura mostra estado antigo | Ler pela Admin API |
| 6 | ID de categoria adivinhado | Produtos em categoria errada | Verificar na fonte |

Toda importação, limpeza de SEO ou migração começa com contagem prévia e backup/exportação (gate da skill `loja-operacao-segura`).

## 4. Auditoria de catálogo somente leitura (modelo `shopify-catalog-audit`, V-44)

Padrão aproveitável do modelo de auditoria: escopo de leitura (`read_products`), nunca mutar, verificação pela Admin API e não pelo sitemap, "justificar ou descartar" cada achado, declarar o que não foi indexado. Relatório: severidade, evidência, correção e "não examinado".

## 5. Mapeamento de redirecionamentos (V-44, V-46, V-19)

Fonte do padrão: `shopify-redirect-mapping` (V-44, MIT) e Google site move (V-46). Limiares e baldes abaixo vêm do V-44; a semântica fina de cada balde não foi relida: ponto de partida, ajuste com amostra (**Inferido**).

1. **Fontes do mapa antigo -> novo (pelo menos três):** sitemaps enviados, logs e analytics, relatório "links para seu site" do Search Console, CMS, recursos embutidos (imagens, vídeos, JS, CSS).
2. **Casamento com limiar por tipo:** produto >= 0,85 e coleção >= 0,70 de similaridade/confiança; sem casamento acima do limiar, o item não vira redirect automático.
3. **Três baldes:** aplicar, revisar (humano) e pular. Orçamento de 2 a 3 rodadas de revisão. **Nunca** destino padrão na home.
4. **Backup dos redirecionamentos existentes** antes de escrever; releitura pela API depois; `curl -I` para conferir o 301.
5. **Cadeias:** 301 direto ao destino final; se houver cadeia, idealmente até 3 saltos e menos de 5; o Googlebot segue até 10 (Verificado, V-46).
6. **Retenção:** manter por pelo menos 1 ano (a página sugere manter indefinidamente para o usuário). 301 e outros permanentes não causam perda de PageRank (Verificado).
7. **Troca de domínio ou subdomínio:** Change of Address no Search Console, enviar o novo sitemap, guardar os dois sitemaps (avisos de redirect no sitemap antigo são normais).
8. **Monitoramento:** indexação, erros de rastreamento e tráfego nas duas bases; janela de 90 dias é **Suposição** do pesquisador.

Formato do CSV de mapa (colunas):

```csv
url_antiga,url_nova,tipo,confianca,balde,fonte_da_url_antiga,observacao
/produtos/camiseta-azul-p,/products/camiseta-basica-azul,produto,0.93,aplicar,sitemap,
/colecao/verao-2024,/collections/verao,colecao,0.74,aplicar,analytics,
/colecao/promocao-relampago,,colecao,0.41,revisar,logs,sem equivalente claro: decisão humana
```

Conferência pós-escrita (amostra; roda contra o ambiente de teste ou, após aprovação, contra a loja):

```bash
curl -sI "https://loja-de-teste.example/produtos/camiseta-azul-p" | grep -iE '^(HTTP|location)'
# esperado: HTTP/2 301 e location: https://loja-de-teste.example/products/camiseta-basica-azul
```

Contagem de destinos na home (deve ser zero):

```bash
awk -F, 'NR>1 && ($2=="/" || $2=="") && $5=="aplicar"' mapa-redirects.csv | wc -l
```
