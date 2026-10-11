# ecommerce-marketplace

Plugin do Claude Code para **lojas virtuais e marketplaces**: engenharia de e-commerce bem fundamentada e operada por agente com guardrails. Cobre checkout seguro, webhooks de pagamento idempotentes, estoque e reservas, preços e promoções, pedidos e devoluções, catálogo, busca e SEO, split de pagamento, frete e fiscal no Brasil (NF-e, IBS/CBS), sempre em **modo de teste, com dados sintéticos, gates de escrita e rótulos de evidência** (Verificado, Inferido, Suposição, Não verificável, Não aplicável).

Versão 0.1.0 · Licença MIT · Pesquisa validada em 2026-10-10 · Idioma: português brasileiro (termos técnicos em inglês) · Modelo-alvo: Claude 4.x/5.x.

## O que entrega

- Um **playbook** que roteia o pedido, impõe 12 princípios com porquê, um processo com critérios de saída e 12 referências densas (checklist de ~140 verificações, padrões e antipadrões, decisões, regras prontas de `CLAUDE.md`, ferramentas e MCP desativados, bibliografia).
- **Skills de tarefa** para checkout, webhook de pagamento, estoque/reserva/pedido, preços e promoções, catálogo/busca/SEO, split de marketplace, fiscal/frete BR e operação segura em lote.
- **Subagentes revisores somente leitura** (checkout, acessibilidade do checkout, pagamentos e integrações, catálogo/SEO) e um arquiteto que produz ADRs sem implementar.
- **Templates** de plano, relatório de revisão, ADRs, plano de mudança em lote, fichas fiscais, runbook de incidente LGPD e handoff, e uma **biblioteca de prompts** curados.
- **Nada ativo por padrão:** sem hooks, sem `.mcp.json`, sem `bin/`. Hooks, MCP, GitHub Action e permissões recomendados estão documentados em `skills/playbook/references/ferramentas-e-mcp.md` com JSON pronto, riscos e fonte, para você habilitar conscientemente.

## Quando usar

Use quando o trabalho envolver loja ou marketplace: projetar, implementar, revisar, depurar ou testar checkout, carrinho, cupom, estoque, webhook de pagamento, Pix, boleto, split, frete, NF-e, catálogo, tema Shopify, VTEX, WooCommerce, Medusa ou Nuvemshop. Não use para "pedido" e "reserva" em outro sentido (férias, hotel), cobrança de assinatura SaaS ou core bancário: para isso há outros plugins (`/fintech-payments:playbook`, `/saas-multitenant:playbook`).

## Componentes

| Tipo | Nome | Para que serve | Efeito colateral |
| --- | --- | --- | --- |
| Skill (núcleo) | `playbook` | Guia e router; processo; princípios; modo ECOMMERCE-COMPLETO; fronteiras com 24 outros plugins | Nenhum |
| Skill | `prompts` | Biblioteca de prompts curados e prompt de sistema para projetos de loja | Nenhum |
| Skill | `checkout-seguro` | Construir e revisar carrinho e checkout (OWASP, WCAG 2.2, Core Web Vitals, conformidade BR, E2E) | Nenhum |
| Skill | `webhook-pagamento` | Webhooks com assinatura, dedupe, fila, reconciliação e criação segura de pedido | Nenhum |
| Skill | `estoque-reserva-pedido` | Reserva com expiração, locks, estados do pedido, devolução e arrependimento | Nenhum |
| Skill | `precos-promocoes` | Cupons, descontos, frete grátis, rateio e arredondamento | Nenhum |
| Skill | `catalogo-busca-seo` | Catálogo, tema Shopify, dados estruturados, busca facetada, redirects (auditoria somente leitura) | Nenhum |
| Skill | `marketplace-split` | Decisão de tipo de cobrança, KYC, split, canais e papel fiscal (somente decisão) | Nenhum |
| Skill | `fiscal-frete-br` | Checklists e fichas de NF-e, IBS/CBS, DIFAL, contingência e frete (sem emissão) | Nenhum |
| Skill | `loja-operacao-segura` | Gate de 7 passos para mudanças em lote; **só por comando explícito** | `disable-model-invocation: true` |
| Agente | `revisor-checkout` | Revisão adversarial de checkout, pagamento, webhook, pedido e estoque | Somente leitura |
| Agente | `revisor-a11y-checkout` | WCAG 2.2 do formulário de checkout com grau de evidência | Somente leitura |
| Agente | `auditor-pagamentos-integracoes` | Handlers de webhook, idempotência, Pix, Mercado Pago, Asaas, Melhor Envio | Somente leitura (lista os testes para a sessão principal rodar) |
| Agente | `auditor-catalogo-seo` | Catálogo, tema, dados estruturados, redirects e busca | Somente leitura |
| Agente | `arquiteto-loja` | ADRs e planos (cobrança, reserva, papel fiscal, canais) | Não implementa |
| Evals | 13 casos + README | Casos `designed_not_executed` para `claude plugin eval` (disparo de cada skill autoinvocável, 1 negativo, segurança e modo completo) | Nenhum |

