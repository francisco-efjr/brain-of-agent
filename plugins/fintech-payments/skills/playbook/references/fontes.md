# Fontes (bibliografia validada)

As URLs foram abertas pelo **validador do segmento em 2026-10-10** (coluna "Consulta"); este plugin foi construído em 2026-10-11 **sem reabrir as páginas** — trate a data de consulta como 2026-10-10 e reconfira o que for virar número em código. Classe A = documentação oficial, norma ou fabricante; B = projeto ou autor reconhecido; C = sinal de prática. Entre parênteses, a pontuação 0 a 10 da rubrica de fontes. "Licença" descreve a licença **identificada**; sem licença identificada ou proprietária, o plugin só **destila** (redação própria) e cita a URL. **Nenhum trecho literal de terceiros foi copiado**; o único texto reaproveitado quase literalmente é conteúdo próprio do usuário (brain-of-agent, MIT; V-34 e V-35), com atribuição.

## Sumário

- [Como ler e citar](#como-ler-e-citar)
- [Classe A](#classe-a)
- [Classe B](#classe-b)
- [Classe C e rebaixados](#classe-c-e-rebaixados)
- [Conteúdo próprio e workflows de terceiros](#conteúdo-próprio-e-workflows-de-terceiros)
- [Rejeitados](#rejeitados)
- [Lacunas conhecidas](#lacunas-conhecidas)

## Como ler e citar

- `V-nn` aponta para o item do consolidado de pesquisa deste segmento (`docs/research/fintech-payments/VALIDATED.md` no repositório de desenvolvimento); cite-o ao justificar uma recomendação.
- Versões, limites, prazos e URLs mudam. Confirme na página vigente antes de copiar número para código. Prazos de disputa, mínimos por moeda, versão do Manual do Pix (2.10.0), ASVS (5.0.0) e PCI DSS (4.0.1) são conteúdo vivo.
- Estrelas e commits vêm de páginas HTML do repositório (a API do GitHub ficou em limite de taxa). Estrela não prova qualidade.
- Revisões feitas por modelos da família Claude (pesquisador claude-haiku-5-5, validador claude-sonnet-5-5, sintetizador e construtor) têm independência **parcial**: não equivalem a validação externa. V-34, V-35, V-48, V-49, V-50, V-54, V-63 e V-70 foram escritos pelo validador (derivados) e aguardam revisão cruzada.

## Classe A

| Título | URL | Licença / tratamento | Itens | Consulta |
| --- | --- | --- | --- | --- |
| Stripe — Idempotent requests (8) | https://docs.stripe.com/api/idempotent_requests | proprietária; destilado | V-01 | 2026-10-10 |
| Adyen — API idempotency (8) | https://docs.adyen.com/development-resources/api-idempotency | proprietária; destilado | V-01 | 2026-10-10 |
| Stripe — Webhooks (8) | https://docs.stripe.com/webhooks | proprietária; destilado | V-03 | 2026-10-10 |
| Adyen — Verificar assinaturas HMAC de webhooks (8) | https://docs.adyen.com/development-resources/webhooks/secure-webhooks/verify-hmac-signatures | proprietária; destilado | V-47 | 2026-10-10 |
| Stripe — Payout reconciliation (8) | https://docs.stripe.com/payouts/reconciliation | proprietária; destilado | V-07 | 2026-10-10 |
| Stripe — How disputes work (8) | https://docs.stripe.com/disputes/how-disputes-work (variante `.md`) | proprietária; destilado | V-09 | 2026-10-10 |
| Stripe — 3D Secure e authentication flow (8) | https://docs.stripe.com/payments/3d-secure.md · https://docs.stripe.com/payments/3d-secure/authentication-flow.md | proprietária; destilado (a página traz um bloco dirigido a agentes: tratado como dado) | V-39 | 2026-10-10 |
| Stripe — Radar (índice) (8) | https://docs.stripe.com/radar | proprietária; destilado (só o índice foi lido) | V-40 | 2026-10-10 |
| Stripe — Currencies (8) | https://docs.stripe.com/currencies | proprietária; destilado | V-10 | 2026-10-10 |
| Stripe — skills oficiais (índice) e `stripe-best-practices/references/security.md` (8; score do arquivo 70) | https://docs.stripe.com/.well-known/skills/index.json · https://docs.stripe.com/.well-known/skills/stripe-best-practices/references/security.md | proprietária; destilado | V-41 | 2026-10-10 |
| Adyen — Dispute process and flow; Manage disputes (8) | https://docs.adyen.com/risk-management/understanding-disputes/dispute-process-and-flow.md · https://docs.adyen.com/risk-management/manage-disputes.md | proprietária; destilado | V-55 | 2026-10-10 |
| Mercado Pago — Chargebacks, gerenciamento (8) | https://www.mercadopago.com.br/developers/pt/docs/checkout-api-orders/payment-management/chargebacks/management | proprietária; destilado | V-56 | 2026-10-10 |
| Mercado Pago — Idempotency key obrigatória (8) | https://www.mercadopago.com.br/developers/en/news/2023/01/04/Idempotency-key-usage-will-be-mandatory | proprietária; destilado (datas ambíguas) | V-57 | 2026-10-10 |
| Asaas — Receba eventos no webhook; About webhooks (8) | https://docs.asaas.com/docs/receba-eventos-do-asaas-no-seu-endpoint-de-webhook · https://docs.asaas.com/docs/about-webhooks | proprietária; destilado | V-51 | 2026-10-10 |
| Asaas — Cobranças via boleto (8) | https://docs.asaas.com/docs/cobrancas-via-boleto | proprietária; destilado | V-52 | 2026-10-10 |
| Efí — Webhooks da API Pix (8) | https://dev.efipay.com.br/en/docs/api-pix/webhooks/ | proprietária; destilado | V-53 | 2026-10-10 |
| TigerBeetle — Data modeling; Two-phase transfers (8) | https://docs.tigerbeetle.com/coding/data-modeling/ · https://docs.tigerbeetle.com/coding/two-phase-transfers/ | repositório Apache-2.0; docs destilado | V-46 | 2026-10-10 |
| BCB — Manual de Padrões para Iniciação do Pix v2.10.0 (8) | https://www.bcb.gov.br/content/estabilidadefinanceira/pix/Regulamento_Pix/II_ManualdePadroesparaIniciacaodoPix.pdf | publicação oficial; destilado (URL montada pelo validador; conteúdo conferido) | V-44, V-65 | 2026-10-10 |
| bacen/pix-api — OpenAPI oficial do Pix (8–9) | https://github.com/bacen/pix-api · https://raw.githubusercontent.com/bacen/pix-api/master/openapi.yaml | Apache-2.0 | V-31, V-43 | 2026-10-10 |
| BCB — Voto 7/2026 (MED 2.0) (8) | https://normativos.bcb.gov.br/Votos/BCB/20267/Voto_do_BC_7_2026.pdf | publicação oficial; destilado | V-64 | 2026-10-10 |
| LGPD (Lei 13.709/2018), texto atualizado, Câmara (8) | https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html | lei; destilado | V-42 | 2026-10-10 |
| ANPD — Comunicação de incidente de segurança (8) | https://www.gov.br/anpd/pt-br/assuntos/incidente-de-seguranca | publicação oficial; destilado | V-30, V-42 | 2026-10-10 |
| PCI SSC — FAQ SAQ A × SAQ A-EP (9) | https://www.pcisecuritystandards.org/faqs/if-a-merchant-s-e-commerce-implementation-meets-the-criteria-that-all-elements-of-payment-pages-originate-from-a-pci-dss-compliant-service-provider-is-the-merchant-eligible-to-complete-saq-a-or-saq-a-ep/ | proprietária; destilado | V-62 | 2026-10-10 |
| Python — `decimal` (9) | https://docs.python.org/3/library/decimal.html | licença da página não lida; destilado | V-59 | 2026-10-10 |
| Oracle — Javadoc `BigDecimal` (Java 21) (9) | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/math/BigDecimal.html | proprietária; destilado (lido ~100 mil de 124 mil caracteres) | V-60 | 2026-10-10 |
| Martin Fowler — Money (PoEAA) (8) | https://martinfowler.com/eaaCatalog/money.html | direitos do autor; destilado | V-10 | 2026-10-10 |
| Anthropic — Claude Code permissions (8) | https://code.claude.com/docs/en/permissions | proprietária; destilado (lido em parte, ~262 mil caracteres) | V-18 | 2026-10-10 |
| Anthropic — Claude Code hooks e hooks-guide (8) | https://code.claude.com/docs/en/hooks · https://code.claude.com/docs/en/hooks-guide | proprietária; destilado (lido em parte) | V-19 | 2026-10-10 |
| Anthropic — Claude Code best practices (8) | https://code.claude.com/docs/en/best-practices | proprietária; destilado | V-20 | 2026-10-10 |
| anthropics/claude-code-security-review (8) | https://github.com/anthropics/claude-code-security-review | MIT (destilado; não copiado) | V-22 | 2026-10-10 |
| OWASP ASVS 5.0.0 (8) | https://owasp.org/www-project-application-security-verification-standard/ | CC BY-SA 4.0 (não permissiva pela regra da casa); só referência | V-25 | 2026-10-10 |

## Classe B

| Título | URL | Licença / tratamento | Itens | Consulta |
| --- | --- | --- | --- | --- |
| Stripe — Blog: Designing robust and predictable APIs with idempotency (Brandur Leach, 22/02/2017) (8) | https://stripe.com/blog/idempotency | direitos do autor; destilado | V-01 | 2026-10-10 |
| Mercado Pago — Webhooks (5) | https://www.mercadopago.com.br/developers/pt/docs/your-integrations/notifications/webhooks | proprietária; destilado (manifesto de `x-signature` ausente) | V-04 | 2026-10-10 |
| Pablo-aps/payments-engineering-skills (5; prompt-score 82–83; 1 estrela) | https://github.com/Pablo-aps/payments-engineering-skills | Apache-2.0; destilado (nada copiado) | V-02, V-05, V-08, V-11, V-12 | 2026-10-10 |
| rmoff — Claude Code isn't going to replace data engineers yet (11/03/2026) | https://rmoff.net/2026/03/11/claude-code-isnt-going-to-replace-data-engineers-yet/ | direitos do autor; destilado | V-08 | 2026-10-10 |
| Paymob — Paymob-AI-Integration-Skill (6; prompt-score 80) | https://github.com/PaymobAccept/Paymob-AI-Integration-Skill | MIT; destilado | V-14, V-66 | 2026-10-10 |
| Mercado Pago — marketplace Claude, skill `mp-review` (7; prompt-score 85) | https://raw.githubusercontent.com/mercadopago/mercadopago-claude-marketplace/main/plugins/mercadopago/skills/mp-review/SKILL.md | Apache-2.0; destilado (hooks e marketplace **não instalar**) | V-15 | 2026-10-10 |
| Simon Willison — The lethal trifecta (16/06/2025) (5) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | direitos do autor; destilado | V-16 | 2026-10-10 |
| OWASP — Logging Cheat Sheet (5) | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | licença não lida nesta página (a de Input Validation mostra CC BY-SA 4.0); destilado | V-23 | 2026-10-10 |
| OWASP — Input Validation Cheat Sheet (5) | https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html | CC BY-SA 4.0; destilado | V-24 | 2026-10-10 |
| github/awesome-copilot — `security-and-owasp.instructions.md` (6; prompt-score 67) | https://github.com/github/awesome-copilot/blob/main/instructions/security-and-owasp.instructions.md | MIT (repositório); destilado | V-26 | 2026-10-10 |
| brexhq/prompt-engineering (6; era GPT-4) | https://github.com/brexhq/prompt-engineering | MIT; destilado | V-27 | 2026-10-10 |
| AllanOps/Clean-Backend (5; prompt-score 75) | https://github.com/AllanOps/Clean-Backend | MIT; destilado | V-28 | 2026-10-10 |
| PCI SSC — Document library (5) | https://www.pcisecuritystandards.org/document_library/ | proprietária; só a lista de documentos | V-29 | 2026-10-10 |
| Stripe — `stripe/agent-toolkit` e `docs.stripe.com/skills.md` (6) | https://raw.githubusercontent.com/stripe/agent-toolkit/main/README.md · https://docs.stripe.com/skills.md | MIT (README); destilado | V-32 | 2026-10-10 |
| Pagar.me — Boleto (6) | https://docs.pagar.me/reference/boleto-1.md (índice https://docs.pagar.me/llms.txt) | proprietária; destilado | V-36 | 2026-10-10 |
| Pagar.me — Webhooks, visão geral, Segurança (6) | https://docs.pagar.me/docs/webhooks.md · https://docs.pagar.me/reference/visão-geral-sobre-webhooks.md · https://docs.pagar.me/reference/segurança-1.md | proprietária; destilado (**sem assinatura documentada**) | V-37 | 2026-10-10 |
| Pagar.me — Pix, settlements e disputas (6) | https://docs.pagar.me/reference/pix-2.md · https://docs.pagar.me/reference/objeto-settlements.md · https://docs.pagar.me/reference/disputas.md | proprietária; destilado | V-38 | 2026-10-10 |
| Open Finance Brasil — portal do desenvolvedor (6) | https://openfinancebrasil.atlassian.net/wiki/spaces/OF/overview | proprietária; só estrutura | V-45 | 2026-10-10 |
| Open Finance Brasil — FAPI-BR v2.1.0 (6) | https://openfinancebrasil.atlassian.net/wiki/spaces/OF/pages/1334149240/EN+Open+Finance+Brasil+Financial-grade+API+Security+Profile+-+v2.1.0 | proprietária; destilado (seção 5.1 apenas) | V-69 | 2026-10-10 |
| Modern Treasury — Ledgers overview (5) | https://docs.moderntreasury.com/ledgers/docs/ledgers-overview | proprietária; visão geral apenas | V-46 | 2026-10-10 |
| IETF — draft-ietf-httpapi-idempotency-key-header-00 (6) | https://greenbytes.de/tech/specs/draft-ietf-httpapi-idempotency-key-header-00.html | rascunho de 2021, expirado, **não é norma**; destilado | V-58 | 2026-10-10 |
| Anthropic — Building effective agents (19/12/2024) (6) | https://www.anthropic.com/engineering/building-effective-agents | proprietária; destilado | V-21 | 2026-10-10 |

## Classe C e rebaixados

| Título | Uso permitido | Itens |
| --- | --- | --- |
| theigwe/moneyproof (4; MIT; 1 estrela) | estrutura e corroboração das 10 regras; a regra "nunca números JSON" é autocontraditória | V-13 |
| Hainrixz/agente-pagokit (4; MIT; 63 estrelas) | só o padrão de roteiro de teste de webhook; **hooks Node não instalar** | V-06 |
| wshobson/agents `payment-processing` (4; MIT; ~40,3 mil estrelas) | contraexemplo (`pci-compliance` score 47: guarda PAN cifrado) e corroboração de webhook (`payment-integration` score 57) | rebaixado |
| OpenAI — GPT-5 prompting guide (arquivado) (4) | corroboração do princípio de confirmação; sem licença | V-17 |
| awesome-cursorrules `google-adk.mdc` (CC0; 4) | corroboração de "ferramenta valida argumentos" | V-16 |
| Stigg, "Best practices I wish we knew when integrating Stripe webhooks" (HN, 2022; 22 pontos) | sinal fraco de comunidade | rebaixado |
| Pagar.me marketplace (3), medici (4), Sanity (4), banco-inter-api-skill (4), cfokit (4) | pistas ou corroboração; ver notas em `VALIDATED.md` | rebaixados |

## Conteúdo próprio e workflows de terceiros

| Material | Licença | Uso |
| --- | --- | --- |
| `francisco-efjr/brain-of-agent` — `brains/qa/references/dominios.md` (Pagamentos, Pix, Boleto, Cartão, Dados/ETL, Microsserviços, Documentos, Datas, Fusos) | MIT (conteúdo próprio do usuário) | tabelas de casos e SQL de fechamento incorporados e adaptados, com atribuição; números regulatórios **Não verificados** (V-33) |
| `brains/qa/scripts/documentos_br.py` | MIT | usado pela skill `payment-test-plan` (CPF, CNPJ alfanumérico) apenas em teste |
| `brains/fullstack/assets/templates/{handoff-checkpoint,adr,plano-incremento}.md` | MIT | base dos templates `handoff-checkpoint.md`, `adr-pagamentos.md`, `plano-incremento-financeiro.md` |
| V-34 (bloco de CLAUDE.md) e V-35 (revisor) | texto do projeto, MIT | adaptados; escritos pelo validador (não independentes) |
| gstack (Garry Tan e contribuidores, MIT) | MIT | somente inspiração do formato de achado e da regra de causa raiz; nada copiado em bloco |

## Rejeitados

| Item | Motivo |
| --- | --- |
| Skills Stripe `stripe-pay`, `stripe-projects`, `stripe-directory` | enviam fundos, provisionam credenciais ou impõem consulta a si mesmas (V-41) |
| `agent-card-skill` | instala pacote npm global e pede código de login no chat |
| aitmpl "guardrails de git" | afirmação de bloqueio de `.env` e comandos destrutivos refutada; instalação por `npx` |
| R-gap2-08 (idempotência Pagar.me, artigo institucional da Stone) | não é documentação; matriz usa "não verificável" |
| R-gap2-16 (Pix Automático por imprensa) | nenhuma fonte primária; mantido só como lista de perguntas |
| R-gap2-23 (skills comunitárias de pagamento, agregadores) | sem repositório, licença nem data |
| Resultados "pix" de pixel-art, internet-court, ag402, ecommerce-cia, uzbekistan-payment-skills, brasil-legal-skills | licença NOASSERTION, fora do escopo ou falso positivo |

## Lacunas conhecidas

Resumo; o registro vivo, com como fechar cada uma, está em [lacunas-e-nao-verificado.md](lacunas-e-nao-verificado.md): PCI DSS (requisitos numerados), KYC/AML Brasil, Manual de Segurança do Pix, Regulamento e IN BCB 766/746, Pix Automático (limites), norma de boleto, layouts de Cielo/Rede/Stone, assinatura e idempotência do Pagar.me, manifesto `x-signature` do Mercado Pago, FAPI-BR além da seção 5.1, COF/EMVCo, guias do Modern Treasury e da Formance, vetores de Java, lente de comunidade.
