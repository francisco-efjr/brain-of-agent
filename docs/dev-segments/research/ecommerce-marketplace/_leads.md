# ecommerce-marketplace — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Segmento com a cobertura mais fraca junto com game-development: poucas pistas. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| shopify-theme-dev-liquid .mdc (CT-06) | https://github.com/PatrickJS/awesome-cursorrules | B | Citado entre as melhores regras do catálogo; arquivo exato não lido pelo validador nesta área: abrir e verificar. CC0. O atlas anota e-commerce como "fraco" no catálogo. |
| FastAPI production architecture (CT-07) | https://github.com/PatrickJS/awesome-cursorrules | B | Idempotência em efeitos (pedido, pagamento), "single writer" por domínio (estoque), bulkhead por provedor. CC0. |
| security-and-owasp (CT-16) | https://github.com/github/awesome-copilot | B | Webhook assinado, sessão e cookies httpOnly em checkout. MIT. |
| security-devsecops (CT-13) | https://github.com/PatrickJS/awesome-cursorrules | B | Sem segredos hardcoded; consultas parametrizadas. CC0. |
| performance-optimization e a11y (CT-19) | https://github.com/github/awesome-copilot | B | Core Web Vitals e acessibilidade de checkout. MIT. |
| playwright-e2e (CT-13, CT-17) | https://github.com/PatrickJS/awesome-cursorrules | B | E2E de carrinho e checkout com `page.route`. CC0. |
| spec-driven workflow e Gherkin (CT-22, CT-13) | https://github.com/github/awesome-copilot | B | Critérios de aceite de promoções e estoque em Given/When/Then. |
| Amplifying (CP-24) | https://amplifying.ai/research/claude-code-picks | B | Declarar stack e bibliotecas (pagamento, auth) antes de gerar. |
| gstack `/office-hours`, `/plan-ceo-review` (BR-20) | https://github.com/garrytan/gstack | B | Premissas e alternativas antes da solução (jargão a remover). |
| Ask HN (CP-21) | https://news.ycombinator.com/item?id=46691243 | B | Fronteiras fortes de módulo e logs para o agente. |
| Brex (PC-29) | https://github.com/brexhq/prompt-engineering | B | Dados de cliente reais fora de prompts e de fine-tuning. MIT. |
| Hooks guardrail (CP-19) | https://aitmpl.com/blog/secure-git-workflow/ | B | Negar comandos destrutivos em banco de pedidos. |
| claude-code-security-review (AO-24) | https://github.com/anthropics/claude-code-security-review | A | Revisão de PR; atribuição obrigatória. MIT. |

## 2. Repositórios e arquivos a abrir
- `PatrickJS/awesome-cursorrules/rules/shopify-theme-dev-liquid-…mdc`.
- `github/awesome-copilot` instructions de security, a11y, performance.
- Snapshot do brain: `brains/qa/references/dominios.md`, `brains/qa/scripts/documentos_br.py`.
- Docs oficiais de Shopify, VTEX, WooCommerce, Medusa; NF-e e impostos; Schema.org/SEO técnico; reservas de estoque: não estão no atlas. Lente authoritative integral.

## 3. Materiais oficiais Anthropic pertinentes
AO-24, AO-23, AO-06; nenhum material Anthropic específico de e-commerce aprovado.

## 4. Padrões da comunidade
- Nenhum relato de praticante aprovado (lacuna declarada em CP).
- Idempotência e dono único de escrita para estoque e pedidos (CT-07).
- Critérios de aceite em Gherkin para promoções e preços (CT-13, BR-08).

## 5. O que o brain-of-agent já oferece
- `brains/qa/references/dominios.md` (e-commerce como semente: carrinho, estoque, regras BR; "não verificado") e `brains/qa/scripts/documentos_br.py` (CPF/CNPJ; validar contra a norma).
- BR-08 (BVA, tabela de decisão, estados, pairwise para variações de catálogo e frete), BR-09 (CBS-IBS e CNPJ alfanumérico em transição, Não verificável), BR-10, BR-20.
- BR-03: modo `ECOMMERCE-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte para catálogo, busca, carrinho, frete, NF-e, marketplace multi-seller, split de pagamento, recomendações, SEO, VTEX/Medusa.
- Regras fiscais brasileiras são Não verificáveis no atlas: exigir norma primária com data.
- Plugin não deve executar compras, pedidos ou chamadas a lojas reais; usar ambientes de teste e dados sintéticos.
