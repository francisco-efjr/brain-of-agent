# Exemplos trabalhados de estratégia

Apoio da skill `test-strategy`. Quatro modelos para copiar a forma, não o conteúdo. Adaptados do brain-of-agent (conteúdo próprio do usuário, MIT), com redação revisada.

Aviso: leis, normas, percentuais e prazos citados são pontos de partida do exemplo (Inferido); não foram reverificados nesta fábrica. Confirme norma e vigência com a área jurídica ou de compliance antes de usar como oráculo (Não verificável aqui).

## Sumário

- [Tabela de riscos: módulo de férias de um portal de RH](#tabela-de-riscos-módulo-de-férias-de-um-portal-de-rh)
- [Frete com tabela nova em 2 horas](#frete-com-tabela-nova-em-2-horas)
- [Parecer de prontidão](#parecer-de-prontidão)
- [Resumo: checkout com PIX](#resumo-checkout-com-pix)
- [Como adaptar](#como-adaptar)

## Tabela de riscos: módulo de férias de um portal de RH

Contexto: novo módulo de solicitação e aprovação de férias; escala 1-3; oráculo legal declarado como hipótese (CLT, arts. 134 e 145) a validar com o jurídico.

| ID | Risco (falha -> efeito) | Característica | P | I | Nível | Mitigação |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Aceita fracionamento fora da regra (período de 4 dias; nenhum período de 14 dias ou mais) -> passivo trabalhista | Adequação funcional | 3 | 3 | 9 Alto | tabela de decisão para 1, 2 e 3 períodos; limites 4/5 e 13/14 dias em teste unitário da regra |
| R2 | Permite início nos 2 dias antes de feriado ou repouso semanal -> infração | Adequação funcional | 3 | 3 | 9 Alto | casos com feriados nacionais e municipais de cada filial, virada de ano, escala com folga fora do domingo |
| R3 | Gestor aprova férias de outra equipe trocando o ID na API -> fraude e exposição de dados | Segurança | 2 | 3 | 6 Alto | matriz perfil x recurso na API, esperado 403/404 |
| R4 | Pagamento chega à folha depois do prazo -> descumprimento | Confiabilidade | 2 | 3 | 6 Alto | contrato com a API da folha; teste do agendamento com início em segunda após feriado; alerta se o lote não sair |
| R5 | Saldo migrado do legado com dias errados -> recusas indevidas | Adequação funcional | 3 | 2 | 6 Alto | reconciliação de totais por filial antes e depois + amostra de 50 casos especiais (afastamento, admissão recente) |
| R6 | Erro no calendário não anunciado por leitor de tela | Capacidade de interação | 2 | 2 | 4 Médio | varredura automatizada + roteiro manual com leitor de tela no fluxo de solicitação |
| R7 | Tela de aprovação lenta no pico de dezembro | Eficiência de desempenho | 1 | 2 | 2 Baixo | smoke de carga com o volume do dezembro anterior; acompanhar p95 em produção |

Fora do plano: relatório gerencial de férias (sem alteração de código). Risco residual: totais do relatório podem divergir até R5 fechar.

Leituras úteis da tabela: três riscos Altos de impacto 3 mostram onde gastar o tempo; R7 recebe só smoke porque P e I são baixos; há linhas não funcionais (R3, R6, R7), o que evita um plano que só olha a regra.

## Frete com tabela nova em 2 horas

Contexto: e-commerce com tabela de frete por região nova e frete grátis "acima de R$ 199". Nunca se corta: riscos Altos, fluxo do dinheiro e parecer com risco residual.

| Janela | Atividade | Saída |
| --- | --- | --- |
| 10 min | Perguntar ao dev o que mudou (diff, flags) e o que o preocupa; ao PO, o pior cenário | lista de mudanças e preocupações |
| 10 min | Listar 5 riscos, escolher 3. A ambiguidade já é um achado: "acima de R$ 199" inclui 199,00? Vale antes ou depois do cupom? | 3 riscos + perguntas ao PO |
| 60 min | Teste focado: 198,99 / 199,00 / 199,01; CEP de cada região e de área remota; frete grátis + cupom; carrinho alterado depois do cálculo | casos executados, defeitos com evidência |
| 20 min | Regressão por impacto: checkout com um meio de pagamento; estimativa de frete na página do produto | smoke verde ou achados |
| 10 min | Confirmar suíte automatizada verde, flag ou rollback disponível, painel da cotação | checklist |
| 10 min | Parecer: testado, não testado, risco residual | mensagem de parecer |

Para 2 dias, acrescente a análise de risco com dev e PO (45 min), a tabela de decisão região x peso x frete grátis x cupom virando teste parametrizado, regressão selecionada por impacto, cotação com a transportadora lenta e 60 min de exploração no celular. Para 2 semanas, entre no refinamento (critérios de aceite com exemplos), contrato com a API da transportadora, massa de dados por região, testes no pipeline, carga no serviço de cotação e liberação gradual por flag (10% -> 50% -> 100%) comparando erro de cotação, conversão e frete médio.

## Parecer de prontidão

Formato curto e decidível (exemplo com dados fictícios):

> **Parecer de prontidão: Frete por região v2, 07/10**
>
> - **Recomendação: GO com condições.** Liberar para 10% dos clientes na terça, 10h; ampliar para 100% na quinta se as métricas se mantiverem.
> - **Verificado:** cálculo das 5 regiões e do limite do frete grátis (42 casos automatizados no serviço, verdes); checkout em Chrome, Safari iOS e Android; regressão crítica (68 testes) verde em pré-produção.
> - **Não verificado:** cotação da transportadora B com tráfego real (sandbox instável); frete grátis com cupom de 100% (combinação rara).
> - **Risco residual:** se a transportadora B falhar, clientes do Norte veem "frete indisponível" e não compram (cerca de 6% dos pedidos); o alerta de erro de cotação detecta em minutos e a flag volta à tabela antiga em menos de 5 min.
> - **Condições:** plantão de backend até 20h; aceite do PO para o cupom de 100%.

Por que funciona: a recomendação vem primeiro, o risco residual está em linguagem de negócio (evento -> efeito -> probabilidade -> detecção -> quem aceita) e o que não foi verificado aparece antes de alguém perguntar. Os números do exemplo são ilustrativos.

## Resumo: checkout com PIX

Contexto suposto: e-commerce médio adiciona PIX ao checkout web; um provedor de pagamento (PSP) gera a cobrança com QR Code e avisa o pagamento por webhook; deploy contínuo com flags.

Riscos Altos (falha -> efeito):

1. Pagamento confirmado e pedido não liberado (webhook perdido, atrasado ou com erro) -> cliente paga e não recebe.
2. Webhook duplicado ou fora de ordem -> baixa dupla de estoque ou pedido duplicado.
3. Webhook forjado marca pedido como pago -> fraude.
4. Valor cobrado diferente do total do pedido (cupom, frete, centavos) -> perda ou reclamação.
5. Pagamento chega depois da expiração e do cancelamento -> cliente paga pedido cancelado.
6. Divergência entre pagamentos recebidos e pedidos pagos -> prejuízo invisível.

Abordagem por camada: unitário para cálculo em centavos inteiros e máquina de estados do pedido (transições proibidas incluídas); integração do handler de webhook com banco real (idempotência, autenticidade, falha no meio); contrato e virtualização do PSP (5xx, timeout, lentidão); três E2E no sandbox (paga no prazo, expira, paga após cancelar); charters exploratórios ("pagar o mesmo QR em dois aparelhos"). Shift-right: flag 5% -> 25% -> 100% com métricas de negócio (cobranças geradas x pagas, p95 pagamento -> liberação, webhooks com erro, pagos e não liberados, divergência da reconciliação) e kill switch.

Detalhes do domínio de pagamentos (regras do PIX, PSP, conformidade) pertencem ao segmento de fintech-payments; aqui o exemplo ilustra apenas a forma da estratégia.

## Como adaptar

1. Troque o domínio, mantenha a forma: risco como falha -> efeito, P e I ancoradas, camada por risco, "fora do plano", risco residual.
2. Reescreva as perguntas ao PO que o exemplo levantou (limite inclusivo? antes ou depois do cupom?) para o seu caso; ambiguidade de requisito é achado.
3. Se não houver dados de probabilidade, use incidentes e chamados recentes como melhor estimativa e diga que é isso.
4. Se o prazo cortar o plano, escreva o corte: o que sai, o risco que sobra, quem aceita.
