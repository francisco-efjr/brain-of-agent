# Pesquisa com usuários e avaliação heurística

Métodos, procedimentos e sinais de alerta para decidir o que validar com pessoas e o que um modelo pode apenas opinar. Fontes: NN/g (V-11, V-17, V-18, V-19), skill `user-research` da Anthropic (V-15, Apache-2.0, redação própria), `ux-research` de Rampstack (V-16, heurísticas do autor). Fora de escopo: survey, personas, JTBD e síntese quantitativa (lacuna; encaminhe a `/product-discovery-specs:playbook`).

## Sumário

- [Escolher o método](#escolher-o-método)
- [Heurísticas de Nielsen](#heurísticas-de-nielsen)
- [Avaliação heurística](#avaliação-heurística)
- [Severidade de 0 a 4](#severidade-de-0-a-4)
- [Entrevista de 50 minutos](#entrevista-de-50-minutos)
- [Teste de usabilidade](#teste-de-usabilidade)
- [Crítica de design em equipe](#crítica-de-design-em-equipe)
- [Arquitetura de informação](#arquitetura-de-informação)
- [Recrutamento, consentimento e síntese](#recrutamento-consentimento-e-síntese)
- [Sinais de alerta](#sinais-de-alerta)
- [Números que parecem iguais e não são](#números-que-parecem-iguais-e-não-são)
- [Lacunas](#lacunas)

## Escolher o método

| Pergunta | Método | Quem faz |
| --- | --- | --- |
| Como as pessoas fazem X hoje? Como reagem a um conceito? | Entrevista centrada em fluxo ou UI | `user-research-plan` |
| Elas conseguem completar a tarefa neste protótipo ou produto? | Teste de usabilidade moderado | `user-research-plan` |
| Onde esta tela viola princípios conhecidos? | Avaliação heurística (opinião barata, antes de testar) | `heuristic-eval` |
| Como o conteúdo deve ser agrupado? | Card sorting (descoberta) | `user-research-plan` |
| A estrutura proposta ou existente é encontrável? | Tree testing | `user-research-plan` |
| O design está coerente e em linha com as metas? | Crítica em equipe | humanos |
| Qual problema vale resolver? Quantos usuários? | Descoberta, survey, JTBD | `/product-discovery-specs:playbook` |

## Heurísticas de Nielsen

Dez heurísticas com os nomes oficiais (NN/g; lista de 1990 com Molich, refinada em 1994 por análise fatorial de 249 problemas, página revisada em 2024-01-30):

1. Visibilidade do estado do sistema.
2. Correspondência entre o sistema e o mundo real.
3. Controle e liberdade do usuário.
4. Consistência e padrões.
5. Prevenção de erros.
6. Reconhecimento em vez de memorização.
7. Flexibilidade e eficiência de uso.
8. Estética e design minimalista.
9. Ajudar o usuário a reconhecer, diagnosticar e se recuperar de erros.
10. Ajuda e documentação.

## Avaliação heurística

Procedimento do artigo de Moran e Gordon (2023): **3 a 5 avaliadores independentes**, 1 a 2 horas cada, escopo estreito, duas passadas (primeiro aprender o fluxo, depois procurar violações), consolidação por agrupamento por afinidade. Violação de heurística não é automaticamente problema: contexto e trade-offs contam; e a avaliação não substitui pesquisa com usuários.

Adaptação para um modelo (conflito C6): rode 2 ou 3 passadas independentes em contextos separados (`design-evaluator`), consolide por agrupamento, rotule tudo Inferido e recomende usuários reais para os 3 achados mais graves. Uma passada única é uma opinião.

Formato por achado: heurística · local exato (tela e elemento) · evidência · severidade 0 a 4 · correção sugerida. Violação que for escolha defensável de contexto vira "trade-off a validar". Proibido projetar taxa de abandono ou conversão.

Exemplo (checkout em 4 passos, mensagem "Falha na operação" e cupom que apaga o carrinho ao errar): H9 · passo 3, banner de erro · texto genérico sem causa nem ação · severidade 3 (afeta toda falha de pagamento, bloqueia a tarefa, persiste a cada tentativa) · correção: dizer o que aconteceu, por quê e o que fazer. H5 · campo de cupom · digitar um código inválido apaga o carrinho · severidade 4 (perda de trabalho do usuário) · correção: validar o cupom sem tocar nos itens.

## Severidade de 0 a 4

Escala do artigo de Nielsen de 1994 (o artigo de procedimento de 2023 não traz escala):

| Nota | Significado | Insumos |
| --- | --- | --- |
| 0 | Não concordo que seja um problema de usabilidade | |
| 1 | Cosmético: corrigir só havendo tempo | **frequência** (com que frequência ocorre), **impacto** (quão difícil é superar), **persistência** (acontece toda vez ou só na primeira) |
| 2 | Menor: baixa prioridade | |
| 3 | Maior: alta prioridade | |
| 4 | Catástrofe: corrigir antes de lançar | |

Para sessões de teste, use a mesma escala como complemento (Inferido) junto da contagem de participantes afetados.

## Entrevista de 50 minutos

Blocos da skill `user-research` da Anthropic, reescritos com a regra de neutralidade que o original não traz:

| Bloco | Tempo | Conteúdo |
| --- | --- | --- |
| 0. Antes | n/a | Pergunta de pesquisa e a decisão que ela apoia; perfil dos participantes; consentimento e gravação |
| 1. Aquecimento | 5 min | Papel, rotina, confiança |
| 2. Contexto do fluxo atual | 10 min | "Conte a última vez que você fez X": experiência concreta, não hipotética |
| 3. Aprofundamento | 20 min | Sondagens neutras: "o que aconteceu depois?", "por que isso importou?"; não sugerir a resposta; não perguntar "você usaria…?" |
| 4. Reação a conceito ou protótipo | 10 min | Tarefa antes de opinião; pensar em voz alta |
| 5. Encerramento | 5 min | "O que eu não perguntei?"; agradecer |

Marque pergunta direcionada para reescrita. Exemplo: "Você acha o filtro confuso?" → "Mostre como você encontraria pedidos de março; o que esperava ver?".

## Teste de usabilidade

Fonte: NN/g, Usability Testing 101 (2019, revisado em 2026-07-15). Para estudo qualitativo de **um grupo de usuários**, cinco participantes revelam a maioria dos problemas comuns. Roteiro de sessão: contexto e consentimento; tarefas realistas em ordem, lidas em voz alta pelo participante (a redação da tarefa muda o comportamento: priming); pedir para pensar em voz alta; observar hesitações; perguntas de acompanhamento sem influenciar; pergunta de fechamento. Registre cada problema com frequência (quantos participantes) e severidade 0 a 4. Declare o que o estudo não responde: com 5 participantes não há significância estatística nem estimativa de taxas.

## Crítica de design em equipe

NN/g, Design Critiques (2016): papéis de apresentador, críticos, facilitador (rotativo) e anotador. Roteiro de 30 minutos: escopo e objetivos; apresentação; discussão em round robin ou com cota de comentários positivos e negativos, reformulando comentários impositivos como perguntas ligadas às metas; acompanhamento com notas e itens de ação. A divisão sugerida de tempo (3, 5, 17 e 5 minutos) é Suposição, não vem do artigo. Armadilhas do facilitador: sem personas ou metas definidas, sessão longa, levar para o lado pessoal, resolver na hora, falar só dos negativos. Comece pequeno (30 minutos por semana). Não cobre crítica assíncrona.

## Arquitetura de informação

Árvore de decisão (NN/g, Tankala 2024): ainda não sei como agrupar o conteúdo → **card sorting** (descoberta, no início, para modelos mentais e agrupamentos). Já tenho uma estrutura proposta ou existente → **tree testing** (avalia encontrabilidade só com texto hierárquico; tarefas de encontrar item). O artigo recomenda usar os dois. Trechos de busca não lidos na íntegra: rótulos neutros em card sorting para evitar casamento por palavra-chave; em tree testing com várias árvores, distribuir entre participantes. **Tamanhos de amostra: lacuna**; leia `nngroup.com/articles/tree-testing/` e "card sorting: how many users to test" na íntegra antes de afirmar números.

Modelo de tarefa de tree testing: cenário ("Você quer saber se pode trocar a data de uma consulta já marcada"), "onde você procuraria?", registro de sucesso, caminho direto e tempo.

## Recrutamento, consentimento e síntese

- Recrute pessoas do perfil; não recrute amigos nem colegas. Preveja sobra para ausências: recrutar 7 para agendar 5 é heurística do autor (no-show de 20 a 30%), não norma.
- Consentimento e gravação por escrito, sem parecer jurídico. Aplicabilidade da LGPD é Suposição: confirme com o jurídico.
- Síntese: agrupamento por afinidade; teste do insight (surpreende, explica o porquê, sugere ação, vale em vários dados, cabe em uma ou duas frases). Padrão em 6 de 8 participantes é sinal e em 1 de 8 é provável ruído (heurística do autor, Inferido).
- Nunca invente participantes, citações ou resultados: o `ux-researcher` só sintetiza notas fornecidas, com citações literais das notas e contagens do que está nelas.

## Sinais de alerta

Pesquisa sem decisão associada; pergunta direcionada; recrutar amigos ou colegas; pular a síntese; insight que só confirma a crença do time; tarefa que entrega a resposta no enunciado; relatório sem "o que este estudo não responde".

## Números que parecem iguais e não são

| Número | Objeto | Fonte |
| --- | --- | --- |
| 5 | Participantes de um teste de usabilidade qualitativo com um grupo de usuários | V-17 |
| 3 a 5 | Avaliadores independentes de uma avaliação heurística | V-11 |
| 7 para agendar 5 | Heurística de recrutamento do autor, não norma | V-16 |
| 6 de 8 | Heurística do autor para chamar de sinal, não norma | V-16 |

Nunca some nem troque estes números num prompt (conflitos C7 e C14).

## Lacunas

Survey, personas, JTBD e métricas HEART: `/product-discovery-specs:playbook`. Tamanho de amostra de card sorting e tree testing: não lido. Prototipação interativa (Figma) e design sprint: sem fonte validada. Pesquisa em PT-BR e com públicos específicos (idosos, PCD): use os parâmetros de `wcag-aa.md` como piso, não como pesquisa.
