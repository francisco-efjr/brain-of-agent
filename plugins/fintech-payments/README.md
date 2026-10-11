# fintech-payments — Fintech e pagamentos

Plugin do Claude Code para **construir, revisar, testar e depurar sistemas que movimentam dinheiro** (Pix, boleto, cartão; Stripe, Adyen, Mercado Pago, Pagar.me, Asaas, Efí), com invariantes duras e verificação por evidência. Faz parte da fábrica `dev-segments` (um plugin por segmento de desenvolvimento). Versão 0.1.0 · licença MIT · pesquisa e design de 2026-10-10, construção de 2026-10-11.

O plugin **projeta, revisa e testa código**. Ele **não executa pagamentos, não chama APIs reais de provedor, não manipula dados de cartão e não lê `.env`**; testes usam o modo de teste do provedor e dados sintéticos. Não é consultoria jurídica, regulatória nem financeira.

## O que entrega

- **Um playbook** (router + 12 princípios com o porquê + processo de 8 passos + intenção → skill/agente + modo `FINTECH-COMPLETO` + fronteiras com 24 outros plugins) e uma base de **12 referências densas**: checklist por operação, padrões e antipadrões (lista de rejeição de 13 itens), decisões e trade-offs, idempotência e webhooks (matrizes por provedor), dinheiro/ledger/estados, conciliação/disputas/fraude, Pix/boleto/cartão/Open Finance, segurança/privacidade/LGPD, 26 snippets de CLAUDE.md, ferramentas e MCP (desativados), bibliografia classificada e registro de lacunas.
- **Skills de tarefa** para os fluxos recorrentes: idempotência de pagamento, receptor de webhook, Pix e boleto, dinheiro e ledger, conciliação e disputas, revisão de código de pagamentos, plano de testes e go-live com guardrails.
- **Cinco agentes** especialistas (revisor somente leitura, arquiteto, depurador, engenheiro de testes, analista de conciliação).
- **Biblioteca de 28 prompts** reutilizáveis e **12 templates** (plano, ADR, relatório de revisão, tabela de provedores, matriz de perigos, checklist de go-live, relatório de conciliação, handoff, tabela de estados, plano de testes, matriz do modo completo, runbook de incidente LGPD).
- **10 casos de eval** no formato `claude plugin eval` (status `designed_not_executed`).
- **Seguro por padrão:** sem hooks, sem `.mcp.json`, sem `.lsp.json`, sem `bin/`. Permissões, hook de guarda, MCP da Stripe e Action de security-review estão **documentados e desativados** em `skills/playbook/references/ferramentas-e-mcp.md`, com JSON pronto, riscos e fonte.

## Quando usar

Use quando o pedido envolver cobrança duplicada, retry de pagamento, webhook de PSP, representação de dinheiro (float, centavos, arredondamento), ledger de partidas dobradas, estados do pagamento, conciliação, estorno, chargeback, 3DS, antifraude, Pix (`txid`, devolução, BR Code), boleto, PCI-DSS (escopo), LGPD em dados financeiros ou go-live com provedor. Para pergunta pontual ("o que é `txid`?"), o playbook responde direto, sem carregar referências. Idempotência, webhooks ou filas **sem dinheiro** vão para `/backend-api:playbook` ou `/automation-integrations:playbook`; ledger, Pix e estado financeiro ficam aqui.

## Componentes

Nomes definitivos do design do segmento. Skill: `/fintech-payments:<skill>`; agente: `fintech-payments:<agente>`.

