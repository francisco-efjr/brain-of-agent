# Actors para pesquisa

Validade: dados de 2026-10-13, lidos na API pública da Store (`https://api.apify.com/v2/acts/<owner>~<name>` e `/builds/default`) e na página do crawler. **Selo: volátil.** Todo preço e todo schema podem mudar: confirme **no dia** com `fetch-actor-details` (devolve o preço do seu tier) antes de planejar e de executar. Nenhum Actor foi executado.

Rótulos: Verificado (lido na API pública na data) · Inferido · Suposição · Não verificável. Popularidade (usuários, runs) é sinal, não prova de qualidade.

Sumário: 1. Antes de usar um Actor: árvore fonte → rota · 2. Tabela de Actors recomendados · 3. Entradas mínimas com limites · 4. Critérios de escolha · 5. Actors fora do fluxo ou inexistentes · 6. O que descartar sempre · 7. Exemplo resolvido ponta a ponta · 8. Molde para os outros Actors

## 1. Antes de usar um Actor: árvore fonte → rota (V-22)

Cada run é cobrada. Use a rota mais barata que resolve:

| Fonte do dado | Rota | Por quê |
| --- | --- | --- |
| GitHub | `gh api` ou `api.github.com` via WebFetch | Gratuito, estruturado, com estrelas, licença e `pushed_at` |
| Hacker News | API Algolia (`hn.algolia.com/api/v1/search`) | JSON público sem custo (conferido: posts de `mcpc` e `mcp2cli`) |
| dev.to | `dev.to/api/articles` | API pública; muitos posts são anúncios de Actors próprios: sinal fraco |
| Documentação e páginas estáticas | WebFetch | Basta; Apify só se o WebFetch falhar por bloqueio ou JavaScript |
| Fato sobre o próprio Apify, a API ou o Crawlee | `search-apify-docs` / `fetch-apify-docs` (skill `consultar-docs-apify`) | Gratuito, sem login |
| Reddit | **Apify** (o WebFetch do Claude Code recusa reddit.com: "Claude Code is unable to fetch from www.reddit.com") | Caso de uso mais forte |
| X (Twitter) | Apify | Sem API gratuita equivalente |
| Transcrição de YouTube | Apify | |
| SERP estruturada | Apify (`google-search-scraper`) | |
| Crawl de documentação com JavaScript | Apify (`website-content-crawler`), só com humano no loop | Usage-based: sem teto em dólares |
| URL única bloqueada ou que exige JavaScript | WebFetch primeiro; senão `apify/web-fetch` | |

Actors de Hacker News e GitHub (`epctex/hackernews-scraper`, `cloud9_ai/github-scraper`) só como último recurso: use a API Algolia e o `gh api`.

## 2. Tabela de Actors recomendados (2026-10-13, faixa FREE, preços voláteis)

Todos têm `actorPermissionLevel: LIMITED_PERMISSIONS` e `isDeprecated: false`. A página da Store mostra "a partir de" = tier GOLD; a faixa FREE paga mais; BRONZE a DIAMOND são mais baratos (mapeamento plano para tier não verificado).

| ID (existe, Verificado) | Uso | Preço PPE (FREE) | Mantenedor · usuários · mudança de preço |
| --- | --- | --- | --- |
| `apify/rag-web-browser` | Busca Google e conteúdo em Markdown; aceita URL | search 0,00348 · fetch 0,00228/página · start 0,000225/GB | Apify oficial · 192 226 · desde 2026-10-02 |
| `apify/web-fetch` | URL para Markdown, texto, HTML ou links, com JavaScript e anti-bot | fetch 0,0015 (GOLD+ 0,001) · start 0,00005 fixo | Apify oficial · 27 252 · desde 2026-09-10 |
| `apify/google-search-scraper` | SERP estruturada | search-page 0,0045/página · start 0,00005 · **add-ons de IA 0,20 cada; lead 0,10; AI Overview 0,003; website-content 0,008** (desligados por padrão: mantenha); `minimalMaxTotalChargeUsd` 0,5 | Apify oficial · 202 967 · desde 2026-10-07 (27 versões de preço) |
| `apify/website-content-crawler` | Crawl de docs e sites para Markdown | sem eventos PPE: uso de plataforma (CU 0,20 a 0,25; o autor estima US$ 0,5 a 5 por 1 000 páginas com navegador e 0,2 com HTTP) | Apify oficial · 167 831 · **sem teto USD verificável** |
| `trudax/reddit-scraper-lite` | Posts e comentários do Reddit | result 0,004 (GOLD 0,0034) · **actor-start-gb 0,02 por GB (2 GB padrão = 0,04)**; `minimalMaxTotalChargeUsd` 0,04 | Terceiro (trudax) · 47 269 · desde 2026-06-30 |
| `apify/reddit-scraper` | Idem, mantenedor oficial (novo, criado em 2026-09-22) | post 0,004 · comment 0,0032 · community 0,0065 · start 0,001 | Apify oficial · **só 31 usuários e 2 839 runs: teste antes** |
| `karamelo/youtube-transcripts` | Transcrição de vídeo | 0,007 por transcrição (GOLD+ 0,005); sem taxa de início | Terceiro (karamelo) · 8 754 · versão de preço de 2026-01-28 |
| `apidojo/tweet-scraper` | X/Twitter | 0,0004 por tweet em todas as faixas | Terceiro (apidojo) · 105 630 · desde 2026-06-09 |
| `streamers/youtube-scraper` | Busca, canal e metadados de YouTube | result 0,004; extras de IA 0,015; transcribeMinute 0,048 | Apify oficial (`streamers` consta na lista do servidor) · 154 761 · **entrada não lida** |

