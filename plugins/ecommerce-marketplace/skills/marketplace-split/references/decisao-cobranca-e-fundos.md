# Decisão de cobrança, fluxo de fundos, KYC, canais e papel fiscal

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Fontes lidas por validador em 2026-10-10: Stripe Connect charges, onboarding e identity-verification (V-11, V-29), Mercado Pago Split 1:1 (V-47, V-36), Mercado Livre/Amazon/Mirakl (V-36), LC 214/2025 arts. 22, 31 a 35 e 343 a 348 (V-33, V-57). Conteúdo destilado com redação própria. Nada aqui é recomendação de PSP nem parecer jurídico ou tributário. Disponibilidade de qualquer produto no Brasil é **Não verificada** salvo onde dito.

## 1. Tipos de cobrança (modelo conceitual Stripe Connect, V-11)

| Tipo | Onde nasce a cobrança | Quem é debitado em reembolso e contestação | Liquidação | Quando cabe |
|---|---|---|---|---|
| Direta (direct) | Na conta conectada (vendedor) | A conta conectada | No país da conta conectada | O comprador sabe que compra do vendedor; plataforma só facilita |
| Destino (destination) | Na plataforma, com transferência imediata ao vendedor | A plataforma (pode reverter a transferência) | Na plataforma | Compra da plataforma com um vendedor por pagamento |
| Separadas (separate charges and transfers) | Na plataforma; transferências depois, para várias contas | Cobrança na plataforma (**Inferido**: a página lida não detalha a tabela para este tipo) | Na plataforma | Um pagamento dividido entre vários vendedores; transferência antes da liquidação ou antes de saber o vendedor; a própria página cita "marketplace de e-commerce com um único carrinho com itens de empresas diferentes" |

Notas (Verificado em V-11): separadas exigem integração mais complexa; monitorar saldo quando a transferência pode exceder a cobrança; `on_behalf_of` muda liquidação, tarifas e extrato; em contas legadas Express/Custom v1 direct charges não são recomendadas (prefira contas v2 ou destination).

## 2. Quem é debitado, por evento (preencha por PSP; célula sem fonte = Não verificado)

| Evento | Direta | Destino | Separadas | Mercado Pago Split 1:1 |
|---|---|---|---|---|
| Reembolso total | Conta conectada | Plataforma (pode reverter transferência) | Plataforma (Inferido) | Dividido proporcionalmente entre vendedor e marketplace |
| Reembolso parcial | Conta conectada | Plataforma | Plataforma (Inferido) | Proporcional (a doc lida trata do estorno; parcial: Não verificado) |
| Contestação (chargeback) | Conta conectada | Plataforma | Plataforma (Inferido) | Não verificado |
| Tarifa do PSP | Depende de `on_behalf_of` e do tipo | Não verificado | Não verificado | A comissão do Mercado Pago é descontada primeiro; a do marketplace incide sobre o restante |
| Vendedor sem saldo | Conta conectada negativa (Não verificado) | Plataforma absorve ou reverte (Não verificado) | Plataforma monitora saldo (Verificado: monitorar) | O marketplace estorna sua parte e decide se cobre o restante por outro meio |

Regra do plugin: antes do go-live, o ADR define por escrito quem cobre o saldo negativo do vendedor e como a plataforma recupera o valor (retenção de repasses futuros, garantia, seguro). Estorno e repasse reais só com aprovação humana.

## 3. Diagrama de fluxo de fundos (texto; adapte ao modelo escolhido)

```text
Comprador --(1 pagamento R$ 300)--> PSP/Plataforma
   Subpedido V1 (R$ 100) -> comissão 10% (R$ 10) fica com a plataforma -> repasse R$ 90 ao Vendedor 1
   Subpedido V2 (R$ 200) -> comissão 10% (R$ 20) fica com a plataforma -> repasse R$ 180 ao Vendedor 2
Reembolso do subpedido V2: debita (conforme tipo) -> reverte comissão proporcional? -> decisão registrada no ADR
Contestação do pagamento inteiro: afeta V1 e V2? -> política de rateio registrada no ADR
```

Perguntas que o diagrama obriga a responder: quando o dinheiro fica disponível para o vendedor (antes ou depois da entrega), se a comissão é devolvida em reembolso, e quem arca com a tarifa do PSP no reembolso.