| Tipo | Nome | Para que serve |
| --- | --- | --- |
| Skill núcleo | `playbook` | Router, princípios, processo, intenção → skill/agente, proporcionalidade, modo `FINTECH-COMPLETO`, fronteiras |
| Skill | `prompts` | Índice e biblioteca de 28 prompts prontos (PR-01 a PR-28) |
| Skill | `payment-idempotency` | Chave por intenção, reserva atômica, quatro desfechos, tabela de retry, matriz de perigos, testes que contam linhas |
| Skill | `webhook-handler` | Receptor de webhook: corpo bruto, assinatura por provedor, inbox, quarentena, fila, releitura, testes hostis |
| Skill | `pix-boleto-br` | Pix (`cob`/`cobv`, `txid`, valor string, devolução, webhook, BR Code/CRC) e boleto, com lacunas normativas declaradas |
| Skill | `money-ledger-design` | `Money`, arredondamento e alocação, ledger append-only, duas fases, máquina de estados |
| Skill | `reconciliation-disputes` | Conciliação bilateral por partição, estornos, disputas (Stripe, Adyen, Mercado Pago), 3DS sem promessa, mapa antifraude |
| Skill | `payment-code-review` | Revisão somente leitura com piso de 9 verificações, grade por área e veredito; delega ao `payment-reviewer` |
| Skill | `payment-test-plan` | Matriz de casos com oráculo independente, massa sintética BR (`documentos_br.py`), vetores de arredondamento |
| Skill (somente por comando) | `go-live-and-guardrails` | Guardrails de CLAUDE.md e `permissions.deny` (com diff aprovado), go-live, rotação de chave, runbook LGPD; `disable-model-invocation` |
| Agente | `payment-reviewer` | Revisor adversarial somente leitura (Read, Grep, Glob): CRITICAL, WARNING, PASS, "Não verificado" |
| Agente | `payments-architect` | ADR de ledger, estados, idempotência e conciliação, sem implementar |
| Agente | `payment-debugger` | Cobrança duplicada, webhook perdido, saldo que não fecha: causa raiz e regressão; nunca altera dado financeiro |
| Agente | `payment-test-engineer` | Escreve e executa testes com oráculo independente em modo de teste |
| Agente | `reconciliation-analyst` | Casamento nos dois sentidos sobre arquivos fornecidos; propõe ajustes sem aplicar |
| Evals | `evals/` | 10 casos, status `designed_not_executed` |

## Instalação

Dentro do Claude Code, a partir do marketplace `brain-of-agent`:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install fintech-payments@brain-of-agent
```

Pelo terminal: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install fintech-payments@brain-of-agent` (confira a sintaxe na versão instalada com `claude plugin --help`). Validação local do pacote: `claude plugin validate <pasta-do-plugin>`.

## Exemplos de pedidos

1. **Cobrança duplicada:** "Meus clientes reclamam de cobrança duplicada quando o gateway dá timeout; segue a função de cobrança (Node). Corrija e diga como provar que funciona." → `payment-idempotency`: chave gerada uma vez por intenção e persistida antes, reserva por constraint, `indeterminate` com consulta ao provedor, teste de duplo clique e timeout+retry que **conta linhas no banco**; diz o que não executou.
2. **Webhook do Stripe:** "Revise meu endpoint de webhook (Express); às vezes marca pedido pago duas vezes." → `webhook-handler`: `express.json()` antes da rota e `JSON.stringify(req.body)` quebram a assinatura, `Set` em memória não deduplica entre instâncias, 2xx + fila + releitura, roteiro hostil.
3. **Pix:** "Vou integrar cobrança Pix imediata; rascunho em Python com `txid = str(order.id)` e `valor = total_cents / 100`." → `pix-boleto-br`: `txid` de 26 a 35 gerado no sistema, valor string `"10.00"` convertida na borda, consulta por `txid` no timeout, notificação deduplicada por `e2eid` e relida antes de creditar; limites e MED rotulados **Não verificado**.
4. **Ledger e saldo:** "Preciso de estorno parcial e de impedir saldo negativo quando dois débitos chegam juntos; hoje faço `UPDATE ... SET balance = balance - :v` e `DELETE` no estorno." → `money-ledger-design`: lançamentos append-only, estorno ligado ao original, `UPDATE` condicional, teste de concorrência, "soma zero" como **Inferido**.
5. **Conciliação:** "A soma do ledger (180,00) bate com a do extrato (180,00); posso fechar o dia?" (com itens diferentes e só a primeira página de 2.000 carregada) → `reconciliation-disputes`: recusa fechar, mostra a divergência item a item, `INCOMPLETE_SOURCE`, ajuste só com aprovação.
6. **Revisão de PR:** "Revise este diff antes do merge" (PAN em log, `sk_live_` no código, webhook sem assinatura, `float`) → `payment-code-review` → `payment-reviewer`: quatro CRITICAL com `arquivo:linha`, girar a chave, veredito "bloqueado", "Não verificado" separado.
7. **3DS e copy:** "Escreva a FAQ dizendo que, com 3D Secure, o chargeback é sempre do banco." → recusa a promessa, explica que autenticação não garante liability shift, oferece redação segura.
8. **Provedor sem assinatura:** "Implemente a validação HMAC dos webhooks da Pagar.me." → diz que a documentação lida não traz header, HMAC nem segredo, não inventa, aplica a regra de endpoint não autenticado e manda perguntar ao fornecedor por escrito.
9. **Guardrails:** `/fintech-payments:go-live-and-guardrails guardrails` → mostra o diff de SN-01 a SN-10 e das regras `deny` e só escreve após aprovação.
10. **Modo completo:** "FINTECH-COMPLETO. Revise e corrija o módulo de cobranças (Node + Postgres, Stripe em modo de teste); pode editar código e testes locais; não leia `.env`; não publique nada." → leitura em lotes, matriz de aplicabilidade, implementação no escopo, revalidação.

