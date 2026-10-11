Em 10 dias úteis, com um QA e quatro devs, você não vai testar tudo nem automatizar tudo. O que funciona é isto:

1. Priorizar por risco de **dinheiro e de dado do cartão**, não por tela.
2. Pôr as regras de cálculo (limite, autorização, fatura) em teste automatizado **dentro do código dos devs**. Você entrega os casos e o resultado esperado.
3. Automatizar você mesmo só um smoke por API dos fluxos críticos.
4. Gastar o resto do seu tempo em exploração e nos riscos que ninguém mais vai enxergar.
5. Liberar de forma gradual, com kill switch. Isso faz parte da estratégia de teste: é o que protege do risco que sobrar.

## Suposições (corrija o que estiver errado)

- O cartão é emitido por uma processadora/emissor parceiro com sandbox. As compras chegam até vocês como autorizações (chamada ou webhook) e debitam o limite.
- A aprovação de limite tem regra ou score com quatro saídas: aprovado, limite reduzido, análise manual e recusado.
- Existe homologação e dá para ligar e desligar a funcionalidade por flag.
- O PO tem as regras de limite e de fatura (fechamento, vencimento, parcelamento, encargos), mas talvez não estejam escritas.
- Existe alguma esteira de build/deploy, mesmo sem testes.

## Riscos, ordenados (falha → efeito)

Todos os "Alto" envolvem dinheiro, dado do cartão, obrigação legal ou efeito difícil de desfazer.

| ID | Falha → efeito | Nível | Caso-chave e onde testar |
| --- | --- | --- | --- |
| R1 | Compra aprovada acima do limite, ou debitada duas vezes (compras simultâneas, retry, evento duplicado da processadora) → perda de crédito, limite negativo | Alto | Limite disponível R$ 100,00: duas compras simultâneas de R$ 80,00 → uma aprova, uma recusa. Compra de R$ 100,00 aprova; de R$ 100,01 recusa. Mesma autorização reenviada → um débito. Integração com banco real; confira o saldo **no banco**, não a resposta |
| R2 | Fatura com valor errado (parcelas, arredondamento, estorno, compra na virada do fechamento, vencimento em fim de semana ou feriado) → cobrança indevida, reclamação, problema regulatório | Alto | Oráculo = planilha independente com a regra escrita pelo PO. R$ 100,00 em 3 parcelas → 33,34 + 33,33 + 33,33 (ou a regra escrita), somando exatamente o total. Compra às 23:59:59 e às 00:00:00 do dia de corte. Vencimento num sábado e num feriado. Total da fatura = soma das transações. Unitário em centavos inteiros |
| R3 | Limite concedido errado (borda de faixa de renda ou score; recusa indevida) → prejuízo de crédito ou negação indevida | Alto | Tabela de decisão da regra de crédito, com 3 valores em cada limite de faixa e ao menos um caso para cada uma das 4 saídas. Unitário |
| R4 | Dado do cartão exposto ou visível a outro cliente (número completo ou CVV em log, URL, analytics; cartão alheio pela API) → fraude, LGPD, PCI | Alto | Cliente B pede o cartão do cliente A trocando o ID direto na API → 403/404 sem nada de A no corpo. Busca nos logs e no analytics por padrão de número de cartão (regex + Luhn). Exibição completa só ao titular autenticado |
| R5 | Ciclo de vida do cartão incoerente (cartão bloqueado ainda autoriza; duplo clique em "gerar" cria dois cartões; solicitação aprovada sem cartão) → fraude, custo, cliente sem cartão | Alto | Bloquear e tentar a compra seguinte → recusada. Duplo clique e retry após timeout → um cartão. Pela API: gerar cartão de solicitação recusada, reativar cartão cancelado → recusado. Tabela de transição de estados |
| R6 | Transações da processadora não batem com o seu registro (evento perdido, duplicado, fora de ordem; estorno e chargeback não refletidos) → prejuízo invisível até o fechamento | Alto | Mesmo evento 2×; eventos invertidos; evento com assinatura inválida → recusado e nada processado; dois estornos parciais somando mais que a compra → recusado. Conciliação diária automática com alerta de divergência |
| R7 | Dependência fora do ar (bureau, processadora, antifraude) e o sistema libera tudo ou recusa tudo → crédito indevido ou todos os clientes sem compra | Alto | Falha fechada: timeout ou 5xx do bureau → solicitação fica pendente ou vai para análise manual, **nunca aprova**. Autorização lenta → resposta dentro do prazo combinado com a processadora. Sandbox ou stub com falhas injetadas |
| R8 | Limite preso por autorização que nunca conclui (3DS abandonado, pré-autorização sem captura) → cliente "sem limite", suporte lotado | Médio | Iniciar a compra e abandonar → reserva liberada no prazo da regra. Exploratório |

