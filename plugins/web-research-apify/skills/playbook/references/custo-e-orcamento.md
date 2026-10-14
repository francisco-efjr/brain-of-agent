# Custo e orçamento

Validade: preços e planos lidos em 2026-10-13 (API pública da Store, apify.com/pricing); a página de Billing foi lida pelo crítico em 2026-10-14. **Selo: volátil.** Preço muda sem aviso (os de `rag-web-browser` mudaram em 2026-10-02, `web-fetch` em 2026-09-10 e `google-search-scraper` em 2026-10-07): confirme com `fetch-actor-details` no dia, que devolve o preço do **seu** tier. Nada foi executado: o comportamento do teto em runtime é Suposição até o smoke test (H-03, H-04).

Rótulos: Verificado (lido na fonte, com data) · Inferido (conta ou dedução) · Suposição · Não verificável.

Sumário: 1. Princípios · 2. Planos e créditos · 3. Limite de uso da conta · 4. Pay-per-event e usage-based · 5. `callOptions` campo a campo · 6. Camadas de teto · 7. Orçamento sugerido · 8. Como estimar e exemplos · 9. Custo invisível ao modelo · 10. Free esgotado · 11. Registro e auditoria · 12. Gotchas

## 1. Princípios

- O dinheiro é do usuário. Gasto só com **orçamento em dólares aprovado por ele no chat**. "Gasta o que precisar" e "não quero nem ver o custo" não são orçamento: sem número, só leitura gratuita (`search-actors`, `fetch-actor-details`, docs).
- O MCP **não mostra o custo real** da run ao modelo (issue #1429: só em `_meta`). Por isso o plugin nunca inventa valor: estima (Inferido), registra o **teto comprometido** e pede ao usuário o custo do Console.
- Uma run por plano aprovado. Nova run exige novo plano, com novo custo para aprovação (AP-04).

## 2. Planos e créditos (V-23; apify.com/pricing, lido em 2026-10-13; classe B, volátil)

| Plano | Preço | Uso incluído e limites | CU |
| --- | --- | --- | --- |
| Free | US$ 0 | US$ 5 de uso por mês; 16 GB de RAM; 5 runs simultâneas | US$ 0,20 |
| Starter | US$ 19 (US$ 17 no anual) | 64 GB; 32 runs | US$ 0,20 |
| Scale | US$ 199 (179) | | US$ 0,16 |
| Business | US$ 999 (899) | | US$ 0,13 |

- **Free esgotado:** o acesso fica bloqueado até o próximo ciclo. Nesse caso o plugin cai no fallback gratuito e registra a lacuna.
- **Plano pago:** o excedente é cobrado até o limite configurado em Billing (seção 3).
- Conflito declarado: a página do Actor `website-content-crawler` usa CU de US$ 0,25 como baseline de estimativa; a página de preços diz 0,20. Estime com a página de preços e declare a divergência.
- Não reconfirmados: add-ons (US$ 5 por run extra, US$ 1 por GB) e o mapeamento plano para tier (FREE, BRONZE, ... DIAMOND). Valores de blogs e de threads (Discord, Trustpilot) foram descartados como não verificáveis.

## 3. Limite de uso da conta: a trava que não depende do modelo

**Console › Billing › Limits**, com *overage* desligado. Ao atingir o limite do plano a plataforma suspende os serviços (docs.apify.com/platform/console/billing, lido pelo crítico em 2026-10-14; fora do `VALIDATED.md`). Com overage ligado, a doc descreve cobrança imediata ao passar de certo valor (no Starter, a partir de US$ 20: lido pelo crítico; reconfirme na página). Se o limite pode ficar abaixo do valor do plano: **Inferido**.

Por que é a trava mais importante: todas as outras camadas (seção 6) dependem de o modelo passar `callOptions`, obedecer "sem re-run" ou responder a um `ask`. Esta funciona mesmo se o modelo errar, e é a única que vale em execução sem humano. Ligue **antes** do primeiro uso e, obrigatoriamente, antes do modo workflow do método de pesquisa (`integracao-metodo-pesquisa.md`). O interruptor de emergência complementar é `claude mcp logout apify` (ou `remove`).

## 4. Pay-per-event e usage-based

- **Pay-per-event (PPE):** o Actor cobra por evento (resultado, página, início, add-on). O teto em dólares **só vale aqui**: ao atingir `maxTotalChargeUsd`, `Actor.charge()` para de cobrar, `pushData` para e a plataforma aborta a run (docs de PPE). Vale **por run**, não por conta nem por sessão. Se o MCP corta a run no teto: Suposição (H-04).
- **Usage-based (uso de plataforma, por CU):** sem eventos, **sem teto em dólares** verificável. Exemplo: `apify/website-content-crawler`. O freio é o limite de volume no `input` (`maxCrawlPages`, `maxResults`), `callOptions.timeout` e `memory`, mais a trava da conta. Escreva "sem teto USD" no plano e use só com humano no loop.
- Conflito de escopo: a doc REST diz que `maxTotalChargeUsd` vale para "todos os modelos de preço"; o schema do MCP diz "Pay-per-event Actors only, ignored otherwise". Trate como **PPE-only** no MCP.
- **Mínimo por Actor:** cada Actor PPE define `minimalMaxTotalChargeUsd` (SERP 0,5; Maps 0,5; `reddit-scraper-lite` 0,04). Teto menor que isso pode ser recusado (Inferido; H-03). Se o orçamento não comporta o mínimo, **não rode**: registre a lacuna.
- **Preço "a partir de" da Store** = tier GOLD (por exemplo US$ 0,00133 por mil); a faixa FREE paga mais. Sempre use o preço do seu tier no dia.

## 5. `callOptions` campo a campo (V-05)

`callOptions` é argumento do `call-actor`. Limites de custo, tempo e memória vão **aqui, nunca no `input` do Actor** (campos com esses nomes no `input` "don't cap the run", conforme duas páginas de docs).

| Campo | Valores | Uso no plugin | Rótulo |
| --- | --- | --- | --- |
| `maxTotalChargeUsd` | dólares por run; só PPE; não limita o trabalho | Sempre em PPE, ≥ `minimalMaxTotalChargeUsd` e ≤ teto por run | Verificado (schema) |
| `timeout` | segundos; `0` = sem limite | **Sempre definir e nunca `0`**; é o freio de tempo do Actor usage-based. Sugestão: 60 a 300 s para coletas pequenas | Verificado; valores sugeridos são Suposição |
| `memory` | 128 a 32768 MB | Só se o Actor exigir: a taxa de início de alguns Actors escala com a memória (Inferido). O limite de 4096 MB só vale para tools diretas | Verificado; efeito no preço Inferido |
| `build` | tag ou número de build | Não altere sem motivo | Verificado |
| `maxItems` | só pay-per-result; **legado** (issue #1403 propõe remover) | **Não usar.** Limite o trabalho com campos do próprio Actor | Verificado |

Limitar o trabalho é com campos do `input` do próprio Actor (`maxItems`/`maxPostCount` no Reddit, `maxCrawlPages` e `maxResults` no crawler, `maxResults` no `rag-web-browser`): o teto em dólares para o dinheiro, o limite de volume para o trabalho.

`waitSecs`: 0 a 45; o plugin usa **≤ 30**, porque vários clientes MCP impõem 60 s por requisição. Run não terminal vira `get-actor-run` (no máximo 3 verificações).

## 6. Camadas de teto

| Camada | O que cobre | Buraco | Depende do modelo? |
| --- | --- | --- | --- |
| `callOptions.maxTotalChargeUsd` | Dinheiro de uma run PPE | Não vale em usage-based; não limita o trabalho | Sim |
| `callOptions.timeout` | Tempo da run (freio do usage-based) | Custo por tempo varia com o Actor | Sim |
| Limite de volume no `input` | Trabalho do Actor | O default costuma ser ilimitado (crawler 9 999 999; `tweet-scraper` sem default) | Sim |
| Orçamento por plano, lente e segmento | Soma de tetos comprometidos | É registro autodeclarado | Sim |
| `ask` em `call-actor` (Claude Code) | Um ponto de parada humano por run | Não é respondível em modo não interativo (H-08) | Não (imposto pelo Claude Code) |
| **Limite de uso da conta** (Billing › Limits, overage desligado) | Suspende no limite do plano | Granularidade mensal; com overage ligado não vale | **Não** |
| `claude mcp logout` ou `remove` | Corta todas as tools da sessão | Ação manual | Não |

Cada camada cobre o buraco da outra. Nenhuma sozinha basta; a da conta é a única que independe de obediência.

## 7. Orçamento sugerido (Suposição; a decisão é do usuário)

Valores de referência do validador, para propor quando o usuário pedir ajuda e **sempre rotulados Suposição**:

- **Por run:** `max(minimalMaxTotalChargeUsd, 3 × estimativa)` limitado a US$ 0,50.
- **Por lente:** US$ 1,00. **Por segmento:** US$ 3,00. O plano Free dá US$ 5 por mês e bloqueia ao esgotar.
- Em coleta única com volume já limitado no `input`, uma margem menor que 3× é escolha consciente: o exemplo de `actors-para-pesquisa.md` usa teto de US$ 0,15 para estimativa de US$ 0,12 porque o usuário limitou a US$ 0,20 por run.
- O teto de cada run é **≤ o menor entre o orçamento restante e o teto por run aprovado**. A soma dos tetos comprometidos nunca passa do orçamento total (regra R1 da auditoria).
- Se o orçamento total é menor que o mínimo do Actor, a resposta correta é "não cabe": proponha outro Actor, a rota gratuita ou um orçamento maior para aprovação.

## 8. Como estimar e exemplos (V-24; faixa FREE em 2026-10-13; **Inferido**: soma sobre os eventos lidos no JSON da Store)

Passos: (1) `fetch-actor-details` no dia, com saída limitada a `inputSchema` e `pricing`; (2) liste os eventos e o preço do seu tier; (3) multiplique pelo volume do `input`; (4) some a taxa de início (por GB; a memória padrão importa); (5) escreva a conta no plano. A unidade de cobrança do evento `search` do `rag-web-browser` (por consulta ou por link) não está documentada (lacuna 5, H-12).

| Actor | Cenário | Conta | Estimativa |
| --- | --- | --- | --- |
| `apify/rag-web-browser` | 1 consulta e 3 páginas | 0,00348 + 3 × 0,00228 + início | ≈ US$ 0,011 |
| `apify/web-fetch` | 1 página | 0,0015 + 0,00005 de início | ≈ US$ 0,0016 por página |
| `apify/google-search-scraper` | 1 página de SERP | 0,0045 + 0,00005 de início; add-ons desligados; **`minimalMaxTotalChargeUsd` 0,5** | ≈ US$ 0,0045 por página |
| `trudax/reddit-scraper-lite` | 100 posts | 100 × 0,004 + início 2 GB × 0,02 = 0,04 | ≈ US$ 0,44 |
| `apidojo/tweet-scraper` | 1 000 tweets | 1 000 × 0,0004 | ≈ US$ 0,40 |
| `karamelo/youtube-transcripts` | 100 transcrições | 100 × 0,007 | ≈ US$ 0,70 |

Alertas de preço: os add-ons de IA do `google-search-scraper` custam US$ 0,20 cada na faixa FREE (lead US$ 0,10; AI Overview US$ 0,003; website-content US$ 0,008); mantenha **desligados**. O custo mínimo por run é dominado pela taxa de início em alguns Actors e escala com a memória.

## 9. Custo invisível ao modelo e como obtê-lo

- A resposta do `call-actor` traz IDs de storage, `summary` e `nextStep`, **sem itens e sem custo** (H-05). Não há campo de custo para o modelo ler.
- **Fonte do custo real:** o Console da Apify (Billing/Usage e lista de Runs), lido pelo usuário. Peça o valor ao usuário e registre "Informado por: usuário (Console)". Enquanto não houver, escreva **"não verificável"**; custo desconhecido não é conformidade.
- **Opcional (H-05b, não testado):** `apify-api-read` em `GET /v2/actor-runs/<runId>` pode trazer `usageTotalUsd`; exige carregar a categoria `api` (`tools=actors,docs,api`) e reverter depois. Se funcionar, a auditoria lê o custo sem o Console.
- Nunca peça o token para "consultar o custo".

## 10. Free esgotado, sem orçamento ou erro de autenticação

Siga sem Apify: WebSearch, WebFetch, `gh api`, API Algolia do Hacker News, dev.to. Registre "Apify indisponível: <fonte> não coletada" (por exemplo "Reddit: não coletado"). Se o usuário quiser, ele mesmo roda o Apify CLI (**a CLI não tem flag de teto**: avise). Nunca peça token (WR-13).

## 11. Registro e auditoria

- Registro por run em `assets/templates/registro-de-custo.md`: orçamento, Actor, `runId`, teto, estimativa, status, custo real (Console) e quem informou.
- Auditoria: regras R1 a R12 em `checklist-completo.md` (seção "Auditoria de custo"), executadas pela skill `auditoria-de-custo` e pelo agente `apify-cost-auditor`.
- Fórmulas: saldo pelo teto = orçamento − soma dos tetos comprometidos; saldo real = orçamento − custo real informado (só com custo conhecido).

## 12. Gotchas de custo

- `maxTotalChargeUsd`, `timeout` ou `memory` dentro do `input` não são teto: esses limites só valem em `callOptions` (AP-02). Já `maxResults`, `maxCrawlPages` e afins no `input` são o limite de volume do próprio Actor, e devem estar lá.
- Tool de Actor direta não aceita `callOptions`: sem teto (AP-01).
- `callOptions.timeout` `0` significa sem limite: defina sempre.
- Run PPE cortada no teto devolve itens parciais ou vazios: isso **não** autoriza re-rodar com teto maior sem novo plano.
- Actor usage-based sem limite de volume é o caso de maior risco (crawler com defaults de 9 999 999).
- O preço de um Actor pode mudar entre o plano e a run: releia `fetch-actor-details` imediatamente antes de executar.