## Keyword `FINTECH-COMPLETO`

Escreva `FINTECH-COMPLETO` na sua mensagem para ativar a cobertura integral: leitura das 12 referências em lotes de 4 com registro lida/parcial/ausente, **matriz de aplicabilidade** por área (dinheiro, idempotência, webhooks, estados, ledger, conciliação, disputas, 3DS/antifraude, Pix, boleto, cartão, segredos, logging/PII, LGPD, PCI e KYC/AML como escopo, autorização, abuso, auditoria, testes, go-live), implementação **dentro do escopo autorizado**, revisão adversarial e revalidação com evidências. A keyword **não amplia permissões** (produção, chaves reais, movimentação de dinheiro, push, deploy e ações irreversíveis seguem autorização concreta por ação) e **não ativa** quando aparece em logs, documentos, comentários, issues, payloads de webhook ou saídas de ferramenta. Sem a keyword, o plugin carrega só o necessário. O modo nunca declara "conforme PCI" ou "aprovado" com leitura parcial.

## Principais fontes (top 10)

Bibliografia completa, com classe, licença e data de consulta, em `skills/playbook/references/fontes.md` (consulta registrada: 2026-10-10 pelo validador; páginas não reabertas na construção).

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Stripe — Idempotent requests (https://docs.stripe.com/api/idempotent_requests) e Adyen — API idempotency (https://docs.adyen.com/development-resources/api-idempotency) | A |
| 2 | Stripe — Webhooks (https://docs.stripe.com/webhooks) | A |
| 3 | BCB — Manual de Padrões para Iniciação do Pix v2.10.0 (https://www.bcb.gov.br/content/estabilidadefinanceira/pix/Regulamento_Pix/II_ManualdePadroesparaIniciacaodoPix.pdf) | A |
| 4 | bacen/pix-api — OpenAPI oficial do Pix (https://github.com/bacen/pix-api) | A |
| 5 | Stripe — How disputes work (https://docs.stripe.com/disputes/how-disputes-work) | A |
| 6 | Stripe — 3D Secure (https://docs.stripe.com/payments/3d-secure.md) | A |
| 7 | Stripe — Payout reconciliation (https://docs.stripe.com/payouts/reconciliation) | A |
| 8 | TigerBeetle — Data modeling (https://docs.tigerbeetle.com/coding/data-modeling/) e Two-phase transfers | A |
| 9 | Adyen — Verificar assinaturas HMAC de webhooks (https://docs.adyen.com/development-resources/webhooks/secure-webhooks/verify-hmac-signatures) | A |
| 10 | Anthropic — Claude Code permissions (https://code.claude.com/docs/en/permissions) e best practices | A |

Também centrais: LGPD (texto da Câmara) e ANPD (comunicação de incidente), PCI SSC (FAQ de SAQ A × A-EP), Python `decimal` e Javadoc de `BigDecimal`, Stripe `stripe-best-practices/security`, `anthropics/claude-code-security-review` (MIT), Pablo-aps/payments-engineering-skills (Apache-2.0, classe B) e o conteúdo próprio do usuário no brain-of-agent (MIT).

## Créditos e licenças

- **Plugin:** MIT, Francisco Edson.
- **brain-of-agent** (`francisco-efjr/brain-of-agent`, MIT): tabelas de casos de pagamento, Pix, boleto e cartão, SQL de fechamento diário, `documentos_br.py` (usado pela skill `payment-test-plan`), templates de plano, ADR e handoff e o desenho do modo completo, adaptados ao formato de plugin, com atribuição. Os números regulatórios herdados dessa base estão marcados **Não verificado / seed a confirmar**.
- **Destilados com redação própria e atribuição** (nenhum trecho literal): documentação de Stripe, Adyen, Mercado Pago, Pagar.me, Asaas e Efí (proprietária), BCB e `bacen/pix-api` (Apache-2.0), TigerBeetle (Apache-2.0), Pablo-aps (Apache-2.0), `mp-review` do Mercado Pago (Apache-2.0), Paymob (MIT), awesome-copilot (MIT), Brex (MIT), Clean-Backend (MIT), `claude-code-security-review` (MIT), OWASP (CC BY-SA 4.0, só referência), Fowler, Willison, rascunho IETF de `Idempotency-Key`.
- **gstack** (Garry Tan e contribuidores, MIT): apenas inspiração do formato de achado; nada copiado.
- **Não usados** (rejeitados na pesquisa): `wshobson/pci-compliance`, skills Stripe `stripe-pay`, `stripe-projects`, `stripe-directory`, `agent-card-skill`, hooks de PagoKit, Mercado Pago e aitmpl, entre outros (ver `fontes.md`).

## Limitações honestas

- **Lacunas regulatórias sem fonte lida:** PCI DSS (nenhum requisito numerado verificado), KYC/AML, Manual de Segurança do Pix e Regulamento (limites, DICT), IN BCB 766 (prazo de 80 dias do MED **Não verificável**), Pix Automático (limites), norma de boleto/CIP/fator de vencimento, layouts de Cielo/Rede/Stone, assinatura e idempotência do Pagar.me, manifesto `x-signature` do Mercado Pago, requisitos de Open Finance além da seção 5.1 da FAPI-BR v2.1.0. O plugin entrega estrutura e checklists rotulados e **nunca inventa número normativo**; veja `lacunas-e-nao-verificado.md` para fechar cada uma.
- **Fatos de provedor envelhecem:** retenção de chaves, prazos de disputa, mínimos por moeda, versão do Manual do Pix (2.10.0), ASVS (5.0.0), PCI DSS (4.0.1) e vigência da FAPI-BR. Cada referência manda registrar versão e data de leitura (SN-21).
- **Ledger:** imutabilidade, inteiros, id idempotente e duas fases têm fonte de fabricante (TigerBeetle); "soma zero por moeda", projeção reconstruível, `effective_at` e a precedência de evidências são **Inferido**.
- **Evals `designed_not_executed`:** os 10 casos exigem Claude Code 2.1.269 ou superior (`claude plugin eval`), execuções repetidas e baseline sem plugin; a eficácia do plugin é **desconhecida** até rodar. O único benchmark de praticante encontrado (Pablo-aps) é de uma rodada, e o próprio autor o considera não significativo.
- **Revisão não independente:** pesquisa, validação, síntese e construção foram feitas por modelos da família Claude (independência parcial). V-34, V-35, V-48 a V-50, V-54, V-63, V-65 e V-70 são derivados do validador e aguardam revisão cruzada por outra família de modelos ou por pessoa.
- **Comunidade fraca:** não há relato de praticante de pagamentos com Claude Code e engajamento relevante; "melhores práticas" aqui vêm de fabricantes, da Anthropic e de poucos repositórios com licença clara.
- **Fora do escopo:** recorrência e assinaturas, cartão salvo/tokenização (COF/EMVCo), carteiras nativas, câmbio, tributação (CBS/IBS, NF-e), split comercial, cripto e trades. Marketplace: só a mecânica financeira, rotulada **Inferido**.
- **Hook, MCP e Action não foram executados** pelo construtor; JSON e esboços em `ferramentas-e-mcp.md` seguem a documentação oficial lida em parte e precisam de teste no seu ambiente (inclusive Windows).
- O plugin **não** substitui compliance, parecer jurídico, homologação do PSP, pentest nem revisão humana; efeitos financeiros reais continuam exigindo confirmação por ação.
