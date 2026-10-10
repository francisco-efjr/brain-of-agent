# fintech-payments — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Segmento com cobertura fraca; normas e provedores exigem fonte primária própria. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| FastAPI production architecture (CT-07) | https://github.com/PatrickJS/awesome-cursorrules | B | "Every side-effect operation accepts an idempotency_key: UUID. Look up before retrying."; "single writer" por domínio; bulkhead por provedor. CC0, literais Verificados. |
| security-and-owasp (CT-16) | https://github.com/github/awesome-copilot | B | "Always verify webhook signatures (Stripe, GitHub HMAC, etc.)."; níveis de severidade. MIT. |
| claude-code-security-review (AO-24) | https://github.com/anthropics/claude-code-security-review | A | Metodologia; ressalva do atlas: exclusões (ex.: rate limiting) podem não servir a fintech. MIT. |
| GPT-5 guide: limiares de confirmação por risco (PC-02) | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide | A | Checkout/pagamento exigem confirmação antes de qualquer outra ação. Guia arquivado (MIT cookbook). |
| Brex Prompt Engineering Guide (PC-29) | https://github.com/brexhq/prompt-engineering | B | Nunca fine-tuning com dados reais de cliente; conteúdo de prompt pode ser visto pelo usuário. MIT. |
| wshobson/agents, `payment-processing` (EC-10) | https://github.com/wshobson/agents | B | Plugin citado; abrir e verificar. |
| Google ADK .mdc (CT-11) | https://github.com/PatrickJS/awesome-cursorrules | B | "Validate tool arguments before performing side effects."; controle de acesso em código. CC0. |
| Willison, lethal trifecta (PC-21) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | A | Agentes com acesso a dados financeiros. |
| Hooks guardrail (CP-19) | https://aitmpl.com/blog/secure-git-workflow/ | B | Negar leitura de `.env` e comandos destrutivos. |
| Sanity (CP-22) | https://www.sanity.io/blog/first-attempt-will-be-95-garbage | B | Produção nunca conectada ao agente. |
| rmoff (CP-26) | https://rmoff.net/2026/03/11/claude-code-isnt-going-to-replace-data-engineers-yet/ | B | Reconciliação de contagens como base para conciliação financeira (Inferido). |
| Cursor/Copilot regras de segurança (CT-13) | https://github.com/PatrickJS/awesome-cursorrules | B | Sem segredos hardcoded; nova dependência com aprovação; log sem dados sensíveis. CC0. |

## 2. Repositórios e arquivos a abrir
- `PatrickJS/awesome-cursorrules/rules/fastapi-production-architecture-…mdc`, `security-devsecops-ssdls-appsec.mdc`, `google-adk.mdc`.
- `github/awesome-copilot/instructions/security-and-owasp.instructions.md`.
- `wshobson/agents/plugins/payment-processing`.
- Snapshot do brain: `brains/qa/references/dominios.md`, `brains/qa/scripts/documentos_br.py`.
- Docs de Pix (BACEN), PCI-DSS, Stripe, Adyen, Mercado Pago, Pagar.me, Open Finance, KYC/AML, ledger de partidas dobradas não estão no atlas: lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-24, AO-23, AO-10, AO-09; nenhum material Anthropic específico de pagamentos aprovado.

## 4. Padrões da comunidade
- Nenhum relato de praticante aprovado (lacuna declarada em CP).
- Idempotência, assinatura de webhook e escopo por usuário como invariantes em código (CT-07, CT-16).
- Confirmação explícita antes de efeitos financeiros (PC-02).

## 5. O que o brain-of-agent já oferece
- `brains/qa/references/dominios.md` (Pix, boleto, cartão como sementes, "não verificado") e `brains/qa/scripts/documentos_br.py` (validar contra a norma oficial antes de confiar).
- BR-08 (BVA, tabela de decisão, estados, pairwise para valores e arredondamento), BR-09 (normas em transição: CBS-IBS, CNPJ alfanumérico; primária gov.br Não verificável), BR-10.
- BR-14: OWASP e ASVS (ASVS Não verificado).
- BR-03: modo `FINTECH-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte para ledger, representação de dinheiro, conciliação, chargeback, antifraude, KYC/AML, PCI-DSS, BACEN, Open Finance, LGPD.
- Regras BR do brain são sementes não verificadas.
- Plugin não deve executar pagamentos, chamar APIs reais nem manipular dados de cartão; testes só com modo de teste do provedor e dados sintéticos.
- Nenhuma orientação de investimento ou consultoria financeira personalizada.
