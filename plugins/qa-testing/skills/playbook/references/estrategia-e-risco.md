# Estratégia de testes e análise de risco

Como decidir **o que testar, com que profundidade, em que nível e quando parar**. Leia para montar estratégia ou plano, decidir com pouco tempo, escolher a regressão, dar parecer de prontidão ("está pronto para produção?") ou definir métricas. Base: `estrategia.md` do brain-of-agent (MIT, conteúdo próprio, condensado e adaptado) cruzado com V-14, V-16, V-23, V-36 (ver `fontes.md`). Rótulo geral: conhecimento próprio **Inferido** (não reverificado em fonte externa); normas e números regulatórios são pontos de partida, confirme vigência. Validado em 2026-10-10.

## Sumário

- [Perguntas de contexto](#perguntas-de-contexto)
- [Análise de risco](#análise-de-risco)
- [Níveis, tipos e quadrantes](#níveis-tipos-e-quadrantes)
- [Formato do portfólio](#formato-do-portfólio)
- [Estratégia com pouco tempo](#estratégia-com-pouco-tempo)
- [Regressão](#regressão)
- [Shift-left e shift-right](#shift-left-e-shift-right)
- [Critérios de entrada, saída e parada](#critérios-de-entrada-saída-e-parada)
- [Prontidão para produção e parecer](#prontidão-para-produção-e-parecer)
- [Métricas](#métricas)
- [Estimativa de esforço](#estimativa-de-esforço)
- [Exemplo resumido: PIX no checkout](#exemplo-resumido-pix-no-checkout)

## Perguntas de contexto

Saiba quais perguntas, respondidas de outro jeito, mudariam o plano; não precisa de todas as respostas para começar. O que faltar vira suposição declarada ("Supondo que…"). Armadilha: virar interrogatório e não entregar nada; em 15 minutos com dev e PO você responde a maioria.

| Pergunta | Respostas que mudam o plano | Efeito na estratégia |
| --- | --- | --- |
| Qual fluxo paga as contas ou cumpre a missão? | checkout, emissão de nota, prescrição, folha | Profundidade máxima nele; o resto recebe smoke e exploração proporcional |
| Quem usa, quantos, em que condições? | 20 clientes B2B com configuração própria; milhões no celular; usuários de leitor de tela | B2B: teste por configuração dos maiores clientes; B2C massivo: compatibilidade, desempenho, acessibilidade |
| Qual o pior efeito realista de uma falha? | incômodo; venda perdida; dinheiro ou dado perdido; dano à saúde | Define o teto de impacto; efeito irreversível torna rollback e reconciliação testes obrigatórios |
| Há regulação, auditoria ou contrato? | LGPD, normas setoriais, PCI DSS, SLA | Evidência rastreável por versão; oráculo na própria norma; trilha de auditoria testada |
| Qual a arquitetura? | monólito, microsserviços, SPA, nativo, legado, terceiros | Define o formato do portfólio e a necessidade de contrato e de virtualização |
| Como se publica e se desfaz? | deploy contínuo com flag; app em loja; on-premises trimestral | Correção barata → mais shift-right; correção cara (loja, on-prem, firmware) → pré-release mais profundo |
| Qual o prazo e o que é imóvel? | Black Friday, prazo legal | Congele escopo; priorize regressão do crítico e contingência (flag, rollback) |
| Qual a maturidade do time? | sem CI e sem testes; TDD e pipeline confiável | Baixa: smoke automatizado e checklist de release; alta: QA foca em risco, exploração e não funcional |
| O que já existe e o que já quebrou? | suíte, incidentes, chamados | Incidentes e chamados são a melhor estimativa de probabilidade disponível |
| Quem decide o go/no-go? | PO, diretoria, comitê | Define formato e vocabulário do parecer |

## Análise de risco

**Identificar.** Cruze cada funcionalidade (ou mudança) com as características de qualidade de produto da ISO/IEC 25010 (a edição de 2023 tem nove; muito material ainda reproduz a de 2011, com oito: Inferido, confirme a edição) como lembrete, não formulário. Outras fontes: o diff, incidentes e chamados, módulos com mais defeitos (defeitos se agrupam), "onde você tem medo?" ao dev e "do que o cliente mais reclama?" ao suporte.

| Característica | Pergunta-gatilho | Exemplo de risco |
| --- | --- | --- |
| Adequação funcional | faz o certo, completo, com resultado correto? | desconto aplicado duas vezes |
| Eficiência de desempenho | responde a tempo sob a carga esperada? | cotação de frete acima de 5 s no pico |
| Compatibilidade | convive com outros sistemas e versões? | app antigo quebra com campo novo na API |
| Capacidade de interação (inclui acessibilidade) | a pessoa usa sem errar, inclusive com teclado e leitor de tela? | erro de formulário não anunciado |
| Confiabilidade | continua e se recupera de falhas? | aviso de pagamento perdido deixa pedido pendente |
| Segurança (security) | só quem pode acessa e altera? fica registrado? | trocar o ID na URL mostra pedido de outra pessoa |
| Manutenibilidade | dá para mudar e testar sem medo? | mesma regra duplicada em três serviços |
| Flexibilidade | adapta-se a outro ambiente, escala, configuração? | só funciona no fuso de Brasília |
| Segurança operacional (safety) | pode causar dano físico, à saúde ou ao ambiente? | dose arredondada para cima |

**Escreva o risco como falha → efeito**: "cupom aplicado duas vezes no clique duplo → perda de margem", não "cupom". Risco escrito como funcionalidade não diz o que testar nem quanto custa ignorá-lo.

| Probabilidade sobe com… | Impacto sobe com… |
| --- | --- |
| complexidade (condições, cálculo, estados, concorrência) | perda financeira (direta, estorno, multa, venda perdida) |
| código novo ou muito alterado | obrigação legal ou regulatória |
| integração nova (terceiro, fila, legado) | reputação e cliente-âncora |
| histórico de defeitos no módulo | segurança física e saúde |
| time novo no domínio, rotatividade | alcance: nº de usuários e frequência do fluxo |
| requisito vago ou sem oráculo claro | irreversibilidade (e-mail, pagamento, nota emitida) |
| baixa testabilidade (sem testes, ambiente, dados) | baixa detectabilidade (defeito silencioso até o fechamento do mês) |
| variabilidade (flags, tenants, dispositivos) | — |

Probabilidade vem de quem conhece o código (dev); impacto, de quem conhece o negócio (PO, suporte, jurídico). O QA facilita e consolida. Uma sessão de 30 a 45 minutos com os três resolve a maior parte; nota dada só pelo QA erra nos dois eixos.

**Matriz 1–3 com âncoras** (para notas comparáveis entre pessoas):

| Nota | Probabilidade | Impacto |
| --- | --- | --- |
| 1 | código estável, simples, já coberto | incômodo com contorno fácil, poucos usuários |
| 2 | mudança moderada ou integração conhecida | função importante degradada, contorno existe, custo de suporte |
| 3 | código novo ou complexo, integração nova, histórico de defeitos | perda de dinheiro ou dados, violação legal ou de segurança, fluxo principal parado, efeito irreversível |

| P \ I | 1 | 2 | 3 |
| --- | --- | --- | --- |
| **3** | 3 Médio | 6 Alto | 9 Alto |
| **2** | 2 Baixo | 4 Médio | 6 Alto |
| **1** | 1 Baixo | 2 Baixo | 3 Médio |

Regras: **impacto máximo nunca fica abaixo de Médio** (a multiplicação trata "raro e catastrófico" como "frequente e trivial"); use 1–5 só se a escala 1–3 empatar riscos demais; a ordem relativa importa mais que o número; se mais de um terço dos riscos é "alto", force um ranking.

**Do nível à profundidade:**

| Nível | Profundidade | Técnicas | Regressão automatizada | Além do teste |
| --- | --- | --- | --- | --- |
| Alto | todas as regras, limites, negativos, hostis, concorrência | valor-limite de 3 valores, tabela de decisão completa, transições inválidas, charter dedicado | todo PR, no nível mais barato que prova + 1 E2E do fluxo | revisão focada no risco, alerta em produção, rollback ensaiado |
| Médio | caminho feliz, alternativos e negativos principais | partição e limites de 2 valores | no nível mais barato | exploração curta (30–60 min) |
| Baixo | smoke | checagem rápida, exploração oportunista | só se quase de graça | — |

Exemplo de tabela (portal de RH, módulo de férias, oráculo legal confirmado com o jurídico; trecho):

| ID | Risco (falha → efeito) | Característica | P | I | Nível | Mitigação |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Aceita fracionamento fora das regras (período de 4 dias; nenhum ≥ 14) → passivo trabalhista | Adequação funcional | 3 | 3 | 9 Alto | tabela de decisão para 1, 2 e 3 períodos; limites 4/5 e 13/14 dias em unitário |
| R3 | Gestor aprova férias de outra equipe trocando o ID na API → fraude e exposição de dados | Segurança | 2 | 3 | 6 Alto | teste de autorização na API: cada perfil × recurso de outra equipe, esperado 403/404 |
| R5 | Saldo migrado do legado com dias errados → recusas indevidas | Adequação funcional | 3 | 2 | 6 Alto | reconciliação por filial antes/depois + amostra de 50 casos especiais |
| R7 | Tela de aprovação lenta no pico de dezembro | Desempenho | 1 | 2 | 2 Baixo | smoke de carga com o volume do ano anterior; acompanhar p95 |

Fora do plano: relatório gerencial (sem alteração de código). Risco residual declarado: totais do relatório podem divergir até R5 fechar. (Números de artigos da CLT citados no original do brain: Inferido, confirme com o jurídico.)

Armadilhas: matriz feita uma vez e esquecida (reavalie quando o escopo mudar, após incidente e a cada release grande); misturar risco do produto com risco do projeto (o ambiente atrasar vai para o plano, com contingência); **nenhuma linha não funcional** (desempenho, segurança, acessibilidade) deixa a análise incompleta.

## Níveis, tipos e quadrantes

| Nível | Foco | Pega tipicamente | Dublês | Dono típico |
| --- | --- | --- | --- | --- |
| Componente (unitário) | função, classe, módulo | cálculo, validação, ramos | dependências externas substituídas | dev |
| Integração de componentes | serviço com BD real, fila | mapeamento, query, serialização, transação | só o que está fora do serviço | dev, SDET |
| Contrato (técnica, não nível ISTQB) | consumidor × provedor | campo removido, tipo trocado | o outro lado vem do contrato | dev, SDET |
| Sistema | produto inteiro integrado | fluxos ponta a ponta, não funcional | terceiros virtualizados ou sandbox | QA |
| Integração de sistemas | produto + sistemas externos | protocolo, timeout, idempotência | nenhum, ou sandbox do parceiro | QA e parceiros |
| Aceite | necessidade e obrigações | regra mal entendida, operação inviável | ambiente próximo de produção | negócio, operações |

Tipos atravessam níveis: funcional, não funcional (as características da ISO 25010), caixa-branca e ligados a mudança (confirmação e regressão). Confundir nível com tipo gera planos com "fase de performance" no fim, quando a carga do serviço crítico deveria rodar desde a primeira versão estável.

Quadrantes ágeis (Marick; Crispin e Gregory): Q1 técnico/apoia o time (unitário, integração); Q2 negócio/apoia (exemplos, BDD); Q3 negócio/critica (exploratório, usabilidade, aceite); Q4 técnico/critica (desempenho, carga, segurança, confiabilidade). Use para achar buracos no plano, não como sequência: time com Q1 e Q2 e nada em Q3 e Q4 verifica o que especificou e não descobre o que não imaginou.

## Formato do portfólio

| Formato | Distribuição | Faz sentido quando | Sinal de erro |
| --- | --- | --- | --- |
| Pirâmide | muitos unitários, menos serviço/API, poucos E2E | monólito ou backend com regra rica | unitários que mockam tudo e não pegam defeito de integração |
| Troféu (Dodds) | análise estática na base; integração como faixa maior | frontend pesado (SPA) | testes de detalhe de implementação que quebram em refatoração |
| Favo de mel (Spotify) | maioria de integração do serviço com BD real em contêiner, vizinhos simulados | microsserviços pequenos, risco nas fronteiras; complete com contrato | ambiente compartilhado como única forma de testar |
| Casquinha de sorvete (antipadrão) | muitos E2E e manuais, quase nenhum unitário | nunca como alvo | pipeline de horas, intermitência, ninguém confia no vermelho |

O formato é consequência de **onde os defeitos nascem e quanto custa o feedback**, não regra da empresa: pirâmide no motor de preços, troféu no frontend e favo de mel nos serviços convivem. Não conte testes por camada; pergunte qual nível mais barato prova cada risco (K1).

## Estratégia com pouco tempo

Nunca se corta: riscos altos, o fluxo do dinheiro e o parecer com risco residual. Sai primeiro: risco baixo, cosmético, combinações raras. Caso: frete de e-commerce com tabela nova por região e frete grátis "acima de R$ 199".

**2 horas:** (10 min) pergunte ao dev o que mudou e o que o preocupa; ao PO, o pior cenário → (10 min) liste 5 riscos, escolha 3; a ambiguidade já é achado ("acima de R$ 199" inclui 199,00? antes ou depois do cupom?) → (60 min) teste focado: R$ 198,99 / 199,00 / 199,01, CEP de cada região e de área remota, frete grátis + cupom, carrinho alterado após o cálculo → (20 min) regressão por impacto: checkout com um meio de pagamento e estimativa de frete → (10 min) confirme suíte verde, flag ou rollback e painel → (10 min) parecer: testado, não testado, risco residual.

**2 dias:** dia 1, análise de risco com dev e PO (45 min), condições de teste (partição, limites, tabela de decisão região × peso × frete grátis × cupom), execução e registro; dia 2, a tabela de decisão vira teste parametrizado no serviço com o dev, regressão por impacto, tempo de resposta da cotação com transportadora lenta, 60 min de exploração no celular, parecer.

**2 semanas:** critérios de aceite com exemplos no refinamento; contrato com a API da transportadora; massa por região; testes no pipeline; carga no serviço de cotação com o volume do pico anterior; liberação gradual por flag (10% → 50% → 100%) com métricas comparadas (erro de cotação, conversão, frete médio); acessibilidade da etapa; relatório final com riscos aceitos.

## Regressão

**Por risco:** alto roda sempre; médio quando a área foi tocada; baixo em rodízio ou noturno. **Por impacto:** do diff aos dependentes (código compartilhado, tabelas, eventos e filas, configurações, contratos de API). Ferramentas ajudam a partir do grafo de código (`nx affected`, `jest --findRelatedTests`, `pytest-testmon`; Inferido, confirme na versão instalada), mas não enxergam dependência por **dado**, **configuração** ou **evento**: o smoke dos fluxos críticos roda sempre.

| Camada | Conteúdo | Quando | Orçamento (referência ajustável) |
| --- | --- | --- | --- |
| Smoke | fluxos que geram receita ou bloqueiam tudo | todo deploy, inclusive produção | poucos minutos |
| Regressão crítica | riscos altos, nos níveis mais baratos | todo PR ou merge | até ~15 min, senão o time para de esperar |
| Regressão completa | médios e baixos, combinações | noturna ou pré-release | até a manhã seguinte |

Cada teste paga aluguel (tempo de pipeline, manutenção, análise de falha): regra validada com 20 variações no unitário pede um E2E do fluxo, não mais 20 pela interface. **Aposentar** quando a funcionalidade saiu, duplica outro mais barato, o risco deixou de existir, ninguém age quando falha, ou é intermitente crônico sem dono (quarentena com prazo, depois corrigir ou apagar). Não aposente só porque "nunca falhou": confirme que consegue falhar (mutação; agente `test-auditor`).

## Shift-left e shift-right

**Shift-left:** exemplos no refinamento, testabilidade no design (IDs estáveis, logs, ganchos de dados, flags), análise estática, unitário e contrato no PR, ambiente efêmero por PR. **Shift-right** usa produção como fonte controlada de informação:

| Prática | Quando | Cuidado |
| --- | --- | --- |
| Feature flag | liberar para internos ou beta; kill switch | testar com a flag ligada **e** desligada; flags velhas viram dívida |
| Canary | serviço com tráfego suficiente | métricas e limiares de aborto **antes**; 1% de pouco tráfego não diz nada |
| Dark launch / tráfego espelhado | reescrita de serviço, novo motor de cálculo | bloquear efeitos colaterais (e-mail, cobrança, escrita); dado pessoal copiado segue a LGPD |
| Blue-green | rollback instantâneo | migração de banco deve servir às duas versões |
| Monitoramento sintético | fluxos críticos 24/7, terceiros | contas e pedidos marcados como teste e excluídos de faturamento, estoque e analytics |
| Chaos engineering | sistemas distribuídos com boa observabilidade | começar fora de produção, raio limitado, autorização explícita (SLO e chaos em produção: plugin `sre-observability`) |

**Testar em produção com segurança:** autorização e janela combinadas; contas de teste identificáveis; nenhum dado pessoal real criado ou exposto; operação financeira só com valor mínimo estornável ou modo de teste do provedor, com estorno conferido; preferir leitura; limpar o que criou; carga só com autorização, fora do pico e com botão de aborto. **Observabilidade como oráculo:** métricas técnicas por endpoint (taxa, erros, percentis) e de negócio (pedidos pagos por minuto; 200 com carrinho vazio só aparece na de negócio), logs estruturados com ID de correlação, critério de canário escrito antes (exemplo: "5% por 30 min; aborta se erro do checkout > linha de base + 0,5 ponto percentual ou p95 > linha de base + 20%"). Armadilhas: painel com média (esconde a cauda), alerta sem dono.

## Critérios de entrada, saída e parada

**Entrada:** build no ambiente certo com smoke verde; critérios de aceite claros; dados e acessos prontos; testes do time verdes; nota do que mudou (acordo, não muro). **Saída:** riscos altos com mitigação executada e evidência ou aceitos por escrito por quem decide; nenhum crítico aberto no escopo; altos com contorno e aceite; regressão crítica verde, sem falha inexplicada (vermelho "conhecido" sem análise conta como não verde); critérios de aceite verificados; metas não funcionais medidas.

**Quando parar.** Não achar defeitos não prova que não há. Pare quando a próxima hora valer menos que a informação que traria: riscos altos cobertos, descoberta caindo **apesar de** variar técnica, dado e ambiente (se caiu porque você repete os mesmos testes, não vale), ou a missão mudou. Prazo esgotado antes: declare o que ficou sem teste e o risco que sobra.

## Prontidão para produção e parecer

Critérios objetivos de go/no-go (template `parecer-de-prontidao.md`, checklist maior em `checklist-completo.md`): (1) zero crítico aberto no escopo, altos com contorno e aceite; (2) smoke e regressão crítica verdes em pré-produção com configuração equivalente (flags, integrações, volume); (3) riscos altos mitigados ou aceitos formalmente; (4) metas de desempenho e verificações de segurança feitas, ou risco declarado; (5) migração ensaiada com volume realista, rollback ou roll-forward ensaiado e com tempo medido; (6) painel e alertas para o comportamento novo; (7) flag ou liberação gradual com kill switch; (8) suporte e áreas afetadas informados.

**Risco residual em linguagem de negócio:** *se* [evento], *então* [efeito em dinheiro, clientes ou obrigação]; *probabilidade* [e por quê]; *como detectamos e contornamos*; *quem aceita*. "3 bugs P2 no módulo de frete" não ajuda a decidir; "clientes do Norte podem ver frete indisponível se a transportadora B falhar" ajuda.

Exemplo de parecer (adaptado do brain, números fictícios):

> **Parecer de prontidão: Frete por região v2.** Recomendação: **GO com condições**, liberar para 10% na terça às 10h e ampliar para 100% na quinta se as métricas se mantiverem. Verificado: cálculo das 5 regiões e limite do frete grátis (42 casos automatizados verdes); regressão crítica (68 testes) verde em pré-produção. Não verificado: cotação da transportadora B com tráfego real (sandbox instável); frete grátis com cupom de 100%. Risco residual: se a transportadora B falhar, clientes do Norte veem "frete indisponível" e não compram (cerca de 6% dos pedidos); o alerta de erro de cotação detecta em minutos e a flag volta à tabela antiga em menos de 5 min. Condições: plantão de backend até 20h; aceite do PO para o cupom de 100%.

## Métricas

| Métrica útil | Como medir | Como engana |
| --- | --- | --- |
| Defeitos escapados | achados em produção até N dias após a release, por severidade e área | depende de alguém reportar; normalize por volume de mudança |
| DDP (detecção de defeitos) | antes ÷ (antes + depois) × 100, janela fixa | janela curta infla; defeito pequeno em produção não é reportado |
| DORA | frequência de deploy, lead time, taxa de falha de mudança, tempo de recuperação (2024 acrescentou taxa de retrabalho; Inferido) | otimizar uma isolada |
| Taxa de intermitência | execuções com resultado diferente no mesmo commit ÷ total | retry automático esconde |
| Tempo de pipeline | p50 e p90 até o resultado | média esconde as lentas |
| Cobertura de risco | % dos riscos altos com mitigação executada e evidência | lista de riscos incompleta dá 100% enganoso |

Métricas de vaidade: nº de casos (incentiva fatiar), bugs por QA (incentiva duplicata e pune quem previne), % de cobertura isolada (mede execução), % passando (100% verde pode ser suíte que não verifica nada). Lei de Goodhart: medida que vira meta deixa de ser boa; use pares que se contrapõem (velocidade + estabilidade; cobertura + mutação; achados + escapados), tendência acima de valor absoluto, nunca ligue métrica de teste a avaliação individual e pergunte "que decisão ela muda?".

## Estimativa de esforço

Decomposição (WBS: análise, dados, ambiente, execução, ciclos de reteste, automação, relatório); proporção histórica **da própria organização**; extrapolação após ~20% da execução; Wideband Delphi; três pontos E = (O + 4M + P) ÷ 6, desvio ≈ (P − O) ÷ 6. Exemplo: O=3, M=5, P=13 dias → E = (3 + 20 + 13) ÷ 6 = 6 dias, desvio ≈ 1,7: comunique "cerca de 6 dias, provavelmente entre 4 e 8". Mais estoura: ciclos de reteste (planeje 2 a 3 rodadas e declare a suposição), montar ambiente e dados, dependências, análise de falha de automação, aprendizado do domínio.

## Exemplo resumido: PIX no checkout

Contexto suposto: e-commerce médio adiciona PIX via PSP, QR dinâmico, aviso por webhook, deploy com flags, data promocional imóvel. Detalhes de regras de pagamento pertencem ao plugin `fintech-payments`; aqui só o desenho de teste.

| Risco (falha → efeito) | Nível | Mitigação principal |
| --- | --- | --- |
| Webhook perdido, atrasado ou com erro → cliente pagou e não recebe | Alto | handler com falha e reprocesso; consulta periódica ao PSP; alerta "pago e não liberado há 5 min" |
| Webhook duplicado ou fora de ordem → baixa dupla de estoque | Alto | idempotência pelo ID da transação; mesmo evento 2× e eventos invertidos na integração |
| Webhook forjado marca pedido como pago → fraude | Alto | rejeitar notificação não autenticada; confirmar no PSP antes de liberar |
| Valor cobrado ≠ total (cupom, frete, centavos) | Alto | unitário em centavos inteiros com limites; oráculo independente |
| Pagamento após cancelamento por expiração | Alto | transições inválidas; devolução ou reativação no sandbox |
| Divergência entre pagamentos e pedidos pagos | Alto | reconciliação diária automatizada |
| Estoque preso por QR nunca pago | Médio | liberação de reserva na expiração |

Abordagem: unitário para valor e máquina de estados (inclusive transições proibidas); integração do handler com banco real (idempotência, autenticidade, falha no meio); contrato com o PSP e virtualização de 5xx, timeout, lentidão; 3 E2E no sandbox (paga no prazo, expira, paga após cancelar); charters ("pagar o mesmo QR em dois aparelhos"). Shift-right: flag 5% → 25% → 100% com kill switch e métricas (cobranças geradas × pagas, p95 pagamento → liberação, webhooks com erro, pagos e não liberados). Saída: riscos altos com evidência, reconciliação ensaiada, alertas ativos, roteiro de suporte.