## Quem faz o quê

| Quem | O que |
| --- | --- |
| Devs | Unitário de limite, fatura e estados (R1–R3, R5) em todo PR. Integração de autorização e eventos (R1, R6), cada dev dono do seu teste. Regra da casa: história só fica pronta com o teste da regra no PR |
| Você | Casos e resultado esperado **antes** do código, quando der (1–2 h de pair por regra). Testes de API de concorrência, idempotência e acesso indevido, na linguagem que os devs já usam. Smoke automatizado. Exploração. Ensaio de rollback. Parecer |
| Smoke automatizado (seu) | Por API: solicita → aprova → gera cartão → autoriza compra → fecha fatura (simulada). No máximo 1 teste de interface. Roda a cada deploy em homologação, o que vale a pena porque você vai repeti-lo em cada rodada de correção até o lançamento |
| Não faça | Suíte de interface inteira, ou centenas de casos passo a passo. Em 10 dias isso vira teste intermitente e documento que ninguém lê |

Para organizar: um quadro com uma linha por risco (R1–R8) e status, casos numa planilha ou como teste no repositório com o ID da história, e um resumo diário de 5 linhas para o PO.

## Calendário (D1 a D10 úteis)

Se o seu intervalo cruza a segunda 12/10 (feriado nacional), confira que o D10 foi contado só com dias úteis.

| Dia | Foco | Saída |
| --- | --- | --- |
| D1 | Sessão de 45 min com dev líder e PO (e compliance, se houver): confirmar R1–R8, escrever as regras de limite e fatura, pedir ambiente, sandbox e flag. Smoke manual de 15 min no que já roda | Riscos aprovados; perguntas abertas com dono e prazo |
| D2–D3 | Casos das regras Altas (decisão, limites, estados) com pair nos devs. Massa sintética (CPFs gerados, cartões só da sandbox). Falhas injetadas da processadora e do bureau. Exploratório 1: solicitação e aprovação | Planilha-oráculo da fatura; testes unitários de R1–R3 entrando nos PRs |
| D4–D5 | Testes de API: concorrência, idempotência, acesso indevido, bloqueio. Busca de número de cartão nos logs. Exploratórios 2 e 3: geração do cartão e compra online. Smoke no pipeline até o fim do D5 | Smoke verde em cada deploy |
| D6–D7 | Fatura: peça um jeito de adiantar o relógio ou disparar o fechamento em homologação, senão ela só é testável no fechamento real. Conciliação. Dependências fora do ar (R7). p95 da autorização com poucas dezenas de requisições por segundo. Varredura axe nas telas de solicitação e do cartão | Fatura conferida contra a planilha; não funcional com número |
| D8 | Congelamento de código. 1ª rodada completa dos riscos altos + smoke. Exploratório 4 (cortar rede, fechar o app no meio, duas abas) | Defeitos por severidade; correções priorizadas |
| D9 | Reteste e regressão crítica. Ensaio de kill switch e rollback com tempo medido. Painel e alertas. Checklist de release e parecer | GO, GO com condições ou NO-GO |
| D10 | Liberação gradual e acompanhamento. Smoke em produção só com conta de teste identificada e autorização | Métricas de cada etapa |