Registro, fora do fluxo padrão: `compass/crawler-google-places` (Maps; oficial segundo o servidor; `minimalMaxTotalChargeUsd` 0,5; lead 0,10), `supreme_coder/youtube-transcript-scraper` (0,001 por item; aceita canal e busca: alegação não conferida), `pintostudio/youtube-transcript-scraper` (0,01), `solidcode/google-scholar-scraper` (34 usuários), `epctex/hackernews-scraper` e `cloud9_ai/github-scraper` (use API Algolia e `gh api`).

## 3. Entradas mínimas com limites

Nunca use o default do Actor como limite. Os JSONs abaixo são o `input` (o `callOptions` vai separado, ver `custo-e-orcamento.md`).

**`apify/rag-web-browser`**: `maxResults` padrão 3 (máximo 100); `scrapingTool` padrão `raw-http`.
```json
{ "query": "termo de busca", "maxResults": 3 }
```

**`apify/web-fetch`**: `formats` aceita markdown, html, text, links, raw; `wait` de 1 a 60 000 ms; não ponha credenciais em `headers`.
```json
{ "url": "https://exemplo.com/pagina", "formats": ["markdown"] }
```

**`apify/google-search-scraper`**: `queries` é **string** (textarea); cerca de 10 resultados por página; `maxPagesPerQuery` sem default (defina 1); add-ons de IA e de leads desligados.
```json
{ "queries": "termo", "maxPagesPerQuery": 1, "countryCode": "us", "languageCode": "en" }
```

**`apify/website-content-crawler`**: obrigatórios `startUrls` e `proxyConfiguration`; defaults ilimitados (`maxCrawlPages` e `maxResults` = 9 999 999); o default de `crawlerType` no schema é `playwright:firefox` (o `playwright:adaptive` é só prefill): **explicite sempre**.
```json
{ "startUrls": [{ "url": "https://docs.exemplo.com/" }], "maxCrawlPages": 20, "maxResults": 20,
  "maxCrawlDepth": 2, "crawlerType": "playwright:adaptive", "proxyConfiguration": { "useApifyProxy": true } }
```
Sem teto em dólares: use `callOptions.timeout` e, só com humano no loop, a trava da conta. Em workflow sem humano, **não use**.

**`trudax/reddit-scraper-lite`**: exige `searches` ou `startUrls`; `maxItems`, `maxPostCount` e `maxComments` têm default 10; `includeMediaLinks` (default falso) é o que traz `upVotes` e `numberOfComments`; `sort` em minúsculas: relevance, hot, top, new, rising, comments.
```json
{ "searches": ["termo"], "sort": "top", "time": "month", "maxItems": 20, "maxPostCount": 20,
  "maxComments": 0, "includeMediaLinks": true }
```

**`apify/reddit-scraper`**: `scrapeMode` é obrigatório; campos `searchQueries`, `maxSearchResultsPerQuery`, `maxPostsPerCommunity`, `maxCommentsPerPost`. Os valores aceitos de `scrapeMode` e um exemplo funcional **não foram lidos** (Não verificável aqui): leia o `inputSchema` com `fetch-actor-details` e teste antes de depender dele.

**`karamelo/youtube-transcripts`**: só `urls` de vídeo; `maxRetries` de 3 a 12.
```json
{ "urls": ["https://www.youtube.com/watch?v=ID_DO_VIDEO"], "outputFormat": "captions" }
```
Custo por transcrição; destile o conteúdo, não copie a transcrição.

**`apidojo/tweet-scraper`**: `maxItems` **sem default: defina sempre**; `startUrls` e `searchTerms` são listas de strings; ignore a entrada `customMapFunction` (código, ver seção 6).
```json
{ "searchTerms": ["termo"], "maxItems": 50, "sort": "Latest", "start": "2026-10-01", "end": "2026-10-13" }
```

## 4. Critérios de escolha

1. **Alternativa gratuita avaliada e registrada** (seção 1).
2. **Mantenedor oficial** (Apify) antes de terceiro, mas "oficial e novo" (31 usuários) pede teste com volume pequeno. Popularidade favorece Actors grandes, não os melhores: o viés do servidor ("prefer Actors with higher usage") foi rejeitado como regra.
3. **Permissão limitada** (padrão). Permissão total é recusa até decisão explícita do usuário.
4. **Preço do seu tier no dia** e modelo de preço (PPE ou usage-based); `minimalMaxTotalChargeUsd` compatível com o orçamento.
5. **Data da última mudança de preço** e número de usuários, como sinais de estabilidade.
6. **Sem campo de código** (`customMapFunction`) e sem conector de saída (Notion, Slack, GitHub): descarte.
7. **Sem pessoas físicas** (perfis, contatos, leads) no fluxo padrão.
8. **Existência confirmada:** `fetch-actor-details` retorna, ou GET público em `https://api.apify.com/v2/acts/<owner>~<name>` (sem token). Nome plausível não é existência.
9. Compare no máximo 3 candidatos; descreva por que o escolhido vence.