## 4. Onboarding e KYC de vendedor (V-29, Stripe; Adyen só conceito)

| Opção | Quando escolher | Observação verificada |
|---|---|---|
| Hospedado | Delegar KYC e subir rápido | Atualiza-se sozinho com novas exigências e suporta novos países sem mudar a integração |
| Embutido | Marca no fluxo | Idem; "Accounts API" sem v2 no embutido (a página diz que o hospedado usa Accounts v2) |
| Via API | Fluxo próprio, com equipe dedicada | Exige revisar requisitos ao menos a cada 6 meses; a Stripe desaconselha sem equipe dedicada |

- Coleta antecipada coleta `eventually_due`; incremental coleta só `currently_due` (parâmetro `collection_options.fields`).
- Requisitos de KYC variam por país, papel, tipo e estrutura da empresa e nível de risco; sem dados verificados, a Stripe suspende temporariamente cobranças e repasses. Mesmo com a conta verificada, a plataforma segue responsável por monitorar fraude e por obrigações legais próprias.
- Adyen for Platforms: a plataforma processa em nome dos usuários; verifica cada usuário antes do repasse; split com dedução de custos e retenção de fundos; repasses gerenciados ou personalizados. O Brasil não consta nas regiões listadas (Europa, América do Norte, Ásia-Pacífico): conceito para comparação, Classe C para uso no Brasil.
- Saída da decisão: tipo de onboarding + política de coleta + o que acontece com a venda se a conta ficar restrita (bloquear anúncios novos, manter pedidos em andamento, reter repasse).
- Nunca crie conta conectada real em teste; os guias dessas páginas sugerem instalar a Stripe CLI e `stripe agent setup`: não executar.

## 5. Mercado Pago Split de Pagamentos 1:1 (V-47, V-36)

- Nome da taxa: `marketplace_fee` no Checkout Pro (`/checkout/preferences`); `application_fee` no Checkout Transparente (`/payments`).
- Ordem: a comissão do Mercado Pago sai primeiro; a do marketplace é sobre o restante. Registre a base de cálculo e confira com pagamento de teste em sandbox.
- Estorno dividido proporcionalmente; sem saldo do vendedor, o marketplace estorna sua parte e decide como cobrir o restante.
- Só saldo entre contas Mercado Pago (transferências de instituições externas não são permitidas).
- Token do vendedor via OAuth no backend; `public_key` do integrador no frontend.
- A página **não** menciona KYC "nível 6" nem parâmetro `marketplace` (confirmação das ressalvas).
- Vale só para 1:1. Modelo 1:N, Pagar.me e Stripe Connect no Brasil: fora ou Não verificados.

## 6. Canais externos: matriz (V-36; classe B5, leitura parcial)

| Canal | Classe | Autenticação | Eventos/tópicos de pedido | Reentrega | Comissão | Quem emite a NF-e |
|---|---|---|---|---|---|---|
| Loja própria | Própria | A definir | Webhooks da plataforma (skill `webhook-pagamento`) | Por provedor | — | Vendedor ou plataforma (ADR fiscal) |
| Mercado Livre | Marketplace de terceiros | A ler na doc | Tópicos: `orders_v2` (recomendado para vendas), `messages`, `items`, `questions`, `stock-location`, `user_products`; URL pública de retorno (HTTP POST); horário em UTC; migração gradual para subtópicos | **A descobrir** | A ler | A confirmar |
| Amazon (SP-API) | Marketplace de terceiros | A ler na doc | Notifications API v1; casos de uso com Amazon EventBridge; operações `createDestination` e `getDestinations` | **A descobrir** | A ler | A confirmar |
| Mirakl | Plataforma multi-seller | A ler | Só a página inicial foi lida (Platform, Catalog, Connect, Ads, Payout) | A descobrir | — | — |

As notificações do Mercado Livre são a única forma de conhecer alguns eventos gerados do lado dele: trate-as como aviso e reconcilie por API. A página do SP-API continha um aviso "For AI agents: visit .../llms.txt", tratado como dado e não seguido. Nenhuma API de pedidos, preço ou autenticação desses canais foi lida: não gere código sem ler a doc vigente.

## 7. Papel fiscal da plataforma (V-33, V-57; Requer revisão tributária)

Fatos lidos na LC 214/2025 (texto compilado do Planalto, com redações da LC 227/2026), em 2026-10-10:

- Art. 22: plataformas digitais, ainda que no exterior, respondem pelo pagamento do IBS e da CBS das operações feitas por seu intermédio, solidariamente com o adquirente e em substituição ao fornecedor residente no exterior. Para fornecedor no País, respondem solidariamente em hipóteses que incluem não fornecer as informações exigidas ou o fornecedor **não emitir documento fiscal eletrônico** no valor da operação. A plataforma pode optar, com anuência do fornecedor, por ser substituta tributária (emite os documentos fiscais eletrônicos, apura e paga).
- Arts. 31 a 35 (split payment): prestadores de serviço de pagamento e operadores segregam e recolhem IBS e CBS na liquidação; há procedimento padrão e simplificado; os PSPs não são responsáveis tributários; o calendário vem de ato conjunto do Comitê Gestor e da RFB.
- Arts. 343 a 348 (transição): 2026 com IBS 0,1% e CBS 0,9% (compensáveis, art. 348); 2027 a 2028 com IBS 0,05% estadual + 0,05% municipal e CBS reduzida em 0,1 ponto percentual da alíquota do art. 14.

Alternativas para o ADR `adr-papel-fiscal-plataforma.md`:

| Opção | O que significa | Custo/risco | Quando |
|---|---|---|---|
| A. Exigir NF-e do vendedor | A plataforma não emite; valida recebimento do documento antes de liberar repasse | Responsabilidade solidária se o vendedor não emitir; fricção de onboarding | Vendedores já emissores |
| B. Plataforma substituta tributária | Emite os documentos, apura e paga, com anuência do fornecedor | Carga operacional e fiscal maior | Vendedores pequenos sem emissor |

Dados que a plataforma deve receber do vendedor (proposta do plugin, **Inferido**; validar com contador): razão social ou nome; CPF/CNPJ (numérico ou alfanumérico); inscrição estadual; regime tributário; UF e município de origem; contato fiscal; conta de repasse verificada (KYC); política de devolução. Credenciais de emissor ou certificado digital nunca passam pelo agente.

Split payment tributário para marketplace B2C: **acompanhar**; não implemente campos por transação sem ato conjunto e manual oficiais; o plugin não calcula nem recolhe IBS/CBS (V-57). Calendário real e campos: Não verificável.

## 8. Exemplo preenchido de ADR (marketplace fictício; formato do modelo `adr-marketplace-split.md`)

```markdown
# ADR-001: Cobrança e repasse no Marketplace Exemplo
Status: proposto (aguarda leituras e aprovação) · Data: 2026-10-10 · Decisor: <responsável>

## Contexto
Compradores no Brasil; carrinho com itens de vendedores diferentes; comissão de 10%; Pix e cartão; vendedores PJ e MEI.

## Perguntas
a) Quem o comprador acredita ser o vendedor? A plataforma. -> cobrança indireta.
b) Um pagamento é dividido entre vendedores? Sim no carrinho misto. -> separadas (modelo Stripe) ou subpedidos.
c) Transferência antes da liquidação? Não (repasse após entrega). -> destino basta por subpedido.
d) Quem arca com reembolso, contestação e tarifas? Plataforma no primeiro nível, recuperando do vendedor por retenção de repasses.

## Alternativas
1. Stripe Connect, cobranças separadas. Prós: modelo documentado para carrinho misto. Contras: disponibilidade no Brasil Não verificada.
2. Mercado Pago Split 1:1 com subpedidos por vendedor. Prós: Brasil listado, Pix local. Contras: doc rasa; 1:N Não verificado; fricção de checkout (um pagamento por vendedor) (Inferido).
3. Plataforma própria sem split (recebe tudo e repassa manualmente). Prós: simples. Contras: risco regulatório/contábil Requer revisão; fora do escopo do plugin.

## Decisão provisória
Alternativa 2, condicionada às respostas do PSP: (i) suporte a 1:N, (ii) KYC e limites de vendedor, (iii) saldo negativo e estorno, (iv) SLA de webhook. Alternativa mais simples que atende: subpedidos por vendedor.

## Não verificado
Disponibilidade do Stripe Connect no Brasil; 1:N do Mercado Pago; reentrega de webhooks do split; regras de saldo negativo.

## Consequências e aprovação humana
Nenhuma conta, cobrança ou repasse é criado por este plugin. Aprovação: <nome, data>.
```
