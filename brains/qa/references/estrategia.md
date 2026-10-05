# Estratégia de testes

Como decidir **o que testar, com que profundidade, em que nível e quando
parar**, partindo do contexto e do risco. Leia para montar estratégia ou plano,
decidir com pouco tempo, escolher a regressão, dar parecer de "está pronto para
produção?" ou definir métricas de qualidade.

## Sumário

- [Perguntas de contexto que mudam a estratégia](#perguntas-de-contexto-que-mudam-a-estratégia)
- [Análise de risco](#análise-de-risco)
- [Níveis, tipos e quadrantes ágeis](#níveis-tipos-e-quadrantes-ágeis)
- [Formato do portfólio de testes](#formato-do-portfólio-de-testes)
- [Estratégia com pouco tempo](#estratégia-com-pouco-tempo)
- [Regressão](#regressão)
- [Shift-left e shift-right](#shift-left-e-shift-right)
- [Critérios de entrada e saída e quando parar](#critérios-de-entrada-e-saída-e-quando-parar)
- [Prontidão para produção](#prontidão-para-produção)
- [Métricas de qualidade](#métricas-de-qualidade)
- [Estimativa de esforço de teste](#estimativa-de-esforço-de-teste)
- [Exemplo completo: checkout com PIX](#exemplo-completo-checkout-com-pix)

## Perguntas de contexto que mudam a estratégia

Faça estas perguntas antes de escolher técnica ou ferramenta. Não precisa de
todas as respostas para começar — declare suposições — mas saiba quais
perguntas, se respondidas de outro jeito, mudariam o plano.

| Pergunta | Respostas que fazem diferença | Como a estratégia muda |
| --- | --- | --- |
| Qual fluxo paga as contas ou cumpre a missão? | checkout, emissão de nota, prescrição, folha | profundidade máxima nele; o resto recebe smoke e exploração proporcional |
| Quem usa, quantos, em que condições? | 20 clientes B2B com configuração própria; milhões no celular; público idoso; usuários de leitor de tela | B2B: teste por configuração dos maiores clientes; B2C massivo: compatibilidade, desempenho, acessibilidade; público vulnerável: capacidade de interação pesa mais |
| Qual o pior efeito realista de uma falha? | incômodo; venda perdida; dinheiro ou dado perdido; dano à saúde | define o teto de impacto; efeito irreversível torna rollback e reconciliação testes obrigatórios |
| Há regulação, auditoria ou contrato? | LGPD, normas do Banco Central, ANVISA, PCI DSS, SLA contratual | evidência rastreável por versão, oráculo na própria norma, trilha de auditoria testada, às vezes independência de quem testa |
| Qual a arquitetura? | monólito, microsserviços, SPA, app nativo, legado, terceiros | define o formato do portfólio, a necessidade de contrato e de virtualização de serviço |
| Como se publica e se desfaz? | deploy contínuo com flag; app em loja; instalação on-premises trimestral | correção barata → mais shift-right e menos varredura antes; correção cara (loja, on-prem, firmware) → pré-release mais profundo, porque o defeito convive semanas com o usuário |
| Qual o prazo e o que é imóvel? | Black Friday, prazo legal, contrato | congele escopo; priorize regressão do crítico e contingência (flag, rollback) em vez de ampliar cobertura |
| Qual a maturidade do time? | sem CI nem testes; TDD e pipeline confiável | baixa: comece por smoke automatizado e checklist de release; alta: QA foca em risco, exploração e não funcional |
| O que já existe e o que já quebrou? | suíte atual, incidentes, chamados de suporte | incidentes e chamados são a melhor estimativa de probabilidade disponível |
| Quem decide o go/no-go? | PO, diretoria, comitê de mudança | define formato e vocabulário do parecer |

Armadilha: virar interrogatório e não entregar nada. Em 15 minutos com dev e PO
você responde a maioria; o resto vira suposição declarada no plano.

## Análise de risco

### Identificar: funcionalidade × característica de qualidade

Cruze cada funcionalidade (ou cada mudança) com as características do modelo
de qualidade de produto da ISO/IEC 25010. A edição de 2023 tem nove; muito
material ainda reproduz a de 2011, com oito (sem segurança operacional e com
"usabilidade" e "portabilidade" onde hoje estão capacidade de interação e
flexibilidade). Use o cruzamento como lembrete, não como formulário: a maioria
das células fica vazia, e tudo bem.

| Característica | Pergunta-gatilho | Exemplo de risco |
| --- | --- | --- |
| Adequação funcional | faz o certo, completo e com resultado correto? | desconto aplicado duas vezes |
| Eficiência de desempenho | responde a tempo sob a carga esperada sem esgotar recursos? | cotação de frete acima de 5 s no pico |
| Compatibilidade | convive e troca dados com outros sistemas e versões? | app antigo quebra com campo novo na API |
| Capacidade de interação (inclui acessibilidade) | a pessoa usa sem errar, inclusive com teclado e leitor de tela? | erro de formulário não anunciado |
| Confiabilidade | continua funcionando e se recupera de falhas? | aviso de pagamento perdido deixa pedido pendente |
| Segurança (security) | só quem pode acessa e altera? Fica registrado? | trocar o ID na URL mostra pedido de outra pessoa |
| Manutenibilidade | dá para mudar e testar sem medo? | mesma regra duplicada em três serviços |
| Flexibilidade | adapta-se a outro ambiente, escala, configuração? | só funciona no fuso de Brasília |
| Segurança operacional (safety) | pode causar dano físico, à saúde ou ao ambiente? | dose arredondada para cima |

Outras fontes de risco: diff da mudança, incidentes e chamados recentes,
módulos com mais defeitos (defeitos se agrupam), a pergunta "onde você tem
medo?" ao dev e "do que o cliente mais reclama?" ao suporte.

Escreva o risco como **falha → efeito**: "cupom aplicado duas vezes no clique
duplo → perda de margem", não "cupom". Risco escrito como funcionalidade não diz
o que testar nem quanto custa ignorá-lo.

### Fatores de probabilidade e de impacto

| Probabilidade sobe com… | Impacto sobe com… |
| --- | --- |
| complexidade: muitas condições, cálculo, estados, concorrência | perda financeira: direta, estorno, multa, venda perdida |
| código novo ou muito alterado, refatoração grande | obrigação legal ou regulatória (LGPD, trabalhista, fiscal, setorial) |
| integração: terceiro, fila, legado, formato de dado novo | reputação: exposição pública, cliente-âncora |
| histórico de defeitos ou incidentes no módulo | segurança física e saúde |
| time novo no domínio ou na tecnologia, rotatividade | alcance: nº de usuários e frequência de uso do fluxo |
| requisito vago, instável ou sem oráculo claro | irreversibilidade: e-mail enviado, pagamento feito, nota emitida não voltam |
| baixa testabilidade: sem testes, sem ambiente, sem dados | baixa detectabilidade: defeito silencioso que só aparece no fechamento do mês |
| variabilidade: flags, tenants, dispositivos, configurações | — |

Probabilidade vem principalmente de quem conhece o código (dev); impacto, de
quem conhece o negócio (PO, suporte, jurídico). O QA facilita e consolida. Uma
sessão de 30 a 45 minutos com os três resolve a maior parte; nota dada só pelo
QA erra nos dois eixos.

### Matriz probabilidade × impacto

Escala 1–3 com âncoras, para que notas sejam comparáveis entre pessoas:

| Nota | Probabilidade | Impacto |
| --- | --- | --- |
| 1 | código estável, simples, já coberto por testes | incômodo com contorno fácil, poucos usuários |
| 2 | mudança moderada ou integração conhecida | funcionalidade importante degradada, contorno existe, custo de suporte |
| 3 | código novo ou complexo, integração nova, histórico de defeitos | perda de dinheiro ou de dados, violação legal ou de segurança, fluxo principal parado, efeito irreversível |

| P \ I | 1 | 2 | 3 |
| --- | --- | --- | --- |
| **3** | 3 Médio | 6 Alto | 9 Alto |
| **2** | 2 Baixo | 4 Médio | 6 Alto |
| **1** | 1 Baixo | 2 Baixo | 3 Médio |

- **Impacto máximo nunca fica abaixo de Médio.** A multiplicação trata "raro e
  catastrófico" como "frequente e trivial", e é o primeiro que derruba empresa.
- Use 1–5 quando a escala 1–3 empatar riscos demais ou a organização já usar
  1–5. Faixas sugeridas: 15–25 alto, 8–12 médio, 1–6 baixo, com a mesma regra
  para impacto 5.
- A ordem relativa importa mais que o número. Não gaste uma hora discutindo se
  é 3 ou 4; se mais de um terço dos riscos é "alto", force um ranking.

### Do nível de risco à profundidade de teste

| Nível | Profundidade | Técnicas | Regressão automatizada | Além do teste |
| --- | --- | --- | --- | --- |
| Alto | todas as regras, limites, negativos, hostis e concorrência | valor-limite com 3 valores, tabela de decisão completa, transições inválidas, carta exploratória dedicada | em todo PR, no nível mais barato que prova a regra + 1 ponta a ponta do fluxo | revisão de código focada no risco, alerta em produção, rollback ensaiado |
| Médio | caminho feliz, alternativos e negativos principais | partição e limites com 2 valores | no nível mais barato | exploração curta (30–60 min) |
| Baixo | smoke | checagem rápida, exploração oportunista | só se for quase de graça | — |

### Exemplo de tabela de riscos preenchida

Contexto: portal de RH, novo módulo de solicitação e aprovação de férias,
escala 1–3. Oráculo legal: CLT, arts. 134 e 145, validado com o jurídico.

| ID | Risco (falha → efeito) | Característica | P | I | Nível | Mitigação |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Aceita fracionamento fora da CLT (período de 4 dias; nenhum período ≥ 14 dias) → passivo trabalhista | Adequação funcional | 3 | 3 | 9 Alto | tabela de decisão para 1, 2 e 3 períodos; limites 4/5 e 13/14 dias em teste unitário da regra |
| R2 | Permite início nos 2 dias antes de feriado ou do repouso semanal → infração | Adequação funcional | 3 | 3 | 9 Alto | casos com feriados nacionais e municipais da cidade de cada filial, virada de ano, escala com folga fora do domingo |
| R3 | Gestor aprova férias de outra equipe trocando o ID na API → fraude e exposição de dados | Segurança | 2 | 3 | 6 Alto | teste de autorização na API: cada perfil × recurso de outra equipe, esperado 403/404 |
| R4 | Pedido de pagamento chega à folha depois de 2 dias antes do início → descumprimento do art. 145 | Confiabilidade | 2 | 3 | 6 Alto | contrato com a API da folha; teste do agendamento com início em segunda após feriado; alerta se o lote não sair |
| R5 | Saldo migrado do legado com dias errados → recusas indevidas | Adequação funcional | 3 | 2 | 6 Alto | reconciliação de totais por filial antes e depois + amostra de 50 casos especiais (afastamento, admissão recente) |
| R6 | Erro no calendário não é anunciado pelo leitor de tela | Capacidade de interação | 2 | 2 | 4 Médio | varredura axe + roteiro manual com NVDA no fluxo de solicitação |
| R7 | Tela de aprovação lenta no pico de dezembro | Eficiência de desempenho | 1 | 2 | 2 Baixo | smoke de carga com o volume de dezembro anterior; acompanhar p95 em produção |

Fora do plano: relatório gerencial de férias (sem alteração de código).
Risco residual declarado: totais do relatório podem divergir até R5 fechar.

Armadilhas que separam análise amadora de profissional:

- **Matriz feita uma vez e esquecida.** Reavalie quando o escopo mudar, depois
  de incidente e a cada release grande.
- **Misturar risco do produto com risco do projeto.** O software falhar define
  profundidade de teste; o ambiente atrasar vai para o plano, com contingência.
- **Nenhuma linha não funcional.** Se a tabela não fala de desempenho,
  segurança ou acessibilidade, a análise está incompleta — não o produto seguro.

## Níveis, tipos e quadrantes ágeis

| Nível | Objeto e foco | Pega tipicamente | Dublês | Dono típico |
| --- | --- | --- | --- | --- |
| Componente (unitário) | função, classe, módulo | regra de cálculo, validação, ramos | dependências externas substituídas | dev |
| Integração de componentes | serviço com BD real, ORM, fila | mapeamento, query, serialização, transação | só o que está fora do serviço | dev, SDET |
| Contrato (técnica, não nível ISTQB) | acordo consumidor × provedor | campo removido, tipo trocado, enum novo | o outro lado vem do contrato | dev, SDET |
| Sistema | produto inteiro em ambiente integrado | fluxos ponta a ponta, não funcional | terceiros virtualizados ou sandbox | QA |
| Integração de sistemas | produto + sistemas externos reais | protocolo, timeout, idempotência com terceiro | nenhum, ou sandbox do parceiro | QA e parceiros |
| Aceite (usuário, operacional, regulatório, contratual) | atende à necessidade e às obrigações? | regra mal entendida, operação inviável | ambiente próximo de produção | negócio, operações |

Tipos atravessam níveis: **funcional** (o quê), **não funcional** (quão bem —
as características da ISO 25010), **caixa-branca** (estrutura) e **ligados a
mudança** (confirmação de correção e regressão). Confundir nível com tipo gera
planos como "fase de teste de performance" no fim, quando a carga do serviço
crítico deveria rodar desde a primeira versão estável.

Quadrantes ágeis (Brian Marick, popularizados por Lisa Crispin e Janet Gregory):

| | Apoiam o time (guiam o desenvolvimento) | Criticam o produto (avaliam o resultado) |
| --- | --- | --- |
| **Voltados ao negócio** | Q2: exemplos, testes de história/BDD, protótipos, testes funcionais | Q3: exploratório, usabilidade, aceite do usuário, alfa/beta |
| **Voltados à tecnologia** | Q1: unitários, de componente, de integração (TDD) | Q4: desempenho, carga, segurança, confiabilidade |

Use os quadrantes para achar buracos no plano, não como sequência: os números
não são ordem. Time com Q1 e Q2 automatizados e nada em Q3 e Q4 verifica o que
especificou e não descobre o que não imaginou.

## Formato do portfólio de testes

| Formato | Distribuição | Faz sentido quando | Sinal de que está errado |
| --- | --- | --- | --- |
| Pirâmide (Mike Cohn) | muitos unitários, menos de serviço/API, poucos ponta a ponta | monólito ou backend com lógica de domínio rica (cálculo, regras, estados) | unitários que mockam tudo e não pegam defeito de integração |
| Troféu (Kent C. Dodds) | análise estática na base; integração como faixa maior; poucos unitários e E2E | frontend pesado (SPA), em que o defeito mora na composição de componentes, estado e chamadas | testes de detalhe de implementação que quebram a cada refatoração |
| Favo de mel (engenharia do Spotify) | maioria de testes de integração do serviço (serviço real + BD real em contêiner, vizinhos simulados); poucos de detalhe; quase nenhum "integrado" que depende de outro serviço estar correto | microsserviços pequenos com pouca lógica interna; o risco está nas fronteiras; complete com contrato | ambiente compartilhado com todos os serviços como única forma de testar |
| Casquinha de sorvete (anti-padrão) | muitos E2E e manuais, quase nenhum unitário | nunca como alvo | pipeline de horas, falhas intermitentes, ninguém confia no vermelho |

O formato é consequência de **onde os defeitos nascem e quanto custa o
feedback**, não regra da empresa: um produto pode ter pirâmide no motor de
preços, troféu no frontend e favo de mel nos serviços. Não conte testes por
camada para "acertar o desenho"; pergunte qual nível mais barato prova cada risco.

## Estratégia com pouco tempo

Nunca se corta: riscos altos, o fluxo do dinheiro e o parecer com risco
residual. Sai primeiro: risco baixo, cosmético, combinações raras. Exemplo:
frete de e-commerce com tabela nova por região e frete grátis "acima de R$ 199".

**2 horas**

1. (10 min) Pergunte ao dev o que mudou (diff, flags) e o que o preocupa; ao
   PO, o pior cenário.
2. (10 min) Liste 5 riscos, escolha 3. A ambiguidade já é um achado: "acima de
   R$ 199" inclui R$ 199,00? O limite vale antes ou depois do cupom?
3. (60 min) Teste focado: R$ 198,99 / 199,00 / 199,01; CEP de cada região e de
   uma área remota; frete grátis + cupom; carrinho alterado depois do cálculo.
4. (20 min) Regressão por impacto: checkout com um meio de pagamento e a
   estimativa de frete na página de produto.
5. (10 min) Confirme suíte verde, flag ou rollback e painel da cotação.
6. (10 min) Parecer: o que foi testado, o que não foi, risco residual.

**2 dias**

- Dia 1: análise de risco com dev e PO (45 min); condições de teste com
  partição, limites e tabela de decisão (região × peso × frete grátis × cupom);
  execução e registro de defeitos.
- Dia 2: a tabela de decisão vira teste parametrizado no serviço de frete,
  com o dev; regressão selecionada por impacto; tempo de resposta da cotação
  com a transportadora lenta; 60 min de exploração no celular; parecer.

**2 semanas**

- Entra no refinamento: critérios de aceite com exemplos, ambiguidade
  resolvida antes do código.
- Contrato com a API da transportadora; massa de dados por região; testes no
  pipeline; carga no serviço de cotação com o volume do pico anterior.
- Liberação gradual por flag (10% → 50% → 100%) com métricas comparadas:
  erro de cotação, conversão no checkout, frete médio.
- Acessibilidade da etapa de frete; relatório final com riscos aceitos.

## Regressão

**Seleção por risco.** Testes de risco alto rodam sempre; médio, quando a área
foi tocada; baixo, em rodízio ou na suíte noturna.

**Seleção por análise de impacto.** Do diff aos testes: componentes alterados
→ quem depende deles (código compartilhado, tabelas, eventos e filas,
configurações, contratos de API) → testes dessas áreas. Ferramentas ajudam a
partir do grafo de código: `nx affected` em monorepos Nx, `jest
--findRelatedTests` e `--changedSince`, `pytest-testmon`, mapas de cobertura
por teste. Elas não enxergam dependência por **dado** (dois sistemas lendo a
mesma tabela), por **configuração** ou por **evento** — por isso o smoke dos
fluxos críticos roda sempre, independentemente da análise.

**Camadas de execução** (valores de referência; ajuste ao seu pipeline):

| Camada | Conteúdo | Quando roda | Orçamento de tempo |
| --- | --- | --- | --- |
| Smoke | fluxos que geram receita ou bloqueiam tudo | a cada deploy, inclusive em produção | poucos minutos |
| Regressão crítica | riscos altos, nos níveis mais baratos | a cada PR ou merge | até ~15 min, senão o time para de esperar |
| Regressão completa | riscos médios e baixos, combinações | noturna ou antes de release | o que couber até a manhã seguinte |

**Manter enxuta.** Cada teste paga aluguel: tempo de pipeline, manutenção,
análise de falha. Regra validada com 20 variações no unitário precisa de um
ponta a ponta do fluxo, não de mais 20 pela interface.

**Quando aposentar um teste:** a funcionalidade saiu; o teste duplica outro em
nível mais barato; o risco que ele cobria deixou de existir; ninguém age quando
ele falha; é intermitente crônico sem dono (quarentena com prazo, depois
corrigir ou apagar). **Não** aposente só porque "nunca falhou": teste de risco
alto é seguro, não desperdício — mas confirme que ele *consegue* falhar
(quebre a regra de propósito ou use teste de mutação).

## Shift-left e shift-right

**Shift-left** antecipa a informação: exemplos no refinamento, testabilidade no
design (IDs estáveis, logs, ganchos para dados, flags), análise estática,
unitário e contrato no PR, ambiente efêmero por PR. Defeito achado aqui custa
uma conversa, não um incidente.

**Shift-right** aceita que parte do risco só aparece com tráfego real e
transforma produção em fonte controlada de informação:

| Prática | O que é | Quando usar | Cuidado |
| --- | --- | --- | --- |
| Feature flag | código publicado desligado, ligado por público | liberar para internos ou beta; kill switch | teste com a flag ligada **e** desligada; flags velhas viram dívida e combinações explosivas |
| Canary | nova versão recebe pequena fração do tráfego e é comparada à estável | serviços com tráfego suficiente para estatística | defina métricas e limiares de aborto **antes**; 1% de pouco tráfego não diz nada |
| Dark launch / tráfego espelhado | nova versão recebe cópia do tráfego; respostas descartadas e comparadas | reescrita de serviço, novo motor de cálculo | bloqueie efeitos colaterais (e-mail, cobrança, escrita); dados pessoais copiados seguem a LGPD |
| Blue-green | dois ambientes, troca de roteamento | rollback instantâneo | migração de banco precisa servir às duas versões |
| Monitoramento sintético | robô executa transações reais periodicamente | fluxos críticos 24/7, dependências de terceiros | contas e pedidos marcados como teste e excluídos de faturamento, estoque e analytics |
| Chaos engineering | falhas injetadas de forma controlada | sistemas distribuídos com boa observabilidade | comece fora de produção, raio de impacto limitado, autorização explícita |

**Testar em produção com segurança:** autorização e janela combinadas; contas
de teste identificáveis e excluídas de relatórios, cobrança e marketing; nenhum
dado pessoal real criado ou exposto; operação financeira só com valor mínimo
estornável ou modo de teste do provedor, e estorno conferido; preferir leitura;
limpar o que criou; carga em produção só com autorização, fora do pico e com
botão de aborto.

**Observabilidade como oráculo.** Em produção, o resultado esperado vem das
métricas:

- Técnicas por endpoint (taxa, erros, duração em percentis) **e de negócio**
  (pedidos pagos por minuto, conversão). Status 200 com carrinho vazio só
  aparece na métrica de negócio.
- Logs estruturados com ID de correlação, para ligar a falha de um teste ao
  rastro da requisição; rastreamento distribuído para achar onde nasce a
  latência.
- Critério de canário escrito antes de liberar, por exemplo: "5% por 30 min;
  aborta se erro do checkout > linha de base + 0,5 ponto percentual ou p95 >
  linha de base + 20%".
- Armadilhas: painel com média (esconde a cauda); alerta sem dono; métrica que
  ninguém olhou antes do incidente.

## Critérios de entrada e saída e quando parar

**Entrada** (pronto para testar): build no ambiente certo com smoke verde;
critérios de aceite claros; dados e acessos prontos; testes do time verdes;
nota do que mudou. Em ágil é um acordo, não um muro: "não testo até estar
perfeito" só move a fila.

**Saída** (pronto para decidir):

- Todos os riscos altos com mitigação executada e evidência, ou aceitos por
  escrito por quem decide.
- Nenhum defeito crítico aberto no escopo; altos com contorno documentado e
  aceite.
- Regressão crítica verde, sem falha inexplicada (vermelho "conhecido" sem
  análise conta como não verde).
- Critérios de aceite verificados; metas não funcionais medidas.

**Quando parar.** Não achar defeitos não prova que não há defeitos. Pare quando
a próxima hora de teste valer menos que a informação que traria: riscos altos
cobertos, descoberta caindo **apesar de** variar técnica, dado e ambiente (se
caiu porque você repete os mesmos testes, não vale), ou a missão mudou. Se o
prazo acabou antes, declare o que ficou sem teste e o risco que sobra.

## Prontidão para produção

Critérios objetivos de go/no-go (use `assets/templates/checklist-release.md`):

1. Defeitos: zero crítico aberto no escopo; altos com contorno e aceite.
2. Smoke e regressão crítica verdes em pré-produção com configuração
   equivalente à de produção (flags, integrações, volume de dados).
3. Riscos altos 100% mitigados ou aceitos formalmente.
4. Não funcional: metas de desempenho e verificações de segurança feitas, ou
   risco declarado.
5. Migração ensaiada com volume realista; rollback (ou roll-forward) ensaiado e
   com tempo medido.
6. Painel e alertas para o comportamento novo; plantão sabe o que olhar.
7. Flag ou liberação gradual com kill switch, quando aplicável.
8. Suporte e áreas afetadas informados.

**Risco residual em linguagem de negócio.** Use a forma: *se* [evento],
*então* [efeito em dinheiro, clientes ou obrigação]; *probabilidade* [e por
quê]; *como detectamos e contornamos*; *quem aceita*. "3 bugs P2 no módulo de
frete" não ajuda ninguém a decidir; "clientes do Norte podem ver frete
indisponível se a transportadora B falhar" ajuda.

Exemplo de parecer:

> **Parecer de prontidão — Frete por região v2 — 07/10**
>
> - **Recomendação: GO com condições** — liberar para 10% dos clientes na
>   terça, 10h; ampliar para 100% na quinta se as métricas se mantiverem.
> - **Verificado:** cálculo das 5 regiões e limite do frete grátis (42 casos
>   automatizados no serviço, verdes); checkout em Chrome, Safari iOS e
>   Android; regressão crítica (68 testes) verde em pré-produção.
> - **Não verificado:** cotação da transportadora B com tráfego real (sandbox
>   instável); frete grátis com cupom de 100% (combinação rara).
> - **Risco residual:** se a transportadora B falhar, clientes do Norte veem
>   "frete indisponível" e não compram (cerca de 6% dos pedidos); o alerta de
>   erro de cotação detecta em minutos e a flag volta à tabela antiga em < 5 min.
> - **Condições:** plantão de backend até 20h; aceite do PO para o cupom de 100%.

## Métricas de qualidade

| Métrica útil | Como medir | Para que serve | Como engana |
| --- | --- | --- | --- |
| Defeitos escapados | achados em produção até N dias após a release, por severidade e área | eficácia real da estratégia | depende de alguém reportar; normalize por volume de mudança |
| DDP (percentual de detecção de defeitos) | antes ÷ (antes + depois) × 100, em janela fixa (ex.: 30 dias) | tendência de detecção | janela curta infla o número; defeito pequeno em produção nunca é reportado |
| DORA | frequência de deploy, lead time de mudança, taxa de falha de mudança, tempo de recuperação de deploy com falha; o relatório de 2024 acrescentou taxa de retrabalho | equilíbrio entre velocidade e estabilidade | otimizar uma isolada (deploy diário com muita falha) |
| Taxa de intermitência | execuções com resultado diferente no mesmo commit ÷ total | confiança no vermelho | retry automático esconde |
| Tempo de pipeline | p50 e p90 até o resultado | velocidade de feedback | média esconde as execuções lentas |
| Cobertura de risco | % dos riscos altos com mitigação executada e evidência | o que o plano cobriu de fato | lista de riscos incompleta dá 100% enganoso |

| Métrica de vaidade | Por que engana |
| --- | --- |
| Nº de casos de teste | incentiva fatiar casos; 500 rasos protegem menos que 50 bons |
| Bugs por QA | incentiva duplicatas e briga com dev; pune quem previne defeito |
| % de cobertura de código isolada | mede execução, não verificação; meta gera asserção vazia |
| % de testes passando | 100% verde pode ser suíte que não verifica nada |

**Lei de Goodhart:** quando uma medida vira meta, deixa de ser boa medida.
Defesas: métricas em pares que se contrapõem (velocidade + estabilidade;
cobertura + score de mutação; defeitos achados + escapados); tendência acima de
valor absoluto; nunca ligar métrica de teste a avaliação individual; para cada
métrica, responder "que decisão ela muda?" — se nenhuma, pare de coletar.

## Estimativa de esforço de teste

| Técnica | Como funciona | Limitação |
| --- | --- | --- |
| Decomposição (WBS) | quebra em atividades: análise, dados, ambiente, execução, ciclos de reteste, automação, relatório | esquece o que ninguém listou; base para as demais |
| Proporção | usa a relação histórica teste/desenvolvimento **da própria organização** | proporção de outro contexto não vale; mudança de tecnologia invalida |
| Extrapolação | mede o ritmo no início da execução e projeta o resto | só funciona depois de começar; reestime após ~20% |
| Wideband Delphi / planning poker | estimativas independentes, discussão das divergências, nova rodada | depende de quem estima; ancoragem no primeiro número |
| Três pontos | E = (O + 4M + P) ÷ 6; desvio ≈ (P − O) ÷ 6 | o pessimista costuma ser otimista demais |

Exemplo de três pontos: otimista 3 dias, mais provável 5, pessimista 13 →
E = (3 + 20 + 13) ÷ 6 = 6 dias; desvio ≈ 1,7. Comunique "cerca de 6 dias,
provavelmente entre 4 e 8", nunca só "6".

O que mais estoura estimativa: ciclos de reteste (cada rodada de correção pede
reteste e regressão — planeje 2 a 3 rodadas e declare a suposição), montar
ambiente e dados, espera por dependências, análise de falha de automação e
aprendizado do domínio. Estimativa de teste depende da qualidade do que chega:
diga "supondo até 2 rodadas de correção" para que a estimativa não vire
promessa incondicional.

## Exemplo completo: checkout com PIX

Contexto (suposto): e-commerce médio adiciona PIX ao checkout web. Um
provedor (PSP) gera cobrança com QR Code dinâmico e avisa o pagamento por
webhook. Deploy contínuo com flags; lançamento antes de uma data promocional.
Detalhes do domínio PIX estão em `references/dominios.md`.

**Riscos principais (falha → efeito)**

| Risco | Nível | Mitigação principal |
| --- | --- | --- |
| Pagamento confirmado, pedido não liberado (webhook perdido, atrasado ou com erro) → cliente pagou e não recebe | Alto | teste do handler com falha e reprocesso; consulta periódica ao PSP para cobranças pendentes; alerta "pago e não liberado há 5 min" |
| Webhook duplicado ou fora de ordem → baixa dupla de estoque ou pedido duplicado | Alto | idempotência pelo identificador da transação; mesmo evento 2x e eventos invertidos no teste de integração |
| Webhook forjado marca pedido como pago → fraude | Alto | rejeitar notificação não autenticada; confirmar o pagamento no PSP antes de liberar |
| Valor cobrado ≠ total do pedido (cupom, frete, centavos) → perda ou reclamação | Alto | unitário do cálculo em centavos inteiros com limites; oráculo independente (planilha de casos) |
| Pagamento chega depois do cancelamento por expiração → cliente paga pedido cancelado | Alto | transições de estado inválidas; devolução automática ou reativação testada no sandbox |
| Divergência entre pagamentos recebidos e pedidos pagos → prejuízo invisível | Alto | reconciliação diária automatizada, ensaiada com dados do sandbox |
| Estoque preso por QR nunca pago → venda perdida no pico | Médio | teste da liberação de reserva na expiração |
| Geração de cobrança lenta no pico (PSP com latência) → abandono | Médio | carga com PSP virtualizado e latência injetada; timeout e mensagem testados |
| Tela do QR ruim no celular ou com leitor de tela ("copia e cola" sem rótulo) | Médio | exploração em dispositivos reais; axe e teste com leitor de tela |

**Abordagem por nível:** unitário para cálculo do valor e máquina de estados
do pedido (inclusive transições proibidas, como pago → aguardando);
integração do handler de webhook com banco real (idempotência, autenticidade,
falha no meio); contrato com a API do PSP e virtualização para 5xx, timeout e
lentidão; 3 fluxos ponta a ponta no sandbox (paga no prazo, expira, paga após
cancelar); cartas exploratórias ("pagar o mesmo QR em dois aparelhos",
"recarregar e voltar na tela do QR", "dois pedidos abertos").

**Shift-right:** flag libera PIX para 5% → 25% → 100%. Métricas: cobranças
geradas × pagas, tempo pagamento → liberação (p95), webhooks com erro, pedidos
pagos e não liberados, divergência da reconciliação. Kill switch esconde o PIX
do checkout sem afetar cobranças já emitidas.

**Fora de escopo e risco residual:** app nativo (só web nesta fase); PIX
recorrente. Saída: os seis riscos altos com evidência, reconciliação ensaiada,
alertas ativos e roteiro do suporte para "paguei e não liberou".