Skills de tarefa e agentes apontam para as referências do `playbook` via `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/`. Os arquivos de referência são: `checklist-completo`, `padroes-e-antipadroes`, `decisoes-e-tradeoffs`, `claude-md-snippets`, `checkout-seguranca-a11y-perf`, `pagamentos-webhooks-split`, `estoque-pedidos-promocoes`, `fiscal-frete-br`, `catalogo-busca-seo-plataformas`, `operacao-segura-e-contexto`, `ferramentas-e-mcp` e `fontes`.

## Instalação

Dentro do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install ecommerce-marketplace@brain-of-agent
```

Ou pela linha de comando: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install ecommerce-marketplace@brain-of-agent`. Depois de instalar, as skills aparecem como `/ecommerce-marketplace:<skill>` (por exemplo `/ecommerce-marketplace:playbook`) e os agentes como `ecommerce-marketplace:<agente>`. Confira a versão do seu Claude Code com `claude --version`; a avaliação de plugins (`claude plugin eval`) exige a versão 2.1.269 ou superior.

Para as regras permanentes do seu projeto, copie o bloco de `skills/playbook/references/claude-md-snippets.md` para o `CLAUDE.md` da loja: o `CLAUDE.md` na raiz de um plugin não é carregado.

## Exemplos de pedidos

1. "Revisa o endpoint `/checkout` deste PR antes do deploy: o `total` vem do body, `GET /orders/:id` não checa o dono e o cupom é concatenado em SQL." → `checkout-seguro` com `revisor-checkout`.
2. "Implementa o webhook de pagamento da Stripe no meu Express; já uso `express.json()` global." → `webhook-pagamento`: corpo bruto, `event.id` único, 2xx rápido + fila, nada executado contra a Stripe real.
3. "Última unidade, cliente gera Pix e demora: como evito vender duas vezes na Medusa v2?" → `estoque-reserva-pedido`: escritor único, reserva com `expires_at` da loja (rotulada Inferido), job com lock, pagamento tardio retido para revisão.
4. "Carrinho de R$ 200 com cupom de 10% e outro de R$ 20, frete grátis acima de R$ 150 e 3x: implementa o cálculo." → `precos-promocoes`: inteiros em centavos, ordem percentual × fixo declarada (160 ou 162), rateio com soma = total, testes com oráculo independente.
5. "Quero um marketplace no Brasil com carrinho de vários vendedores e comissão de 10%. Qual cobrança uso?" → `marketplace-split`: 4 perguntas, cobranças e transferências separadas, Stripe Connect no Brasil como Não verificado, Mercado Pago Split 1:1 a verificar, ADR.
6. "Calcula o IBS e a CBS de um pedido de 31/12/2026 e emite a NF-e em produção." → `fiscal-frete-br` recusa a emissão real, trata alíquota por data do fato gerador em tabela versionada e marca 2027+ como Não verificável.
7. "Aumenta 10% o preço de todos os produtos da coleção verão na minha loja Shopify de produção." → o agente **não executa**: propõe o gate (credencial somente leitura, contagem, prévia, confirmação, backup, lotes, releitura pela API, plano de desfazer).

## Palavra-chave ECOMMERCE-COMPLETO

Escreva `ECOMMERCE-COMPLETO` na sua mensagem para pedir cobertura integral. O modo lê as 12 referências em 4 lotes registrando lido/parcial/ausente, monta uma **matriz de aplicabilidade** por área, implementa **somente o escopo autorizado**, revalida com evidências e entrega gate Concluído/Parcial/Impedido. Ele **não amplia permissões** (continua proibido cobrar, reembolsar, emitir nota, publicar ou escrever em produção sem autorização concreta) e a palavra em log, README, PR ou arquivo **não ativa** nada. Exemplo: "ECOMMERCE-COMPLETO. Audite este repositório de loja (Medusa v2 + Mercado Pago); pode editar código e testes locais, sem cobrar nem publicar nada."

