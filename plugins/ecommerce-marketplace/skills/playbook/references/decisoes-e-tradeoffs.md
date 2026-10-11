# Decisões e trade-offs de e-commerce e marketplaces

Cada decisão traz: situação, opções, critério de escolha, recomendação com rótulo e fonte. Quando a decisão é material (dinheiro, estoque, fiscal, marketplace), registre em ADR ([adr-marketplace-split.md](../assets/templates/adr-marketplace-split.md), [adr-papel-fiscal-plataforma.md](../assets/templates/adr-papel-fiscal-plataforma.md)) e peça aprovação humana antes de implementar. A decisão é da pessoa responsável pelo produto; o agente apresenta alternativas, inclusive a mais simples.

Modelo-alvo: Claude 4.x/5.x · pesquisa validada em 2026-10-10 · compilado em 2026-10-11.

## Sumário

- [D-01 Tipo de cobrança em marketplace](#d-01-tipo-de-cobrança-em-marketplace) · [D-02 Onboarding de vendedor e KYC](#d-02-onboarding-de-vendedor-e-kyc) · [D-03 PSP para split no Brasil](#d-03-psp-para-split-no-brasil)
- [D-04 Autenticação de webhook](#d-04-autenticação-de-webhook-hmac-token-mtls) · [D-05 Pix: webhook × consulta](#d-05-pix-webhook-ou-consulta) · [D-06 Reserva de estoque](#d-06-reserva-de-estoque-com-ou-sem-ttl)
- [D-07 Ordem de descontos](#d-07-ordem-de-descontos-e-arredondamento) · [D-08 Motor de busca](#d-08-motor-de-busca-de-catálogo) · [D-09 Plataforma própria × canal](#d-09-plataforma-própria-ou-canal-de-terceiros)
- [D-10 Papel fiscal da plataforma](#d-10-papel-fiscal-da-plataforma) · [D-11 Workflow × agente](#d-11-workflow-ou-agente-autônomo) · [D-12 Checkout hospedado × próprio](#d-12-checkout-hospedado-ou-formulário-próprio)
- [D-13 Evento fino × snapshot](#d-13-evento-fino-ou-snapshot) · [D-14 Reembolso e devolução](#d-14-reembolso-e-devolução) · [D-15 Facetas](#d-15-facetas-indexáveis-ou-não)
- [Conflitos entre fontes e como foram resolvidos](#conflitos-entre-fontes-e-como-foram-resolvidos)

## D-01 Tipo de cobrança em marketplace

Fonte: V-11 (Stripe Connect, documentação oficial). Os três tipos são conceitos de PSP; a disponibilidade no Brasil de cada provedor é **Não verificada**.

| Opção | Onde a cobrança nasce | Quem é debitado em reembolso e contestação | Quando serve |
| --- | --- | --- | --- |
| Direct | Conta do vendedor; fundos liquidados no país dela | O vendedor (conta conectada) | O comprador sabe que compra do vendedor; plataforma só facilita |
| Destination | Conta da plataforma; transferência imediata ao vendedor | A plataforma (pode reverter a transferência) | Comprador compra da plataforma; um vendedor por pagamento |
| Cobranças + transferências separadas | Conta da plataforma; transferências depois, para várias contas | A plataforma (gerencia o saldo) | Carrinho com itens de vendedores diferentes; transferir antes da liquidação |

**Quatro perguntas:** (1) o comprador sabe que compra do vendedor ou da plataforma? (2) um pagamento é dividido entre vários vendedores? (3) a transferência pode ocorrer antes da liquidação ou antes de saber o vendedor? (4) quem arca com reembolso, contestação e tarifas? **Recomendação:** carrinho multi-seller ⇒ separadas (a própria página cita esse caso); monitorar saldo quando a transferência puder exceder a cobrança; `on_behalf_of` muda liquidação, tarifas e extrato. Saída: tipo + diagrama do fluxo de fundos + tabela "quem é debitado" por evento. Rótulo: **Verificado** (conceito Stripe), **Não verificado** (Brasil).

## D-02 Onboarding de vendedor e KYC

Fonte: V-29 (Stripe Connect). Três opções: **hospedado** (a Stripe atualiza exigências e países sem mudar a integração), **embutido** (marca no fluxo; atualiza sozinho), **via API** (a plataforma revê requisitos ao menos a cada 6 meses; a Stripe desaconselha sem equipe dedicada). Coleta **antecipada** (`eventually_due`, menos risco de repasse travado) × **incremental** (`currently_due`, cadastro mais rápido). Critério: delegar KYC e subir rápido ⇒ hospedado; marca no fluxo ⇒ embutido; fluxo próprio só com equipe. Antes de liberar repasse, ler o estado de requisitos da conta conectada e bloquear venda com pendência vencida. O KYC do provedor não substitui obrigações da plataforma (LGPD, fiscais, antifraude). Sem dados verificados, a Stripe suspende temporariamente cobranças e repasses. Rótulo: **Verificado**; aplicação ao Brasil **Não verificada**.

## D-03 PSP para split no Brasil

| Opção | O que a pesquisa leu | Limites |
| --- | --- | --- |
| Mercado Pago Split 1:1 | Lista Brasil (V-36); `marketplace_fee` (Checkout Pro) / `application_fee` (Transparente); comissão do Mercado Pago primeiro, a do marketplace sobre o restante; estorno proporcional; só saldo entre contas Mercado Pago (V-47) | Só modelo 1:1; 1:N fora; quem cobre saldo negativo do vendedor é decisão do marketplace |
| Stripe Connect | Documentação rica de tipos de cobrança e KYC (V-11, V-29) | Brasil **Não verificado** |
| Adyen for Platforms | Conceito de split e retenção (V-29) | Brasil não aparece nas regiões listadas: só comparação conceitual |
| Mirakl | Só a página inicial (V-36) | Sem leitura de API |
| Pagar.me split | Não lido | Lacuna |

**Recomendação:** o plugin não recomenda um PSP como fato. Entregar matriz com "Não verificado" onde faltar leitura, comparando KYC, repasse retido, estorno, meios locais (Pix, boleto) e custo ([matriz-canais-integracao.md](../assets/templates/matriz-canais-integracao.md)). Conflito C6 (abaixo).

## D-04 Autenticação de webhook: HMAC, token, mTLS

| Mecanismo | Provedores lidos | Cuidados |
| --- | --- | --- |
| HMAC sobre corpo bruto | Stripe (`Stripe-Signature`), Shopify (`X-Shopify-Hmac-Sha256`), Mercado Pago (`x-signature` `ts=...,v1=...`), Melhor Envio (`X-ME-Signature`), Nuvemshop (`x-linkedstore-hmac-sha256`) | Corpo bruto; tempo constante; recência onde existir; rotacionar segredo com janela (Stripe: até 24 h) |
| Token estático | Asaas (`asaas-access-token`) | Não é HMAC do corpo; comparar em tempo constante; não usar a API Key como token; combinar com IPs oficiais (página não lida) e reconciliação |
| mTLS | Webhook Pix do Banco Central (callback protegido por mTLS; detalhes no Manual de padrões, não lido) | Certificado e SLA são do PSP; confirmar |

Regra: nunca generalizar de um provedor para outro. Tabela completa em [pagamentos-webhooks-split.md](pagamentos-webhooks-split.md). **Verificado** (V-09, V-30, V-31, V-35, V-51).

## D-05 Pix: webhook ou consulta

O webhook Pix só notifica Pix associados a um `txid` (cobrança `cob`/`cobv`); cobrança sem `txid` não gera aviso. O aviso não é prova de liquidação final. **Recomendação:** usar webhook como gatilho **e** consultar a API (valor, `txid`, devoluções) antes de liberar pedido; manter consulta de reconciliação para cobranças sem `txid`; tratar devolução como evento próprio com estado final (`DEVOLVIDO` ou `NAO_REALIZADO`). SLA e reentrega variam por PSP: **Não verificável** sem o contrato. Fonte: V-31.

## D-06 Reserva de estoque com ou sem TTL

| Opção | Quando | Custo |
| --- | --- | --- |
| Reservar na conclusão do carrinho, sem expiração | Pagamento síncrono (cartão aprovado em segundos) | Reservas órfãs se o pagamento nunca confirmar |
| Reservar com `expires_at` da loja + job de liberação | Pix, boleto, última unidade | Mais peças: job, lock, política de pagamento tardio |
| Não reservar; decrementar no pagamento confirmado | Estoque abundante | Venda acima do saldo na corrida pela última unidade |

**Recomendação:** para Pix/boleto, TTL próprio (**Inferido**: nenhuma fonte lida define; o módulo de inventário da Medusa não tem expiração, V-39/V-48). Pagamento após a liberação ⇒ reabrir se houver saldo, senão reter para revisão humana. TTL de lock (segundos, `acquireLockStep`) ≠ TTL de reserva (minutos). Detalhes em [estoque-pedidos-promocoes.md](estoque-pedidos-promocoes.md).

## D-07 Ordem de descontos e arredondamento

R$ 200,00 com 10% e R$ 20,00: percentual primeiro ⇒ 200 → 180 → 160; fixo primeiro ⇒ 180 → 162 (brain). **Recomendação:** a ordem é regra de negócio, escreva-a e teste as duas. Na Medusa, `buyget` vem antes de `standard`, percentual incide sobre o **restante** e desconto de pedido é distribuído proporcionalmente ao valor restante (V-38, **Verificado**). Arredondamento: inteiros em unidade menor, resto no último item (**Inferido**; nenhuma fonte define; 100,00 em 3 parcelas = 33,34 + 33,33 + 33,33). Frete grátis: o limite vale antes ou depois do desconto? Decida e teste 198,99 e 199,00.

## D-08 Motor de busca de catálogo

| Motor | Lido | Pontos de decisão |
| --- | --- | --- |
| Typesense | `facet_by`, `facet_strategy` (`exhaustive`, `top_values`, `automatic`), `filter_by` (`:` não exato, `:=` exato), `sort_by` até 3 campos | Exige `:=` em ID/SKU/marca |
| Meilisearch | `filterableAttributes`, parâmetro `facets` | Declarar atributos antes |
| Algolia | Facetas derivadas de atributos, contagem por faceta | Custo e sinônimos **não lidos** |
| Elasticsearch, Shopify Search & Discovery, busca da Medusa | Não lidos | **Não verificável** |

**Recomendação:** escolha por requisitos (facetas, volume, idioma PT, custo, operação), não por popularidade (estrelas não provam qualidade). Documento de decisão com requisito, recurso do motor e teste; preço como inteiro (**Inferido**); sinônimos e typos em PT sem fonte: testar com catálogo sintético. Fonte: V-37.

## D-09 Plataforma própria ou canal de terceiros

Classifique o canal: loja própria, marketplace de terceiros (Mercado Livre, Amazon), plataforma multi-seller própria. Em canal de terceiros as notificações são a **única forma** de conhecer alguns eventos (Mercado Livre: tópicos como `orders_v2`, `items`, `stock-location`; Amazon SP-API: Notifications API com EventBridge), a comissão e a emissão de NF-e dependem do contrato e a reentrega é "a descobrir". Plataforma própria dá controle de dados e de margem, mas assume KYC, repasse, estorno, fiscal e suporte (D-01 a D-03, D-10). Critério: tamanho do catálogo, necessidade de controle do cliente, capacidade operacional. Fonte: V-36 (nenhuma API de pedido, preço ou autenticação foi lida: **Não verificado**).

## D-10 Papel fiscal da plataforma

Art. 22 da LC 214/2025 (texto com LC 227/2026, lido em 2026-10-10): plataforma digital responde solidariamente pelo IBS/CBS das operações feitas por seu intermédio, incluindo quando o fornecedor no País não emite documento fiscal eletrônico; pode **optar** por ser substituta tributária (emite documentos fiscais eletrônicos, apura e paga) com anuência do fornecedor. Opções: (a) exigir NF-e do vendedor e validar; (b) substituta tributária por opção. Critério: perfil dos vendedores (MEI/PJ), capacidade fiscal da plataforma, risco da responsabilidade solidária. Saída: ADR com dados exigidos do vendedor. **Requer revisão tributária**; nada aqui é aconselhamento. Split payment tributário (arts. 31–35): marketplace B2C **acompanha**; calendário por ato conjunto é **Não verificável**; a hipótese "nenhuma ação em B2C" foi rejeitada (V-57). Fontes: V-33, V-57.

## D-11 Workflow ou agente autônomo

Fonte: V-04 (Anthropic, 2024; princípios gerais). Comece pelo mais simples. Passos fixos com checagem ⇒ encadeamento; classificação antes de tratar (troca × devolução × reembolso) ⇒ roteamento; auditoria de lojas grandes ⇒ orquestrador-trabalhadores; **qualquer efeito em pedido ou pagamento ⇒ ponto de parada humano obrigatório**, nunca autônomo. Atendimento automatizado de pedido: avaliar antes de publicar com casos sintéticos, incluindo adversariais (V-27).

## D-12 Checkout hospedado ou formulário próprio

Campos hospedados ou redirecionamento do provedor mantêm o número do cartão fora do backend da loja e **reduzem o escopo** de PCI (**Inferido**; a página do PCI SSC lida descreve só o público do padrão, V-43). Formulário próprio dá controle de UX, mas amplia escopo e superfície (scripts de terceiros: requisitos 6.4.3 e 11.6.1, brain, **Inferido**). A decisão de escopo (SAQ aplicável) é humana e do adquirente: **Requer revisão especializada**. Para acessibilidade, o checkout hospedado do provedor ou da plataforma pode ficar fora do que você controla (a própria ferramenta `ecom-a11y-audit` deixa o checkout da Shopify fora de escopo, V-16): registre isso.

## D-13 Evento fino ou snapshot

A Stripe recomenda eventos **thin** em integrações novas (buscar o objeto atual pela API) e snapshot quando terceiros exigem o objeto completo (V-09). **Recomendação:** thin + busca do estado atual combina com "evento é aviso, API é verdade" (PA-07); use snapshot só quando a integração de terceiros não puder consultar a API.

## D-14 Reembolso e devolução

Classifique antes de tratar: troca, devolução, arrependimento, reembolso parcial. Cada um é uma transição explícita (devolvido → reembolso pendente → reembolsado) com chave de idempotência por reembolso e soma de reembolsos ≤ valor capturado. Retorno ao estoque só após conferência (Medusa: devolução recebida repõe, danificada não, V-48). O reembolso no PSP exige **aprovação humana**. Arrependimento: CDC art. 49 (7 dias do recebimento, contratação fora do estabelecimento; devolução imediata de valores pagos a qualquer título); "dias corridos", "frete devolvido" e "sem exigir motivo" são **Inferido/Suposição**; aplicação ao e-commerce via Decreto 7.962 art. 5º (não relido). **Requer revisão jurídica** (V-55, V-32).

## D-15 Facetas indexáveis ou não

Lista de parâmetros de faceta, cada um marcado indexável ou não; não indexáveis bloqueados no `robots.txt`; filtro que precisa de SEO nunca em `#`; combinação sem resultado devolve 404, não redirect genérico; canonical/nofollow são menos eficazes no longo prazo (V-45). Contar URLs geradas por combinação antes de publicar (**Suposição** de método). Orientação de rastreamento, não garantia de ranking.

## Conflitos entre fontes e como foram resolvidos

| # | Conflito | Resolução |
| --- | --- | --- |
| C1 | `plugin.json` obrigatório (README do repositório oficial) × opcional, só `name` (referência atual) | Vale a referência atual; manter o manifesto por metadados (V-06) |
| C2 | Retry: "5xx/429 reenviam, demais 4xx não" (Hookdeck) × Stripe reentrega qualquer não-2xx | A regra é do gateway da Hookdeck; documentar por provedor (V-09) |
| C3 | "Shopify exige 200 em 5 s" (sem fonte) × MP 22 s, Melhor Envio 6 s, VTEX 5 s, Nuvemshop 3 s | Cada prazo vale para seu provedor; o "5 s do Shopify" é **Não verificado**; regra do plugin: 2xx em < 5 s e fila |
| C4 | HMAC × token estático × mTLS | Tabela por provedor (D-04) |
| C5 | Medusa sem TTL × necessidade de expirar Pix/boleto | TTL da aplicação (D-06) |
| C6 | Stripe Connect (Brasil não verificado) × Mercado Pago Split 1:1 × Adyen (sem Brasil) × Mirakl | Matriz com "Não verificado" (D-03) |
| C8 | Prompt oficial de security-review exclui DoS e rate limit × abuso de cupom, card testing e enumeração custam dinheiro | Manter o formato (confiança 1–10, corte 8, ferramentas de leitura) e acrescentar achados "sugestão" (V-44) |
| C9 | CLAUDE.md na raiz do plugin não carrega × regras permanentes | Invariantes no `playbook` + snippets para o usuário colar |
| C10 | `reduced motion` AA (awesome-copilot) × WCAG 2.3.3 é AAA | Seguir a norma: boa prática, não AA (V-16) |
| C11 | `availability` obrigatória × recomendada | Recomendada (V-17) |
| C13 | Prazo de arrependimento: Decreto 7.962 não fixa × CDC art. 49 | Art. 49 lido (V-55); aplicação a e-commerce e contagem: **Requer revisão jurídica** |
| C14 | PCI DSS 4.0.1 (brain) × V-43 só leu visão geral | Brain = **Inferido**; decisão de escopo humana |
| C15 | Tabela de transição CBS/IBS do brain × LC 214 lida só em artigos pontuais | 2026 e 2027–2028 **Verificados**; 2029–2033 e Imposto Seletivo **Inferido (brain)**; alíquotas finais **Não verificável** |
| C17 | Woo `consumer_key` na query string × boa prática | Nunca usar (V-41) |

Os conflitos sobre classificação do gstack (C7), loops em Liquid (C12), dados pseudonimizados do WooCommerce (C16) e `dry_run` do shopify-admin-skills (C18) estão na seção "Correções aos pesquisadores" de [fontes.md](fontes.md).
