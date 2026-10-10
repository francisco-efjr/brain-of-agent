# Descoberta e experimentos

Como preparar descoberta com usuários, sintetizar sem fabricar, desafiar premissas e desenhar experimentos antes de olhar o resultado. Leia ao usar `run-discovery`, `write-prd` (seção de riscos) ou o agente `discovery-synthesizer`. Fontes: V-25, V-27, V-32, V-33, V-08 e o processo de premissas do gstack (inspiração, com atribuição). Evidência de ganho de LLM em descoberta é fraca (Inferido): a descoberta continua humana; o modelo prepara e sintetiza.

## Sumário

- [1. Princípio e limite do modelo](#1-princípio-e-limite-do-modelo)
- [2. Os quatro grandes riscos](#2-os-quatro-grandes-riscos)
- [3. Árvore de oportunidades](#3-árvore-de-oportunidades)
- [4. Roteiro de entrevista JTBD de 30 minutos](#4-roteiro-de-entrevista-jtbd-de-30-minutos)
- [5. Síntese sem fabricação](#5-síntese-sem-fabricação)
- [6. Desafio de premissas e alternativas](#6-desafio-de-premissas-e-alternativas)
- [7. Experimento A/B](#7-experimento-ab)
- [8. Lacunas de evidência](#8-lacunas-de-evidência)

## 1. Princípio e limite do modelo

O estudo de expertise da Anthropic (V-08, 2026-06-16, descritivo e correlacional) sustenta apenas o princípio de que a parte humana é decidir **o que construir, o que é pronto e como validar**; o plugin coleta essas três respostas antes de executar. O artigo não prescreve escopo nem verificação em todo pedido; não o cite como guia de escrita de pedido.

Regra de ouro da descoberta: **o modelo nunca inventa fala, número, participante ou tamanho de amostra**. Sem notas ou dados fornecidos, ele pede e para.

## 2. Os quatro grandes riscos

Marty Cagan, SVPG, 2017-12-04 (V-25, classe B): toda ideia precisa passar por quatro riscos, cada um com um dono natural.

| Risco | Pergunta | Dono típico | Pergunta de teste (exemplo) | Evidência que resolve |
| --- | --- | --- | --- | --- |
| Valor | Os clientes vão querer ou comprar? | product manager | "Na última vez que X aconteceu, o que você fez?" (entrevista) | N pessoas relatam o problema com comportamento real |
| Usabilidade | Conseguem descobrir como usar? | designer | Teste com protótipo em 5 tarefas | Tarefas concluídas sem ajuda |
| Viabilidade | Dá para construir com o time, prazo e tecnologia? | líder de engenharia | Spike de 1 a 2 dias; mapa do código (`feasibility-scout`) | Protótipo ou mapa sem bloqueio |
| Negócio | Funciona para o negócio (receita, jurídico, marca, suporte)? | product manager | Revisão com financeiro e jurídico | Aprovação registrada ou restrição conhecida |

Template: [quatro-riscos.md](../assets/templates/quatro-riscos.md). Texto curto e opinativo; o livro INSPIRED não foi lido (V-25). No `ux-ui-design`, usabilidade é aprofundada; aqui é uma linha da matriz.

## 3. Árvore de oportunidades

Teresa Torres (Product Talk; V-32, classe B; o texto é prescritivo, não empírico) com implementação MIT da skill do phuryn/pm-skills. Estrutura: **resultado** (um por árvore) → **oportunidades** (necessidades, dores ou desejos do cliente, vindos de entrevistas) → **soluções** → **testes de premissa**.

Regras:

1. Pré-requisitos: um resultado claro, uma teoria do cliente-alvo e 3 a 4 entrevistas com histórias reais.
2. Uma árvore por resultado.
3. De 3 a 7 oportunidades; foque nas 2 ou 3 melhores; **uma oportunidade-alvo por vez**.
4. Pelo menos 3 soluções por oportunidade-alvo (cerca de 3 na fonte primária): comparar alternativas evita casar com a primeira ideia.
5. Para cada solução escolhida, 1 ou 2 testes de premissa, cada um com **hipótese, método, métrica e limiar** (o que significa "passou").
6. Entrevistas semanais e revisão da árvore a cada 3 a 4 entrevistas (recomendação do método).
7. Opportunity Score só com importância e satisfação reais ([priorizacao-roadmap-okr.md](priorizacao-roadmap-okr.md)).

Template: [arvore-oportunidades.md](../assets/templates/arvore-oportunidades.md). Afirmações como "70% mais rápido" de resumos de terceiros foram descartadas (V-32).

## 4. Roteiro de entrevista JTBD de 30 minutos

Base: skill `interview-script` do phuryn/pm-skills (V-33, MIT, classe B), reescrita; segue a linha do livro The Mom Test, cuja fonte primária não foi lida (lacuna). JTBD (jobs to be done) aqui é vocabulário prático de entrevista; as fontes primárias (Christensen, Ulwick, Moesta) são lacuna: não atribua o conteúdo a elas.

Entradas: objetivo da rodada, premissas a validar, perfil do participante. Saída: roteiro + modelo de anotações + premissas a confrontar.

| Bloco | Tempo | Para quê |
| --- | --- | --- |
| Abertura | 2 a 3 min | consentimento (gravação, uso), tom, "não há resposta certa" |
| Aquecimento | 5 min | contexto do participante: papel, rotina, ferramentas atuais |
| Exploração JTBD | 15 a 20 min | a última vez que o problema ocorreu, passo a passo; alternativas usadas; custo; gatilho da mudança |
| Encerramento | 3 a 5 min | "o que eu deveria ter perguntado?"; indicação de outras pessoas |

Perguntas-modelo sobre o passado (redação própria):

1. Me conte a última vez que você [fez/enfrentou X]. Como foi do começo ao fim?
2. O que levou você a resolver isso naquele dia, e não antes?
3. O que você tentou antes de [solução atual]? O que deu errado?
4. Quanto tempo ou dinheiro isso consumiu na última vez?
5. O que você abriria mão para resolver isso?
6. Quem mais participou ou foi afetado?
7. O que aconteceu depois? Alguém cobrou o resultado?
8. Mostre-me como você faz hoje (se possível, na tela ou no material real).

Regras anti-viés:

1. Pergunte sobre a **vida do participante**, não sobre a ideia.
2. Peça **comportamento passado e específico**; descarte "eu faria", "eu usaria" e "normalmente".
3. Ouça cerca de 80% do tempo.
4. **Não apresente a solução** durante a coleta.
5. Trate **elogio genérico como ruído** ("legal, gostei"); aprofunde com "o que você fez da última vez?".

Verificação do roteiro: nenhuma pergunta sobre opinião futura ("você usaria um app que...?"); toda pergunta pode ser respondida com um episódio real. Os links de "Further Reading" da fonte apontam para um curso pago: não copiar. Privacidade: não cole PII de entrevistados em prompts além do necessário. Templates: [roteiro-entrevista.md](../assets/templates/roteiro-entrevista.md) e [notas-entrevista.md](../assets/templates/notas-entrevista.md).

## 5. Síntese sem fabricação

Executada pelo agente `discovery-synthesizer`. Procedimento:

1. **Exigir arquivos de entrada.** Sem notas ou transcrições, parar e pedir.
2. Dar um **ID a cada nota** (N01, N02...) com participante anonimizado (P1, P2...).
3. Agrupar por tema, com a **contagem de notas e o rótulo do tamanho da amostra** ("4 de 5 participantes relataram X; amostra pequena, não generalizável").
4. Citações **só com trecho literal presente no arquivo**, acompanhadas de ID e localização.
5. Separar **comportamento observado ou relatado** de opinião e elogio genérico.
6. Listar oportunidades (3 a 7), premissas a testar com o teste proposto, contradições e vieses prováveis (pergunta sobre a ideia, amostra pequena, só clientes satisfeitos).
7. Registrar "o que esta amostra não permite concluir".
8. Não recomendar a priorização final: o humano decide.

Formato da tabela de evidências: `tema | nota (ID) | trecho | tipo (comportamento, opinião, pedido de solução)`.

## 6. Desafio de premissas e alternativas

Inspirado nos workflows `office-hours` e `plan-ceo-review` do gstack (garrytan/gstack, MIT, Copyright (c) 2026 Garry Tan; processo reescrito, sem copiar texto, sem preâmbulo de binários, telemetria nem jargão de marca). Use antes de investir em PRD ou spec grande (N4).

**Premissas** (apresente como afirmações que o usuário precisa aceitar ou corrigir):

1. É este o problema certo? Uma moldura diferente produziria uma solução bem mais simples?
2. O que acontece se nada for feito? A dor é real ou hipotética?
3. O que já existe e resolve parte disso (no produto, na empresa, no mercado)?
4. Como o usuário recebe a entrega (distribuição, onboarding, suporte)? Uma entrega sem canal não chega a ninguém.

**Alternativas:** 2 a 3 abordagens distintas, com esforço e risco; uma delas é a **mínima que entrega valor** e outra a de melhor trajetória de longo prazo; recomende uma com a razão ligada ao objetivo declarado e **espere a escolha do humano** antes de documentar.

**Posturas de escopo** (do `plan-ceo-review`, adaptadas; os limiares são Suposição): expandir (produto novo), expansão seletiva (capacidade nova, com cada adição aprovada à parte), manter (correção ou refactor), reduzir (muita coisa ao mesmo tempo; o gstack usa mais de 15 arquivos planejados como gatilho). A escolha de postura não aprova mudanças: cada adição ou corte é decidido à parte.

**Ledger de decisões** (opcional; ver [decisao-produto.md](../assets/templates/decisao-produto.md)): ID, o que foi decidido, evidência, estado atual, estado proposto, status e a aprovação exata do humano com o escopo. Regra herdada: **observação não aprova mudança**.

Perguntas de força do modo "startup" do gstack (realidade da demanda, status quo, especificidade desesperada, cunha mais estreita, observação, ajuste ao futuro): nomes confirmados no cabeçalho do SKILL; o texto detalhado vive em arquivo ausente do snapshot e é **Não verificável**; use os nomes como ponto de partida e desenvolva as perguntas com redação própria.

## 7. Experimento A/B

Base: Evan Miller, "How Not To Run an A/B Test", 2010-04-18 (V-27, classe B; estatística atemporal; cobertura de experimentação continua parcial). Checklist (template: [experimento-ab.md](../assets/templates/experimento-ab.md)):

1. **Hipótese** escrita (mudança, população, efeito esperado e por quê).
2. **Métrica primária** com definição operacional; métricas de guarda.
3. **Efeito mínimo de interesse (δ)**: a menor diferença que justificaria agir.
4. **Variância (σ²)**: para conversão, p(1 - p) com p = taxa base.
5. **Amostra fixa antes de começar**, por braço. Regra de bolso do autor: **n ≈ 16 x σ² / δ²** por braço (parâmetros usuais de 5% de significância e 80% de poder; conferir no artigo, Inferido).
6. **Critério de parada** escrito antes: quando e com que amostra o teste acaba.
7. **Nenhuma espiada com parada por significância.** Olhar o p-valor todo dia e encerrar quando ele cair abaixo de 0,05 infla o falso positivo: dez espiadas com nível nominal de 1% resultam em cerca de 5% real (tabela do artigo, Verificado em V-27).
8. **Alternativas** quando é preciso olhar durante o teste: análise sequencial com checkpoints definidos antes, ou abordagem bayesiana.

Exemplo trabalhado. Pedido: "10 mil visitantes por braço, olho toda manhã e encerro quando p < 0,05; taxa base 4%; quero detectar +0,5 ponto percentual".

- σ² = 0,04 x 0,96 = 0,0384; δ = 0,005 (0,5 ponto percentual).
- n ≈ 16 x 0,0384 / 0,005² = 0,6144 / 0,000025 = **24.576 por braço**.
- 10 mil por braço é insuficiente para esse δ; e a parada oportunista agrava o falso positivo.
- Proposta: fixar n (ou aceitar um δ maior, como 0,8 ponto percentual, que pede cerca de 9.600 por braço) e a data de parada, ou usar análise sequencial com checkpoints combinados antes.

Fora deste plugin: análise estatística avançada (CUPED, SRM, OEC, métricas de guarda no detalhe) é lacuna do atlas e pertence a `/data-science-ml:playbook`; Kohavi, Tang e Xu entram só como bibliografia (classe C).

## 8. Lacunas de evidência

Rotule o conteúdo correspondente como B ou Inferido e não o atribua a fontes não lidas:

1. JTBD sem fonte primária (Christensen, Ulwick, forças de progresso de Moesta).
2. Mom Test: regras vindas de V-33, sem o livro lido.
3. Experimentação: sem OEC, métricas de guarda, SRM nem análise sequencial além de V-27.
4. Métricas de produto: North Star, HEART, AARRR sem fonte aprovada.
5. Reddit, X, YouTube e newsletters não foram lidos; só Hacker News (classe C).