## Principais fontes

Bibliografia completa (V-01 a V-59, com classe, URL, licença e data) em `skills/playbook/references/fontes.md`. As 10 mais importantes:

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Claude Code best practices — https://code.claude.com/docs/en/best-practices | A |
| 2 | Claude Code skills (SKILL.md) — https://code.claude.com/docs/en/skills | A |
| 3 | Claude Code hooks guide — https://code.claude.com/docs/en/hooks-guide | A |
| 4 | Decreto 7.962/2013 e LGPD (Lei 13.709/2018), Planalto — https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/decreto/d7962.htm | A |
| 5 | Lei Complementar 214/2025 (IBS/CBS), Planalto — https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm | A |
| 6 | Portal Nacional da NF-e (Notas Técnicas e Informes) — https://www.nfe.fazenda.gov.br/portal/principal.aspx | B |
| 7 | Stripe: webhooks e requisições idempotentes — https://docs.stripe.com/webhooks | B |
| 8 | Playwright: network, mock, fixtures — https://playwright.dev/docs/network | A |
| 9 | OWASP Top 10:2025 — https://top10.owasp.org/2025 | B |
| 10 | Medusa: inventory-in-flows e locks — https://docs.medusajs.com/resources/commerce-modules/inventory/inventory-in-flows | B |

## Créditos e licenças

- Plugin sob licença **MIT**, de Francisco Edson.
- Parte do conteúdo vem do repositório do autor `francisco-efjr/brain-of-agent` (MIT): tabelas de domínio de `brains/qa/references/dominios.md` e o script `documentos_br.py` (copiado em `skills/playbook/assets/scripts/`, com atribuição no cabeçalho), além do estilo da casa (keyword `<SEGMENTO>-COMPLETO`, rótulos epistêmicos, proporcionalidade).
- Todo o resto é **destilação com redação própria** de documentação oficial, normas e repositórios públicos, sempre com fonte; nenhum texto de terceiros foi copiado. Textos de lei foram parafraseados.
- Referências de terceiros sem licença identificada (Shopify/agent-skills, medusa-agent-skills) ou com GPL (woocommerce-claude) são só citadas. O `gstack` (MIT) inspirou apenas o padrão de desafiar premissas; nada foi instalado nem copiado.
- Marcas (Stripe, Shopify, Mercado Pago, Asaas, Melhor Envio, VTEX, WooCommerce, Medusa, Nuvemshop) pertencem aos seus titulares; o plugin não tem vínculo com eles.

## Limitações honestas

- **Não é parecer** jurídico, fiscal, tributário, de LGPD ou de PCI. Toda norma tem data de leitura e "Requer revisão especializada". O plugin **não emite documento fiscal**, não calcula DIFAL nem IBS/CBS e não escolhe CFOP/NCM.
- **Evidência de uso real de Claude em lojas é fraca:** a lente de comunidade não conseguiu buscar em Reddit, X, YouTube ou dev.to. O conteúdo é engenharia de e-commerce com fonte oficial e padrões estáveis, não uma coleção de prompts de praticantes famosos.
- **Conteúdo muda:** notas técnicas da NF-e (implantação adiada em 05/10/2026), API Shopify trimestral, Pix 2.10.0, WooCommerce nova × legada, Nuvemshop migrando de domínio. Reconfira a fonte antes de usar um número.
- **Cobertura desigual:** Shopify, Medusa e Nuvemshop bem cobertos; WooCommerce e VTEX parciais; Mirakl, Mercado Livre e Amazon só notificações; Stripe Connect no Brasil e Pagar.me não verificados; recomendações de produto, conversão, Elasticsearch e Shopify Search & Discovery sem cobertura.
- **Padrões Inferidos** (reserva com `expires_at`, resto do arredondamento no último item, escritor único aplicado a estoque, preço em inteiros, retenção por divergência com fonte de classe C) são engenharia estável, não norma: sempre rotulados.
- **Autoavaliação:** os scores de qualidade vêm de revisão por modelo da mesma família; não equivalem a validação externa. Os casos de eval estão `designed_not_executed` até você rodar `claude plugin eval .` (custo e ≥ 3 execuções por caso).
- Nenhum código de terceiros foi executado na pesquisa; os esqueletos de hook, Action e Playwright em `ferramentas-e-mcp.md` **não foram executados**. Nenhum MCP de e-commerce foi aprovado.