O plano supõe até **2 rodadas de correção**. Se a fatura só chegar em homologação no D7, a regressão aperta. Peça ao time para entregar na ordem do risco (autorização e limite primeiro, fatura cedo) e leve a decisão ao PO no D5: reduzir escopo ou liberar a fatura depois.

Se o prazo apertar, corte nesta ordem: acessibilidade além do axe, variedade de dispositivos, exploração de baixo risco, combinações raras de parcelamento. Não corte: R1–R7, kill switch e rollback, e o parecer.

## O que fica de fora e o risco que sobra

| Fora | Risco residual |
| --- | --- |
| Carga e pico acima do teste curto de p95 | Comportamento desconhecido num pico (ex.: campanha de lançamento). Mitigação: liberação gradual |
| Segurança além de acesso indevido, mascaramento, logs e login | Falha não óbvia que só um pentest acha. Recomendo antes de ampliar além do grupo inicial |
| Dispositivos além de 1 Android, 1 iPhone e 2 navegadores | Quebra de layout ou de fluxo em aparelho não testado |
| Atraso, encargos e cobrança; disputa (chargeback) ponta a ponta | A primeira fatura só vence semanas depois do lançamento, então dá para testar na sequência, com prazo antes do primeiro fechamento real. Disputa com a bandeira fica sem verificação |

Banco Central, PCI DSS e LGPD entram aqui só como pontos de verificação (R4, R6). Eu não declaro conformidade; isso é com compliance e jurídico, a quem vale perguntar que evidência exigem.

## Liberação e go/no-go

- **Flag em etapas** (equipe interna, depois um grupo pequeno, depois ampliar). Peça ao PO um **limite inicial baixo** para os primeiros clientes: é a medida mais barata contra R1, R2 e R3 errados.
- **Critérios de aborto escritos antes**, por exemplo: qualquer divergência de conciliação sem explicação, qualquer autorização acima do limite, erro na geração de cartão acima de 1%. Ajuste os números ao produto.
- **Primeiras faturas reais:** confira cada uma contra a planilha enquanto o volume for pequeno, antes de enviar.
- **Bloqueantes para GO:**
  - nenhum defeito crítico aberto;
  - R1–R7 com evidência;
  - número de cartão fora dos logs;
  - acesso entre clientes testado pela API;
  - smoke e regressão crítica verdes em homologação com configuração equivalente à de produção;
  - kill switch e rollback ensaiados;
  - painel e alerta com métrica de negócio (autorizações aprovadas e recusadas, divergência de conciliação, erro de geração);
  - roteiro do suporte;
  - risco residual aceito por escrito por quem decide.

  Você informa o risco. O go/no-go é do PO com o líder técnico.

## Perguntas que mudariam este plano

1. Quem emite e processa o cartão, e a sandbox simula falhas (timeout, recusa, evento duplicado)? Sem isso, R6 e R7 viram contrato mais stub.
2. As regras de limite e de fatura estão escritas e com quem? Sem regra escrita não há resultado esperado, e o D1 vira escrever regra.
3. Dá para liberar por flag e com limite inicial baixo? Se não, o risco residual aceitável cai e o NO-GO fica mais provável.
4. Qual a stack dos devs e como é a esteira? Com isso eu escrevo o smoke e os testes de API no padrão de vocês.
5. Dá para adiantar o relógio ou forçar o fechamento da fatura em homologação?

Não executei nada: é um plano sobre as suposições acima. Valores de limite, encargos e prazos regulatórios têm de vir do produto e das normas, não deste texto. Se você confirmar as suposições e passar a stack, o próximo passo mais útil é eu escrever os casos de R1–R3, com dados e resultado esperado, e o checklist de release já preenchido para este lançamento.
