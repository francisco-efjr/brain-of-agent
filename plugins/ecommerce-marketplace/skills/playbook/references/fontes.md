# Fontes (bibliografia validada)

As páginas abaixo foram lidas pelo validador do segmento em **2026-10-10** (coluna "Consulta"). Este arquivo foi **compilado em 2026-10-11 sem reabrir as páginas**: confira a fonte antes de reutilizar um número, prazo ou versão. Classe **A** = documentação oficial da tecnologia, norma ou texto de lei; **B** = autor ou projeto reconhecido, documentação de fornecedor; **C** = sinal de prática ou fonte pouco verificada. O número entre parênteses é a pontuação 0–10 da rubrica de fontes. "Licença" descreve o que foi **identificado**; sem licença identificada, o plugin só destila (redação própria) e cita a URL. Nenhum trecho literal de terceiros foi copiado; o único texto reaproveitado quase literalmente é o do brain-of-agent (conteúdo do próprio autor, MIT), com atribuição.

Modelo-alvo: Claude 4.x/5.x. Revisões feitas por modelos da família Claude têm independência parcial: não equivalem a validação externa. Os prompt-scores citados no consolidado de pesquisa são autoavaliação do validador e funcionam como piso de intenção.

## Sumário

- [Como citar](#como-citar) · [Classe A](#classe-a) · [Classe B](#classe-b) · [Classe C](#classe-c)
- [Repositórios: licença e último commit](#repositórios-licença-e-último-commit)
- [Conteúdo próprio (brain-of-agent) e fatos não reverificados](#conteúdo-próprio-brain-of-agent-e-fatos-não-reverificados)
- [Rejeitados e rebaixados](#rejeitados-e-rebaixados) · [Correções aos pesquisadores](#correções-aos-pesquisadores) · [Lacunas conhecidas](#lacunas-conhecidas)

## Como citar

- `V-nn` identifica o item correspondente no consolidado de pesquisa deste segmento; cite-o ao justificar uma recomendação.
- Versões, flags, prazos e tabelas mudam. Confirme na versão instalada (`<ferramenta> --version`, `--help`) e na página oficial antes de copiar um comando.
- Números de blogs e relatos (percentuais, contagens) são dos autores originais; cite com a fonte e a ressalva.
- Estrelas e forks foram observados nas páginas dos repositórios em 2026-10-10 e não provam qualidade.
- Texto de lei e de documentação foi **parafraseado**; marque a data de leitura ao citar norma.

## Classe A

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-01 (9) | Claude Code best practices | https://code.claude.com/docs/en/best-practices | não declarada; destilado | 2026-10-10 | Verificação executável, plano, CLAUDE.md enxuto, revisor adversarial, recomeço após duas correções |
| V-02 (9) | Claude Code skills (SKILL.md) | https://code.claude.com/docs/en/skills | idem | 2026-10-10 | `description` truncada em 1.536 caracteres; `disable-model-invocation`; progressive disclosure; repositório `anthropics/skills` é *source-available* (não copiar) |
| V-03 (9) | Claude Code hooks guide | https://code.claude.com/docs/en/hooks-guide | idem | 2026-10-10 | `PreToolUse` exit 2 / `permissionDecision` em `hookSpecificOutput`; precedência `deny` > `defer` > `ask` > `allow`; antes de qualquer modo de permissão |
| V-04 (9) | Building effective agents (Anthropic, 19/12/2024) | https://www.anthropic.com/engineering/building-effective-agents | idem | 2026-10-10 | Workflow × agente; aviso de que o ferramental mudou desde 2024 |
| V-05 (9) | Effective context engineering for AI agents (29/09/2025) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | idem | 2026-10-10 | Compactação, notas fora da janela, subagentes com resumo |
| V-06 (8) | Plugins reference · claude-plugins-official | https://code.claude.com/docs/en/plugins-reference · https://github.com/anthropics/claude-plugins-official | Apache-2.0 (repo; cada plugin pode ter a sua) | 2026-10-10 | Layout; `CLAUDE.md` na raiz do plugin não carrega; `plugin.json` só exige `name` |
| V-07 (9) | Memory (CLAUDE.md × AGENTS.md) | https://code.claude.com/docs/en/memory | idem | 2026-10-10 | `@AGENTS.md`; leitura direta de AGENTS.md a partir da v2.1.277 |
| V-32 (8) | Decreto 7.962/2013 · Lei 13.709/2018 (LGPD) | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/decreto/d7962.htm · https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm | texto de lei (ausência de proteção autoral: Inferido) | 2026-10-10 | Checkout BR: arts. 2º, 4º, 5º, 6º; LGPD arts. 6º, 7º, 18, 37, 41, 48, 52 |
| V-33 (8) | Lei Complementar 214/2025 (texto compilado) | https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm | idem | 2026-10-10 | Arts. 11, 22, 343, 344, 346, 347, 348 (só trechos de ~960 mil caracteres) |
| V-40 (8) | Playwright: network, mock, test-fixtures, browser-contexts | https://playwright.dev/docs/network · /mock · /test-fixtures · /browser-contexts | não declarada; destilado | 2026-10-10 | Isolar provedor de pagamento no E2E; `serviceWorkers: 'block'`; HAR |
| V-45 (9) | Google: navegação facetada | https://developers.google.com/crawling/docs/faceted-navigation | idem | 2026-10-10 | robots.txt, `#`, 404 em combinação vazia (atualizada em 2025-12-18) |
| V-46 (9) | Google: migração de site com mudança de URL | https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes | idem | 2026-10-10 | 301, mapeamento, cadeias ≤ 3, ≥ 1 ano |
| V-53 (9) | WCAG 2.2 Understanding: Redundant Entry (3.3.7) | https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html | W3C; destilado | 2026-10-10 | Entrada redundante no checkout |
| V-54 (9) | ANPD: comunicação de incidentes de segurança | https://www.gov.br/anpd/pt-br/assuntos/comunicacao-de-incidentes-de-seguranca-cis | uso governamental; destilado | 2026-10-10 | Relógio de 3 dias úteis e 20 dias úteis; **Requer revisão jurídica** |
| V-55 (9) | CDC, Lei 8.078/1990, texto compilado (art. 49) | https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm | texto de lei | 2026-10-10 | Arrependimento; **Requer revisão jurídica** |
| V-56 (8) | LC 190/2022 · EC 87/2015 | https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp190.htm · https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc87.htm | texto de lei | 2026-10-10 | DIFAL (partes verificadas); **Requer revisão tributária** |
| V-57 (8) | LC 214/2025, arts. 31–35 (split payment; com LC 227/2026) | https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm | texto de lei | 2026-10-10 | Split payment; calendário **Não verificável** |

## Classe B

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-08 (7) | `anthropics/claude-code-security-review` | https://github.com/anthropics/claude-code-security-review | MIT | 2026-10-10 | Revisor de checkout; Action documentada (T-02) |
| V-09 (7) | Stripe webhooks · Shopify webhooks · `hookdeck/webhook-skills` | https://docs.stripe.com/webhooks · https://shopify.dev/docs/apps/build/webhooks · https://github.com/hookdeck/webhook-skills | doc não declarada; Hookdeck MIT (90★) | 2026-10-10 | Checklist de 10 itens |
| V-10 (7/6) | Stripe: requisições idempotentes · Fowler: Idempotent Receiver | https://docs.stripe.com/api/idempotent_requests · https://martinfowler.com/articles/patterns-of-distributed-systems/idempotent-receiver.html | não declarada | 2026-10-10 | Chave por intenção de compra |
| V-11 (7) | Stripe Connect: charges | https://docs.stripe.com/connect/charges | não declarada | 2026-10-10 | Tipos de cobrança; 4 perguntas |
| V-12 (5) | `fastapi-production-architecture` (awesome-cursorrules) | https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/fastapi-production-architecture-cursorrules-prompt-file.mdc | CC0-1.0 (repo, 40,9 mil★); autor do arquivo não verificado | 2026-10-10 | Escritor único, bulkhead, `retryable` |
| V-13 (7) | OWASP Top 10:2025 · `security-and-owasp.instructions` (awesome-copilot) | https://top10.owasp.org/2025 · https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/security-and-owasp.instructions.md | OWASP: licença não confirmada (Não verificável); awesome-copilot MIT (39,9 mil★) | 2026-10-10 | A01–A10 no checkout; snippets do arquivo têm defeitos |
| V-14 (6) | Shopify: arquitetura de temas · CLI | https://shopify.dev/docs/storefronts/themes/architecture · https://shopify.dev/docs/storefronts/themes/tools/cli | não declarada; regra de comunidade CC0 (repo) | 2026-10-10 | Checklist de 12 itens |
| V-15 (7) | web.dev: Core Web Vitals (31/10/2024) · `performance-optimization.instructions` | https://web.dev/articles/vitals · https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/performance-optimization.instructions.md | não declarada; MIT | 2026-10-10 | LCP/INP/CLS no p75 |
| V-16 (7) | WCAG 2.2 Quick Reference · `a11y.instructions` · `kgelster/ecom-a11y-audit` | https://www.w3.org/WAI/WCAG22/quickref/ · https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/a11y.instructions.md · https://github.com/kgelster/ecom-a11y-audit | W3C destilado; MIT; MIT (12★) | 2026-10-10 | Checklist de formulário; grau de evidência |
| V-17 (6) | Google: dados estruturados de Product e Merchant listing | https://developers.google.com/search/docs/appearance/structured-data/product · /merchant-listing | não declarada | 2026-10-10 | `availability` recomendada; variantes |
| V-18 (6) | `kgelster/awesome-ecom-skills` · `40RTY-ai/shopify-admin-skills` · `woocommerce/woocommerce-claude` | https://github.com/kgelster/awesome-ecom-skills · https://github.com/40RTY-ai/shopify-admin-skills · https://github.com/woocommerce/woocommerce-claude | MIT (49★) · MIT (194★) · GPL-3.0-or-later (30★) | 2026-10-10 | Padrão do gate (redação própria) |
| V-19 (5) | Armadilhas de catálogo (`awesome-ecom-skills`) | https://github.com/kgelster/awesome-ecom-skills | MIT | 2026-10-10 | 6 pontos de catálogo |
| V-21 (5) | `brexhq/prompt-engineering` | https://github.com/brexhq/prompt-engineering | MIT (9,6 mil★); conteúdo de 2023, uso interno | 2026-10-10 | Só princípios: dados reais fora do prompt |
| V-22 (6) | Best practices (entrevista de spec) · `spec-driven-workflow-v1.instructions` · `garrytan/gstack` | https://code.claude.com/docs/en/best-practices · https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/spec-driven-workflow-v1.instructions.md · https://github.com/garrytan/gstack | doc não declarada; MIT; MIT (135,8 mil★) | 2026-10-10 | EARS, entrevista, desafio de premissas (gstack: só o padrão) |
| V-23 (6) | `playwright-typescript.instructions` | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/playwright-typescript.instructions.md | MIT | 2026-10-10 | Convenções de E2E |
| V-24 (5) | `medusa.mdc` · Medusa: módulo de inventário | https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/medusa.mdc · https://docs.medusajs.com/resources/commerce-modules/inventory | CC0 (repo); doc não declarada | 2026-10-10 | Regras Medusa v2 (conferir versão) |
| V-25 (6) | `agent-safety.instructions` | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/agent-safety.instructions.md | MIT | 2026-10-10 | Fail-closed, allowlist, aprovação humana |
| V-26 (6) | Spotify Engineering: Portal (03/09/2026) | https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90 | não declarada | 2026-10-10 | Leitura em lote; `offset/limit`; rebaixado de A |
| V-27 (6) | `anthropics/claude-cookbooks` · `anthropics/skills` | https://github.com/anthropics/claude-cookbooks · https://github.com/anthropics/skills | MIT (53,3 mil★) · skills de documento *source-available* | 2026-10-10 | Avaliação de atendimento de pedido (notebooks não abertos) |
| V-28 (5) | Skills de fornecedores: Shopify, Medusa, Stripe, WooCommerce | https://github.com/Shopify/agent-skills · https://github.com/medusajs/medusa-agent-skills · https://docs.stripe.com/skills.md | sem licença na raiz (Shopify, Medusa); GPL (Woo) | 2026-10-10 | Só referência; não instalar |
| V-29 (7) | Stripe Connect: onboarding · verificação de identidade | https://docs.stripe.com/connect/onboarding · https://docs.stripe.com/connect/identity-verification | não declarada | 2026-10-10 | KYC; `eventually_due`/`currently_due` |
| V-30 (7) | Mercado Pago: notificações · Asaas: webhooks | https://www.mercadopago.com.br/developers/pt/docs/checkout-api-orders/notifications · https://docs.asaas.com/docs/sobre-os-webhooks · https://docs.asaas.com/reference/comece-por-aqui | não declarada | 2026-10-10 | Tabela por provedor |
| V-31 (7) | API Pix do Banco Central (`openapi.yaml`, v2.10.0) | https://raw.githubusercontent.com/bacen/pix-api/master/openapi.yaml | Apache-2.0 declarado no YAML (sem LICENSE na raiz) | 2026-10-10 | `txid` 26–35; webhook só com `txid` |
| V-34 (7) | Portal Nacional da NF-e (Notas Técnicas e Informes) · `nfephp-org/sped-nfe` | https://www.nfe.fazenda.gov.br/portal/principal.aspx · https://raw.githubusercontent.com/nfephp-org/sped-nfe/master/README.md | uso governamental; LGPL v3 (README oferece "LGPLv3 ou MIT"): só destilar | 2026-10-10 | Fichas de NT com datas; README do sped-nfe desatualizado |
| V-35 (7/6) | Melhor Envio (fluxo, cotação, webhooks) · Correios Developers | https://docs.melhorenvio.com.br/docs/fluxo-completo-de-integracao.md · /cotacao-de-fretes.md · /webhooks.md · https://www.correios.com.br/atendimento/developers | não declarada | 2026-10-10 | Cotação → etiqueta → rastreio |
| V-36 (5) | Mercado Livre · Amazon SP-API · Mirakl · Mercado Pago Split | https://developers.mercadolivre.com.br/pt_br/produto-receba-notificacoes · https://developer-docs.amazon.com/sp-api/docs/notifications-api-v1-use-case-guide · https://developer.mirakl.com/ · https://www.mercadopago.com.br/developers/pt/docs/split-payments/landing | não declarada | 2026-10-10 | Matriz de canais; só notificações lidas |
| V-37 (6) | Typesense · Meilisearch · Algolia (facetas) | https://typesense.org/docs/latest/api/search.html · https://www.meilisearch.com/docs/learn/filtering_and_sorting/search_with_facet_filters · https://www.algolia.com/doc/guides/managing-results/refine-results/faceting/ | não declarada | 2026-10-10 | Checklist de busca |
| V-38 (6) | Shopify Functions (product discounts) · Medusa promotion e ações | https://shopify.dev/docs/api/functions/reference/product-discounts · https://docs.medusajs.com/resources/commerce-modules/promotion · /promotion/actions | não declarada | 2026-10-10 | Modelo de promoção |
| V-39 (6) | Medusa: inventory-in-flows e locks · Shopify `InventoryLevel` | https://docs.medusajs.com/resources/commerce-modules/inventory/inventory-in-flows · https://docs.medusajs.com/learn/fundamentals/workflows/locks · https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel | não declarada | 2026-10-10 | Reserva e lock |
| V-41 (5) | WooCommerce REST API (nova e legada v3) | https://developer.woocommerce.com/docs/apis/rest-api/ · https://woocommerce.github.io/woocommerce-rest-api-docs/ | não declarada | 2026-10-10 | Autenticação, paginação, status de webhook |
| V-42 (6) | VTEX: Orders Feed e Hook | https://developers.vtex.com/docs/guides/orders-feed | não declarada | 2026-10-10 | Tabela por provedor |
| V-43 (5) | PCI Security Standards Council: padrões | https://www.pcisecuritystandards.org/standards/ | não declarada | 2026-10-10 | Escopo de PCI; versão não lida |
| V-44 (7) | Textos reais: `security-review.md` e `prompts.py` · `shopify-catalog-audit` · `shopify-redirect-mapping` | repositórios `anthropics/claude-code-security-review` e `kgelster/awesome-ecom-skills` | MIT | 2026-10-10 | Correções ao revisor; modelo somente leitura; limiares de redirect |
| V-47 (7) | Mercado Pago: Split 1:1 (integrar marketplace) | https://www.mercadopago.com.br/developers/pt/docs/split-payments/split-1-1/integration-configuration/integrate-marketplace | não declarada | 2026-10-10 | `marketplace_fee`/`application_fee` |
| V-48 (6) | Medusa: reservas · `cancelOrderWorkflow` · inventory-in-flows | https://docs.medusajs.com/user-guide/inventory/reservations/index.html.md · https://docs.medusajs.com/resources/references/medusa-workflows/cancelOrderWorkflow | não declarada | 2026-10-10 | Cancelamento libera reserva |
| V-49 (6) | Medusa: locks de workflow | https://docs.medusajs.com/learn/fundamentals/workflows/locks | não declarada | 2026-10-10 | `acquireLockStep` |
| V-50 (7) | Shopify: estados de estoque · `InventoryLevel` | https://shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps/manage-quantities-states | não declarada | 2026-10-10 | `committed` somente leitura |
| V-51 (7) | Nuvemshop: webhooks | https://tiendanube.github.io/api-documentation/resources/webhook | não declarada | 2026-10-10 | Domínio em migração para nuvemshop.dev |
| V-52 (7/6) | Nuvemshop: pedido · multi-estoque | https://tiendanube.github.io/api-documentation/resources/order · https://nuvemshop.dev/en-US/api/guides/multi-inventory/multi-inventory | não declarada | 2026-10-10 | `restock`, `inventory_behaviour` |
| V-58 (6) | SEFAZ-GO: ocorrência de problemas técnicos · Portal NF-e (contingência) | https://goias.gov.br/economia/ocorrencia-de-problemas-tecnicos-2/ | uso governamental; destilado | 2026-10-10 | Checklist de contingência sem números |

## Classe C

| Item | Título | URL | Licença | Consulta | Uso e ressalva |
| --- | --- | --- | --- | --- | --- |
| V-20 (4) | `vishkaty/commerce-agents-medusa` | https://github.com/vishkaty/commerce-agents-medusa | Apache-2.0 | 2026-10-10 | Retenção por divergência: **padrão, não evidência** (1★, 4 commits, alegações do autor não reproduzidas) |
| V-29 (4, parte) | Adyen for Platforms | https://docs.adyen.com/platforms/ | não declarada | 2026-10-10 | Só conceito de split e retenção; **Brasil não aparece** nas regiões listadas |
| V-59 | Regra de projeto: CFOP/NCM não saem de memória | — | — | 2026-10-10 | **Suposição fundamentada**; nenhum texto primário de CFOP lido (Confaz deu 404 na URL tentada) |

## Repositórios: licença e último commit

Verificado em 2026-10-10 pelo feed Atom de commits e por `LICENSE` bruto (API do GitHub sem cota anônima). Estrelas e commits vêm das páginas.

| Repositório | Último commit | Licença verificada |
| --- | --- | --- |
| Shopify/agent-skills | 2026-04-01 | **nenhuma** na raiz de `main` (404) |
| medusajs/medusa-agent-skills | 2026-10-05 | **nenhuma** na raiz de `main` |
| nfephp-org/sped-nfe | 2026-10-02 | LGPL v3 (`LICENSE.md`); README: "LGPLv3 ou MIT" |
| anthropics/claude-code-security-review | 2026-02-11 | MIT |
| kgelster/awesome-ecom-skills | 2026-08-22 | MIT |
| 40RTY-ai/shopify-admin-skills | 2026-08-14 | MIT |
| hookdeck/webhook-skills | 2026-10-08 | MIT |
| bacen/pix-api | 2026-08-19 | sem LICENSE na raiz; YAML declara Apache-2.0 |
| garrytan/gstack | 2026-10-09 | MIT |

As datas de commit dos demais repositórios (awesome-copilot, awesome-cursorrules, brexhq, ecom-a11y-audit, woocommerce-claude) **não foram observadas**.

## Conteúdo próprio (brain-of-agent) e fatos não reverificados

Repositório `francisco-efjr/brain-of-agent` (MIT, conteúdo do próprio autor do plugin), snapshot em `docs/foundation/brain-of-agent-snapshot/`:

- `brains/qa/references/dominios.md` — tabelas de Pagamentos e fintech, Pix, Boleto, Cartão, PCI DSS, E-commerce, Microsserviços e eventos, Documentos e formatos brasileiros, datas/moeda/feriados/fusos, reforma tributária CBS/IBS. Incorporado e adaptado em `pagamentos-webhooks-split.md`, `estoque-pedidos-promocoes.md`, `fiscal-frete-br.md`, `checkout-seguranca-a11y-perf.md` e `padroes-e-antipadroes.md`, com atribuição.
- `brains/qa/scripts/documentos_br.py` — copiado integralmente para `assets/scripts/documentos_br.py` com cabeçalho de atribuição; `--self-test` passa.
- Estilo da casa: keyword `<SEGMENTO>-COMPLETO`, rótulos epistêmicos, proporcionalidade.

**Fatos do brain não reverificados nesta pesquisa (rotulados Inferido onde aparecem):** limites e prazos do Pix (limite noturno, dispositivo novo, MED de 80 dias, devolução em 90 dias, Pix Automático), regras de boleto (fator de vencimento reiniciado em 22/02/2025), PCI DSS 4.0.1 vigente com requisitos 6.4.3 e 11.6.1 obrigatórios desde 31/03/2025, cartões de teste da Stripe, tabela de transição CBS/IBS de 2029–2033 e Imposto Seletivo de 2027, feriado de 20/11 (Lei 14.759/2023), fusos sem horário de verão desde 2019, regra de arrependimento "frete incluso". Confirme na norma ou regulamento vigente antes de usar um valor como resultado esperado.

Workflows do gstack (MIT) inspiraram só o padrão de desafiar premissas; nada foi copiado.

## Rejeitados e rebaixados

| Item | Decisão | Motivo |
| --- | --- | --- |
| `shopify-mcp` | Rejeitado | 143★ com 400 forks (anômalo); instalação clona outro repositório; ferramentas de cancelar, reembolsar, excluir e mesclar sem confirmação |
| `noique/cross-border` | Rejeitado | CC BY-NC 4.0 (uso comercial proibido); mercado fora do Brasil |
| `Keypo` | Rejeitado | Página nunca aberta; alegação não verificada |
| `office-hours` (gstack) como modelo | Rejeitado | Grava configuração, telemetria, `codex exec`, automação de navegador |
| aitmpl | Rebaixado C(3) | Instala por `npx` de terceiros; sem data |
| amplifying.ai | Rebaixado C(4) | Testou modelos e versão do Claude Code já defasados |
| tanujrajputdev (SEO) | Rebaixado C(4) | Changelog admite erros (robots.txt, "teto de 128 KB" inventado); promove serviço pago |
| claude-marketing | Rebaixado C(4) | `setup.py`/`install.sh` (não executar); foco em marketing |
| Hacker News (46691243) | Rebaixado C(4) | Anedotas sem autoria verificável; evidência complementar |
| nexscope, mollie-best-practices, nextjs15-supabase | Rebaixados C (ideia) | Não reverificados; não se aplicam ao Brasil |
| Exemplos legados do WooCommerce com RequestBin | Rejeitado | Serviço de captura de terceiros |
| "Fase inicial B2B / nenhuma ação em B2C" para split payment | Rejeitado | A LC 214 mira adquirentes não contribuintes (V-57) |
| Decreto 12.955/2026, Ato Técnico Conjunto nº 4/2026, teste em 15/10/2026 | Não verificável | Só em buscas e blogs |
| 168 h, `tpEmis`, evento 110140 (contingência) | Não verificável | MOC não lido |
| Alíquotas 7%/12%, Simples, NFC-e, ADIs, Ajuste SINIEF 3/2024 | Não verificável | Sem fonte primária lida |
| Registro obrigatório de incidentes com retenção de 5 anos | Não verificado | Fora da página da ANPD lida |
| Sitemap com links circulares; `incoming` depreciado (Shopify) | Rejeitado | Não constam das páginas lidas |

## Correções aos pesquisadores

1. `plugin.json` "obrigatório": a referência atual diz opcional, só `name` obrigatório (V-06).
2. `availability` como obrigatória no Google: é recomendada (V-17).
3. "Nunca consultar banco em loop" (Liquid): o arquivo diz "limitar"; Liquid não acessa banco (V-14, conflito C12).
4. Brex "sem licença": é MIT, 9,6 mil estrelas, conteúdo de 2023 (V-21).
5. Hookdeck: retry de 4xx/5xx generalizado indevidamente; a Stripe reentrega qualquer não-2xx (V-09, C2).
6. `security-review` dado como A9: último commit 2026-02-11 e modelo padrão defasado ⇒ B7 (V-08).
7. Spotify dado como A8: a economia de ~90% vale para leituras em lote (V-26).
8. gstack: "seis perguntas" confirmado depois (modo startup), mas o arquivo tem efeitos colaterais (V-22, V-44, conflito C7).
9. WooCommerce "sem dados individuais": há linhas pseudonimizadas (V-18, conflito C16).
10. FastAPI rule: "estoque" é generalização; o arquivo fala de "hold" (V-12).
11. `reduced motion` listado como AA: é AAA 2.3.3 (V-16).
12. `dry_run` atribuído ao shopify-admin-skills: não consta do SKILL raiz (V-44, conflito C18).
13. `buyget` "não aparece" na Medusa: aparece na página de ações (V-38).
14. README do sped-nfe cita NT 2025.002-RTC v1.20, desatualizada; vigente v1.52 de 01/10/2026 (V-34).
15. Cancelamento libera reserva na Medusa: Verificado; "reduz o vendável" é Inferido (V-48).
16. "Workflow aninhado deve adquirir a mesma chave": invertido; o pai adquire e libera (V-49).
17. CDC art. 49: "dias corridos", "frete devolvido", "sem exigir motivo" não constam do texto (V-55).
18. "Planalto inacessível" e "Portal NF-e com loop": abriram com `curl`, user-agent comum e jar de cookie.

## Lacunas conhecidas

1. **Recomendações de produto e conversão** (carrinho abandonado, analytics, A/B): sem fonte primária.
2. **Comunidade real** (Reddit, X, YouTube, dev.to): nenhuma lente teve busca; o único acesso (API do Hacker News) não trouxe nada útil. A evidência de uso de Claude em lojas é fraca: os "melhores praticantes" aqui são inferidos de documentação oficial, repositórios e padrões de engenharia.
3. **Fiscal:** Manual de Orientação do Contribuinte, PDF das NTs (tags IBS/CBS), Ato Conjunto RFB/CGIBS nº 8/2026, NFC-e por UF, Focus NFe/Tecnospeed, tabela CFOP, regras estaduais de DIFAL/Simples/fundo de pobreza, ADIs, calendário do split, Decreto 7.962 art. 5º relido.
4. **Pagamentos:** boleto (regras bancárias), Pagar.me, idempotência do Mercado Pago, manifest da assinatura do Mercado Pago, reentrega e SLA do webhook Pix por PSP, Manual de padrões do Pix (mTLS).
5. **Marketplace:** Mirakl (API), Mercado Livre/Amazon/Shopee (pedidos e autenticação), Pagar.me split, Mercado Pago split 1:N, Stripe Connect no Brasil.
6. **Frete:** API técnica dos Correios (atrás do login CWS), Frenet, endpoints de cálculo e compra do Melhor Envio.
7. **Busca:** Elasticsearch, Shopify Search & Discovery, busca da Medusa, sinônimos e typos em PT.
8. **Preços:** arredondamento definido por plataforma, valor fixo e teto no Shopify Functions, limite de uso por cliente.
9. **Estoque:** devolução ao estoque físico no cancelamento (Medusa), efeito de cada etapa do pedido em `available/on_hand/reserved` (Shopify), decremento/atomicidade/lote (Nuvemshop), artigo de engenharia sobre oversell.
10. **WooCommerce** (assinatura de webhook, HPOS, gateways) e **VTEX** (Catalog, Checkout, OMS).
11. **PCI DSS** (versão vigente, SAQs, checkout hospedado); **LGPD** (texto integral da Resolução CD/ANPD nº 15/2024, gatilho do prazo).
12. **Prompts reais não lidos:** SKILL de `Shopify/agent-skills`, `medusa-agent-skills`, sub-skills de `shopify-admin-skills` e skills da Stripe.
13. **Playwright:** `storageState` e relatórios de trace.
14. `claude plugin eval` e os casos de avaliação do plugin continuam `designed_not_executed` até rodar; a pontuação de prompts é autoavaliação.