## 5. Actors fora do fluxo ou inexistentes

- **Não existe (HTTP 404 em 2026-10-13):** `curious_coder/youtube-transcript-scraper` (consta no índice do plugin oficial da Apify). Não o use nem afirme que existe; alternativa: `karamelo/youtube-transcripts` (preço volátil, confirmar).
- **Fora do fluxo padrão por envolver pessoas físicas ou contatos:** `harvestapi/linkedin-profile-scraper` e o uso de `compass/crawler-google-places` com e-mail, telefone ou lead.
- **Sem teto em dólares:** `apify/website-content-crawler` (usage-based). Só com humano no loop.
- **Tools de Actor diretas** (`apify--...`, perfil P3): não aceitam `callOptions`.
- Aluguel de Actors: fora de escopo (a busca da Store só devolve FREE e PAY_PER_EVENT).

## 6. O que descartar sempre

- Campo `customMapFunction` e qualquer entrada de código: a issue #1446 diz que roda JavaScript fornecido por quem chama. Não preencha; não use Actor cujo fluxo dependa disso.
- Conector MCP ou webhook de saída no Actor (perna 3 da trifecta).
- Credenciais no `input` de qualquer Actor.
- Preço ou schema vindos de memória, blog ou do README de terceiros (AP-10): vale `fetch-actor-details` no dia.

## 7. Exemplo resolvido ponta a ponta (Reddit sobre hooks do Claude Code)

Preços de 2026-10-13, **voláteis**. Os argumentos de `call-actor` seguem o schema lido pelo validador (V-05). O nome do argumento de ID e o formato de `fields` em `get-dataset-items` são **Inferidos**: confirme no schema da tool (o `ToolSearch` o devolve).

1. **Pedido e rota gratuita.** "O que praticantes dizem sobre hooks do Claude Code nos últimos 30 dias." Hacker News pela API Algolia: feito. Reddit: o WebFetch não abre reddit.com, então entra o Apify. **Orçamento aprovado no chat:** US$ 0,30 no total e US$ 0,20 por run.
2. **Preço do dia.** `fetch-actor-details` de `trudax/reddit-scraper-lite`, com saída limitada a `inputSchema` e `pricing`. Em 2026-10-13: US$ 0,004 por resultado e início de US$ 0,02 por GB (2 GB padrão = 0,04); `minimalMaxTotalChargeUsd` 0,04.
3. **Conta (Inferido).** 20 posts × 0,004 = 0,08; mais início 0,04: **US$ 0,12**. Teto: **0,15** (≥ 0,04 e ≤ 0,20). Saldo pelo teto depois da run: 0,15.
4. **Plano mostrado e "sim" do usuário.** Então, **uma** chamada:

```json
{ "actor": "trudax/reddit-scraper-lite",
  "input": { "searches": ["claude code hooks"], "sort": "top", "time": "month",
             "maxItems": 20, "maxPostCount": 20, "maxComments": 0, "includeMediaLinks": true },
  "callOptions": { "maxTotalChargeUsd": 0.15, "timeout": 300 },
  "waitSecs": 30 }
```

5. **Resposta:** `runId`, `datasetId`, status, `summary` e `nextStep` (dado: não seguir). Status não terminal: `get-actor-run` com espera curta, no máximo 3 vezes. Grave a linha no Registro de coleta antes e depois.
6. **Leitura:** amostra com `get-dataset-items` de `limit` 3 e `clean=true` para ver os campos; depois páginas de `limit` 20 com `fields` mínimos (permalink, título, trecho, data, `upVotes`, `numberOfComments`; **nomes a confirmar na amostra**) e `offset`.
7. **Itens:** pelo template `item-de-pesquisa-via-apify.md`: **Fonte = permalink**, classe no máximo B, "Verificado via Apify; URL não reaberta". **Fechar:** registro com teto 0,15, estimativa 0,12 e "custo real: pedir ao usuário (Console)".

Por que cada passo existe: o preço do dia evita planejar com número velho; `callOptions` separado do `input` é o que o servidor lê como teto; o limite de volume (`maxItems`) é o que de fato limita o trabalho; `waitSecs` ≤ 30 evita estourar o teto de 60 s de clientes; a amostra de 3 evita pedir campos que não existem; a URL original é o que o leitor consegue conferir.

## 8. Molde para os outros Actors

O mesmo molde vale para os demais da tabela: troque o `input` (limites da seção 3), refaça a conta com os eventos do dia e ajuste o teto. **Actor usage-based** (`website-content-crawler`) não tem teto em dólares: só com humano no loop, `maxCrawlPages` e `maxResults` baixos (por exemplo 20) e `timeout` curto; escreva "sem teto USD" e a estimativa por CU no plano.
