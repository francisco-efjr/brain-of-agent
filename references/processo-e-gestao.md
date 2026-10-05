# Processo e gestão de qualidade

Como o QA atua no time e na organização: papéis, cerimônias, DoR e DoD,
implantação de QA do zero, decisão entre manual e automatizado, ferramentas de
gestão, rastreabilidade, maturidade, comunicação com gestão, glossário e
carreira. Para decidir *o que* testar e com que profundidade, use
`references/estrategia.md`.

## Sumário

- [Modelos de atuação do QA](#modelos-de-atuação-do-qa)
- [QA nas cerimônias ágeis](#qa-nas-cerimônias-ágeis)
- [DoR e DoD com itens de qualidade](#dor-e-dod-com-itens-de-qualidade)
- [Montar QA do zero: plano de 30, 60 e 90 dias](#montar-qa-do-zero-plano-de-30-60-e-90-dias)
- [Manual ou automatizado](#manual-ou-automatizado)
- [Ferramentas de gestão de testes](#ferramentas-de-gestão-de-testes)
- [Rastreabilidade leve](#rastreabilidade-leve)
- [Maturidade de teste](#maturidade-de-teste)
- [Comunicar qualidade para a gestão](#comunicar-qualidade-para-a-gestão)
- [Glossário PT-BR e inglês](#glossário-pt-br-e-inglês)
- [Carreira em qualidade](#carreira-em-qualidade)

## Modelos de atuação do QA

| Modelo | Como funciona | Funciona bem quando | Risco típico |
| --- | --- | --- | --- |
| QA embarcado | um QA por squad, do refinamento ao deploy; testa, automatiza, explora | produto de risco alto e time ainda sem prática de teste | QA vira gargalo e "dono" da qualidade; dev para de testar |
| Quality coach / enabler | atende vários times; ensina, cria práticas e ferramentas, faz pair testing, não executa tudo | devs já escrevem testes; poucos QAs para muitos times | sem autoridade técnica vira palestra; precisa saber fazer, não só falar |
| Qualidade de todo o time (whole-team) | teste é atividade de todos; especialistas apoiam | práticas maduras: TDD, CI confiável, observabilidade | "todos são responsáveis" vira "ninguém é"; some o olhar crítico de exploração |
| Time de teste separado | testa depois da entrega dos devs | regulação que exige independência; terceirização contratada por escopo | mini-cascata, feedback lento, "jogar por cima do muro" |

Independência de quem testa tem valor real (vê o que o autor não vê) e é
exigida em alguns contextos regulados, mas custa feedback. Busque o mínimo de
independência que o risco exige, não o máximo que a estrutura permite.

**Sinais de que o QA virou gargalo:** histórias acumulam em "em teste" no fim
da sprint; QA testa história da sprint anterior; dev declara pronto sem rodar
nada. Correções: limitar o trabalho em andamento, dev testar a história do
colega, QA parear *antes* do código (exemplos, testabilidade), automação feita
junto com a história, não depois.

## QA nas cerimônias ágeis

| Cerimônia | O que o QA faz | Saída concreta |
| --- | --- | --- |
| Refinamento (three amigos) | pergunta por bordas, erros e riscos; transforma regra em exemplos concretos; aponta testabilidade; sugere fatiar por risco | critérios de aceite com exemplos, riscos e perguntas abertas anotados na história |
| Planning | estima teste junto com o desenvolvimento (não em coluna separada); garante tarefas de dados, ambiente e automação; sinaliza dependências | história com tarefas de teste e capacidade realista |
| Daily | traz bloqueios de teste (ambiente, dados, build quebrado), riscos novos; puxa pareamento; prioriza terminar histórias a começar novas | impedimento visível e acordo de quem pareia com quem |
| Review | demonstra com dados reais, inclusive um caso de borda; diz o que **não** foi verificado; transforma feedback em cenário | stakeholders sabem o estado real, não só o caminho feliz |
| Retro | traz dados: defeitos escapados e onde poderiam ter sido pegos, intermitência, tempo de fila em teste; propõe um experimento | uma ação de melhoria com dono e prazo |

Erro comum: QA calado no refinamento e ativo só na execução. A pergunta "e se
o cliente tiver dois endereços?" vale mais antes do código do que como bug.

## DoR e DoD com itens de qualidade

**Definition of Ready** — a história pode entrar na sprint quando:

- Critérios de aceite têm pelo menos um exemplo concreto por regra, incluindo
  um negativo ("CPF com dígito errado → mensagem X").
- Regras de negócio têm fonte: lei, política, planilha de cálculo, pessoa.
- Dependências (API, terceiro, outro time) identificadas, com acesso ou sandbox.
- Dados de teste necessários identificados e obtíveis sem dado real de cliente.
- Requisitos não funcionais relevantes declarados: desempenho, acessibilidade,
  segurança, LGPD (que dado pessoal entra, por quanto tempo fica).
- Protótipo mostra estados de erro, vazio e carregamento, não só o feliz.
- Cabe na sprint **com** teste e automação incluídos.

**Definition of Done** — a história está pronta quando:

- Critérios de aceite verificados com evidência (teste automatizado ou registro).
- Testes das regras novas no pipeline, verdes, sem intermitência introduzida.
- Regressão automatizada relevante verde; revisão de código inclui os testes.
- Nenhum defeito de severidade alta aberto na história.
- Acessibilidade básica: navegação por teclado, foco visível, rótulos, varredura
  automática sem violação grave.
- Logs e métricas para o comportamento novo; flag configurada, se houver.
- Documentação ou nota de versão atualizada quando muda algo para usuário ou suporte.
- Implantado em homologação (ou em produção atrás de flag).

Armadilhas: DoR virar portão que trava tudo (use como roteiro de conversa);
DoD com 30 itens que ninguém confere; DoD com "100% de cobertura". Automatize no
pipeline (quality gate) o que puder ser verificado por máquina; o resto vira
pergunta rápida na review.

## Montar QA do zero: plano de 30, 60 e 90 dias

Primeira semana, perguntas de diagnóstico: quais fluxos geram receita? O que
quebrou nos últimos três meses e como foi descoberto? Como o código chega à
produção e como se desfaz? O que existe de teste e quem roda? Quem decide o
release? O suporte reclama de quê?

| Fase | Foco | Entregáveis |
| --- | --- | --- |
| Dias 1–30: entender e estancar | mapear fluxos críticos e incidentes; participar dos refinamentos; achar cedo 1 ou 2 problemas relevantes (gera confiança) | mapa de risco com os 10 maiores; checklist de smoke manual (15 min) usado em todo release; padrão de bug report e rotina de triagem; diagnóstico escrito com 3 prioridades |
| Dias 31–60: automatizar o que dói | smoke automatizado dos 3 a 5 fluxos críticos no CI a cada deploy (API primeiro, 1 ou 2 E2E); ambiente e dados de teste estáveis; pair com devs em testes unitários; exploração com cartas nas features novas | pipeline com smoke; DoR e DoD com itens de qualidade; linha de base de defeitos escapados e tempo de pipeline |
| Dias 61–90: escalar e institucionalizar | regressão crítica como quality gate; estratégia de teste escrita (1 a 2 páginas); monitoramento sintético do fluxo crítico; relatório periódico para gestão | estratégia publicada; métricas com tendência; plano dos próximos 6 meses (contratação, coaching, não funcional) |

O que **não** fazer: comprar ferramenta de gestão antes de ter processo;
escrever centenas de casos passo a passo de tudo; automatizar tudo pela
interface; virar portão de aprovação; prometer "zero bugs". Em startup, com
pouco dinheiro e produto mudando toda semana, o peso vai para smoke
automatizado, monitoramento, rollback rápido e exploração — documentação mínima.

## Manual ou automatizado

| Critério | Favorece automatizar | Favorece manual ou exploratório |
| --- | --- | --- |
| Frequência | roda a cada commit ou deploy | roda uma ou duas vezes por ano |
| Estabilidade | regra e interface estáveis | interface ou regra mudando toda semana |
| Risco | regressão de fluxo crítico | área de baixo risco |
| Oráculo | resultado verificável por máquina (valor, estado, registro) | exige julgamento: visual, usabilidade, "faz sentido?" |
| Combinações | muitas (tabela de decisão parametrizada) | poucas |
| Manutenção | seletores estáveis, API, dados controláveis | animações, terceiros instáveis, captcha |
| Determinismo | ambiente controlável | hardware físico, SMS real, impressora |
| Feedback | precisa em minutos | pode esperar |

Automação verifica o que já se sabe; exploração descobre o que não se sabia.
Um não substitui o outro — e a regra testada no nível unitário é quase sempre a
automação mais barata, não a tela.

**Cálculo de ROI.** Ganho mensal = custo manual por execução × execuções no mês
− manutenção mensal − análise de falhas mensal. Payback (meses) = custo de
criação ÷ ganho mensal.

| | Cenário A: regressão do checkout com cartão | Cenário B: exportação trimestral de informe |
| --- | --- | --- |
| Execução manual | 25 min × 20 deploys/mês = 8,3 h/mês | 40 min × 4/ano ≈ 0,2 h/mês |
| Criação da automação | 12 h | 10 h |
| Manutenção + análise de falhas | 1,5 + 0,5 = 2 h/mês | 0,5 h/mês |
| Ganho mensal | 8,3 − 2 = 6,3 h | 0,2 − 0,5 < 0 |
| Payback | 12 ÷ 6,3 ≈ 1,9 mês | nunca, em tempo |

Decisão B: checklist manual e, se erro no informe gera multa, teste unitário da
regra de cálculo (barato), não automação da tela. O tempo não é o único ganho:
automação permite deploy frequente, dá feedback em minutos e executa igual
todas as vezes. Custos ocultos: infraestrutura, intermitência, tempo de
pipeline. Armadilha: comparar com execuções manuais que nunca aconteceriam
("economizamos 300 h") — compare com o que de fato seria executado.

## Ferramentas de gestão de testes

| Ferramenta | Perfil | Vale quando | Atenção |
| --- | --- | --- | --- |
| Jira + Xray | testes como itens do Jira; planos, execuções, cobertura por requisito; importa resultados de automação | time já vive no Jira e precisa de rastreabilidade ou auditoria | apps do Marketplace no Jira Cloud costumam ser cobrados pelo total de usuários do Jira — confirme o modelo |
| Jira + Zephyr | proposta parecida, da SmartBear | idem | existem edições diferentes; confirme qual atende |
| TestRail | ferramenta dedicada, integra com Jira | muito teste manual, vários projetos, relatórios para gestão | mais um sistema para manter sincronizado |
| Qase | dedicada, API e reporters para frameworks | times pequenos e médios, startups | verifique limites do plano gratuito |
| Azure Test Plans | parte do Azure DevOps | quem já usa Boards e Pipelines | recursos completos exigem licenciamento específico |
| Repositório + CI | specs Gherkin ou testes como documentação; relatório do pipeline | time pequeno, automação forte, sem exigência de auditoria | não dá histórico de execução manual nem evidência por versão |

A maioria aceita importar resultado de automação em JUnit XML pelo CI; confirme
o formato e o reporter da sua ferramenta antes de escolher.

**Vale documentar:** estratégia (1 a 2 páginas); riscos e o que ficou fora;
cartas e notas das sessões exploratórias que acharam algo; casos de regressão
manual que ainda existem, como condição + dado + resultado esperado; evidência
de execução quando auditoria exige; parecer de release.

**É burocracia:** passo a passo de algo já automatizado; copiar para a
ferramenta o que já está em Gherkin no repositório; caso "abrir a tela X";
matriz de rastreabilidade mantida à mão que ninguém consulta; plano de 40
páginas que ninguém lê; "passou" sem evidência. Passo a passo detalhado só se
justifica quando quem executa não conhece o sistema ou o auditor exige.

## Rastreabilidade leve

Uma chave comum resolve 80% da rastreabilidade sem planilha: o ID da história
(ex.: `LOJA-123`) aparece no teste, no PR e no bug.

```typescript
// Playwright: tag no teste; filtre com: npx playwright test --grep @LOJA-123
import { test, expect } from '@playwright/test';

test(
  'recusa cupom expirado no checkout',
  { tag: ['@LOJA-123', '@risco-alto'] },
  async ({ page }) => {
    // Supõe um fixture do projeto que cria, via API, um carrinho de R$ 150,00.
    await page.goto('/carrinho');
    await page.getByLabel('Cupom').fill('NATAL2024');
    await page.getByRole('button', { name: 'Aplicar' }).click();
    await expect(page.getByRole('alert')).toHaveText('Cupom expirado em 31/12/2024');
    await expect(page.getByTestId('total-carrinho')).toHaveText('R$ 150,00');
  },
);
```

```gherkin
# language: pt
Funcionalidade: Cupom no checkout

  @LOJA-123 @risco-alto
  Cenário: Cupom expirado é recusado
    Dado um carrinho com total de R$ 150,00
    Quando aplico o cupom "NATAL2024", expirado em 31/12/2024
    Então vejo "Cupom expirado em 31/12/2024"
    E o total continua R$ 150,00
```

- Relatório do CI agrupado por tag = cobertura de requisito gerada, não digitada.
- Bug → história/requisito → teste de regressão criado na correção (com a tag
  do bug). Defeito sem teste que o reproduz volta.
- Duas perguntas que a rastreabilidade precisa responder: "quais testes cobrem
  este requisito?" e "que requisito este teste protege?". Teste que não
  responde à segunda é candidato a aposentar.
- Em contexto regulado, gere a matriz formal a partir das tags e exporte as
  execuções por versão; não mantenha à mão.

## Maturidade de teste

O TMMi (Test Maturity Model integration) é o modelo formal mais usado para
avaliar processo de teste, com avaliação por avaliadores credenciados:

| Nível | Nome | Áreas de processo |
| --- | --- | --- |
| 1 | Inicial | nenhuma; teste caótico, confundido com depuração, depende de heróis |
| 2 | Gerenciado | política e estratégia de teste; planejamento; monitoramento e controle; projeto e execução; ambiente de teste |
| 3 | Definido | organização de teste; programa de treinamento; ciclo de vida e integração; teste não funcional; revisões por pares |
| 4 | Medido | medição de teste; avaliação da qualidade do produto; revisões avançadas |
| 5 | Otimização | prevenção de defeitos; controle de qualidade; otimização do processo de teste |

Avaliação formal faz sentido em organizações grandes, reguladas ou que vendem
serviço de teste. Para a maioria dos times, sinais práticos dizem mais:

| Dimensão | Imaturo | Em evolução | Maduro |
| --- | --- | --- | --- |
| Quando o teste começa | depois que o dev "termina" | em paralelo, na sprint | no refinamento, com exemplos |
| Automação | nenhuma, ou E2E frágil rodado à mão | suíte no CI com intermitência tolerada | gate no pipeline, minutos, intermitência tratada como defeito |
| Release | evento tenso, manual, de madrugada | ensaiado, com checklist | contínuo, com flags e rollback em minutos |
| Defeitos | achados pelo cliente, sem causa raiz | triagem regular | escapados analisados e transformados em prevenção |
| Métricas | nº de casos e de bugs | algumas operacionais | DORA, escapados, intermitência — usadas para decidir |
| Responsabilidade | "o QA aprovou" | QA e devs | time inteiro; QA como especialista e coach |
| Não funcional | só quando quebra | antes de grandes eventos | requisitos explícitos, testes recorrentes, SLOs |

Armadilhas: tratar nível de maturidade como meta em si; pular etapas (automação
sofisticada sem triagem de defeitos nem ambiente estável).

## Comunicar qualidade para a gestão

Comece pela conclusão e pelo que você precisa da gestão; fale em risco para o
negócio, não em contagem de bugs; mostre tendência; cada risco tem dono e data.
Gestor não precisa saber que há "12 bugs abertos" — precisa saber se o
lançamento está em risco, por quê e que decisão cabe a ele.

Exemplo de resumo semanal (dados ilustrativos):

```text
QUALIDADE — Semana 40 — Release 5.2 (PIX no checkout) — previsão 14/10

STATUS: AMARELO — no prazo, com 1 risco alto em aberto.

RISCOS
1. Pedido pago por PIX não é liberado quando o aviso do provedor atrasa mais
   de 10 min (visto 2 vezes em homologação). Efeito: cliente pagou e não
   recebe; chamado no suporte. Dono: time Pagamentos; correção em teste até
   09/10. Tendência: estável.
2. Sandbox do provedor fora do ar por 2 dias: 30% dos testes de integração
   atrasados. Dono: líder técnico, em contato com o provedor. Tendência: piora.

DECISÃO NECESSÁRIA (até 10/10)
Se o risco 1 não fechar até 10/10: lançar com o PIX liberado para 5% dos
clientes e alerta de "pago e não liberado", ou adiar o PIX para a 5.3?

INDICADORES
- Defeitos escapados da 5.1 (30 dias): 2, nenhum crítico (5.0: 5).
- Pipeline p90: 14 min (meta 15). Intermitência: 1,8% (era 3,5%).

PRÓXIMA SEMANA
Teste de carga da geração de cobrança; ensaio de rollback; roteiro do suporte.
```

## Glossário PT-BR e inglês

Termos alinhados ao ISTQB (tradução brasileira do BSTQB) que mais geram
confusão. Em dúvida sobre a tradução oficial, consulte o glossário do ISTQB,
que tem versão em português.

| Inglês | Português | Significado preciso | Confusão comum |
| --- | --- | --- | --- |
| error (mistake) | erro (engano) | ação humana que produz resultado incorreto | chamar tudo de "erro" |
| defect (bug, fault) | defeito | imperfeição em um produto de trabalho (código, requisito) | — |
| failure | falha | comportamento observado diferente do esperado na execução | defeito pode nunca virar falha; falha pode vir do ambiente |
| root cause | causa raiz | razão fundamental que originou o defeito | parar no sintoma ("faltou um if") |
| test basis | base de teste | fonte usada na análise e no projeto: requisito, história, código, norma | — |
| test object | objeto de teste | o que está sendo testado | — |
| test condition | condição de teste | aspecto testável, o "o quê" | confundir com caso de teste |
| test case | caso de teste | pré-condições, entradas, ações e resultados esperados | caso sem resultado esperado concreto |
| test procedure | procedimento de teste | sequência de casos e ações para executar | — |
| test suite | suíte de teste | conjunto de casos ou scripts executados juntos | — |
| test oracle | oráculo de teste | fonte para determinar o resultado esperado | usar o próprio sistema como oráculo |
| testware | testware | artefatos produzidos pelo teste (casos, dados, scripts, relatórios) | — |
| verification / validation | verificação / validação | conforme a especificação / atende à necessidade real | tratar como sinônimos |
| quality assurance / quality control | garantia / controle da qualidade | QA: processo, prevenção; QC: produto, detecção (teste é forma de QC) | "QA" como cargo que só executa teste |
| confirmation testing (re-testing) | teste de confirmação (reteste) | confirma que o defeito foi corrigido | confundir com regressão |
| regression testing | teste de regressão | confirma que a mudança não quebrou o que funcionava | rodar só o reteste e chamar de regressão |
| smoke test | smoke test (teste de fumaça) | verificação rápida de que o build é testável e os fluxos principais vivem | "sanity" tem uso variado; alguns glossários tratam como sinônimo — combine no time |
| test level | nível de teste | componente, integração, sistema, aceite | confundir nível com tipo |
| test type | tipo de teste | funcional, não funcional, caixa-preta, caixa-branca | "fase de performance" no fim |
| component testing | teste de componente | teste isolado de unidade ou módulo | — |
| acceptance testing (UAT) | teste de aceite (do usuário) | confirma que atende à necessidade e às obrigações | QA fazendo UAT no lugar do negócio |
| static testing | teste estático | sem executar: revisão, análise estática | achar que só execução é teste |
| black-box / white-box | caixa-preta / caixa-branca | técnicas baseadas na especificação / na estrutura | — |
| exploratory testing | teste exploratório | aprender, projetar e executar ao mesmo tempo, guiado por carta | confundir com teste ad hoc sem método |
| test charter | carta de teste (charter) | missão, área e tempo de uma sessão exploratória | — |
| product risk / project risk | risco do produto / risco do projeto | o software falhar / o projeto falhar (prazo, recurso) | misturar os dois na mesma matriz |
| entry / exit criteria | critérios de entrada / de saída | condições para começar / encerrar uma atividade | em ágil, aproximam-se de DoR / DoD |
| Definition of Done | Definição de Pronto (DoD) | acordo do time do que é "pronto" | DoD diferente para cada pessoa |
| false positive / false negative | falso positivo / falso negativo | relata defeito que não existe / não detecta defeito que existe | inverter; o "falso verde" é um falso negativo |
| coverage | cobertura | grau em que itens de cobertura foram exercitados | cobertura não é verificação |
| test double (stub, mock, fake, spy) | dublê de teste | substituto de dependência no teste | chamar todo dublê de mock |
| severity / priority | severidade / prioridade | tamanho do estrago / urgência de corrigir | usar uma pela outra |
| flaky test | teste intermitente (flaky) | resultado muda sem mudar código nem dados | tratar como ruído e reexecutar até passar |

## Carreira em qualidade

| Trilha | Foco | Competências-chave | Sinal de senioridade |
| --- | --- | --- | --- |
| Analista de QA | análise de requisitos, projeto de testes, exploração, domínio | técnicas de teste, negócio, comunicação, SQL, API básica | antecipa riscos no refinamento; seus casos pegam defeitos |
| SDET / Quality Engineer | código e infraestrutura de teste | programação, arquitetura de frameworks, CI/CD, contêineres, API, observabilidade | constrói o que o time todo usa; suíte rápida e confiável |
| QA Lead / gestão de qualidade | estratégia, pessoas, processo, métricas | gestão de risco, comunicação executiva, contratação, orçamento | decisões de release apoiadas em dados; time melhora sem depender dele |
| Quality coach | capacitar times | facilitação, ensino, influência sem autoridade, técnica sólida | times testam melhor depois que ele sai |
| Performance | carga, capacidade, gargalos | k6, JMeter ou Gatling, percentis, APM, infraestrutura | explica o gargalo e o limite de capacidade, não só o gráfico |
| Segurança | vulnerabilidades em aplicações | OWASP, HTTP a fundo, Burp ou ZAP, modelagem de ameaças, ética e autorização | prioriza por explorabilidade e impacto; ensina o time a prevenir |
| Acessibilidade | WCAG e tecnologias assistivas | WCAG 2.2, leitores de tela, ARIA, legislação brasileira | audita, explica a barreira para o usuário e propõe correção viável |

**Certificações.** O ISTQB tem a certificação mais reconhecida da área; no
Brasil, o conselho membro é o BSTQB, com exames em português.

- **Fundamentos:** CTFL 4.0 — base e pré-requisito das demais.
- **Avançado:** Test Analyst (CTAL-TA), Technical Test Analyst (CTAL-TTA),
  Test Management (CTAL-TM), Test Automation Engineering (CTAL-TAE) e Agile
  Tester (CTAL-AT).
- **Especialista:** desempenho (CT-PT), segurança (CT-SEC), teste de sistemas
  de IA (CT-AI), teste com IA generativa (CT-GenAI), mobile (CT-MAT),
  estratégia de automação (CT-TAS), usabilidade (CT-UT), aceite (CT-AcT).
- **Fora do ISTQB:** acessibilidade — IAAP (CPACC, fundamentos; WAS, técnico
  web); requisitos — IREB CPRE; segurança ofensiva — certificações práticas de
  pentest (como OSCP) pesam mais que as de teste.

Siglas e versões mudam com frequência: confirme no site do ISTQB ou do BSTQB
antes de recomendar. Certificação abre portas (filtro de RH, consultorias,
setor público e regulado); entrevista sênior avalia prática.

**Perguntas típicas de entrevista**

| Pergunta | Resposta fraca | O que diferencia uma boa resposta |
| --- | --- | --- |
| "Como você testaria esta tela de login?" | lista de casos sem ordem | pergunta contexto (quem usa, o que protege); organiza por risco e característica de qualidade; inclui limites, negativos, segurança (força bruta, enumeração de usuário), acessibilidade; diz o que deixaria de fora |
| "Diferença entre severidade e prioridade, com exemplo" | definição decorada | exemplos próprios: travamento numa tela usada por 0,1% (severidade alta, prioridade baixa); nome do cliente-âncora errado na home (severidade baixa, prioridade alta) |
| "Achou um defeito crítico no dia do release. E aí?" | "bloqueio o release" | reproduz, mede impacto e alcance, leva opções a quem decide (adiar, flag, contorno, liberação parcial) e registra a decisão; QA informa, não decide sozinho |
| "Seu teste automatizado falha às vezes." | "coloco retry" | mede a taxa repetindo N vezes, classifica a causa (espera, dados compartilhados, ordem, ambiente, concorrência real), quarentena com prazo, corrige a raiz |
| "O que você automatizaria primeiro?" | "tudo" ou "os casos manuais" | smoke do fluxo de receita, por risco e frequência, no nível mais barato; justifica o que não automatizaria |
| "Como sabe que testou o suficiente?" | "quando acabaram os casos" | critérios de saída por risco, custo × valor da informação, risco residual declarado |
| "O dev diz que não é bug, é regra." | discute opinião | volta ao oráculo (critério de aceite, norma, expectativa do usuário) e leva ao PO com evidência e impacto |
| "Fale de um defeito que escapou para produção." | culpa alguém | causa raiz no processo e o que mudou depois para não repetir |
| SDET: "Como estruturaria um framework novo?" | "Page Object para tudo" | camadas e por quê, dados de teste, paralelismo, relatórios, integração com CI, critério para testar em API ou interface |

Para quem entrevista: peça para testar algo concreto em 15 minutos e observe
se a pessoa pergunta antes, prioriza e explica o porquê — isso prediz mais que
definições decoradas.
