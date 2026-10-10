# Roteiro de entrevista de descoberta (JTBD, 30 minutos) e modelo de anotações

Base: V-33, skill `interview-script` do phuryn/pm-skills (MIT, Paul Huryn): seções com tempo, perguntas sobre o passado e cinco regras anti-viés. O roteiro abaixo é redação própria, e os links de curso pago da fonte não foram reproduzidos. Lacunas declaradas: a fonte primária de JTBD (Christensen, Ulwick, Moesta) e o livro "The Mom Test" não foram lidos no atlas; este arquivo não atribui o método a eles.

## Sumário

- [Antes da entrevista](#antes-da-entrevista)
- [Roteiro de 30 minutos](#roteiro-de-30-minutos)
- [Perguntas sobre o passado](#perguntas-sobre-o-passado)
- [Perguntas a evitar e como reformular](#perguntas-a-evitar-e-como-reformular)
- [Regras anti-viés](#regras-anti-viés)
- [Modelo de anotações](#modelo-de-anotações)
- [Quantas entrevistas](#quantas-entrevistas)

## Antes da entrevista

Entradas necessárias (peça se faltar):

| Entrada | Pergunta |
| --- | --- |
| Objetivo | Que decisão esta rodada vai informar? |
| Premissas a validar | O que precisa ser verdade para a ideia fazer sentido? (3 a 5 afirmações) |
| Perfil do participante | Quem entrevistar, com que critério de recrutamento, quem fica de fora? |
| Contexto | Entrevistador, anotador, gravação (com consentimento), local e duração |

Boas práticas de preparo: nunca entreviste só amigos e quem já gosta do produto; combine anotador separado quando possível; avise o participante do objetivo sem revelar a solução; peça permissão antes de gravar e diga como os dados serão tratados (LGPD: conferir com jurídico, Inferido).

## Roteiro de 30 minutos

| Seção | Tempo | Objetivo | Exemplo de fala |
| --- | --- | --- | --- |
| Abertura | 2 a 3 min | deixar a pessoa à vontade; combinar regras | "Quero entender como você lida com X no dia a dia. Não há resposta certa; não estou vendendo nada. Posso gravar?" |
| Aquecimento | 5 min | contexto da pessoa | "Me conte um pouco do seu trabalho e de como X aparece nele." |
| Exploração (JTBD) | 15 a 20 min | comportamento passado e o "trabalho" que a pessoa contrata | perguntas da próxima seção |
| Encerramento | 3 a 5 min | fechar sem pitch | "Tem algo que eu deveria ter perguntado? Conhece alguém que lida com isso de outro jeito?" |

Os tempos somam 25 a 33 minutos; ajuste a exploração ao tempo real combinado.

## Perguntas sobre o passado

Modelos próprios, no espírito de V-33 (que cita "me conte a última vez que..." e "o que abriria mão para resolver isso?"). Use 6 a 8 e aprofunde com "e então?" e "por quê?".

1. Me conte a última vez que você [fez / precisou fazer X]. Como foi do começo ao fim?
2. O que você estava tentando conseguir naquele momento? O que aconteceu logo antes?
3. O que você usou ou fez para resolver (ferramenta, planilha, pessoa, gambiarra)?
4. O que foi mais difícil, demorado ou irritante nessa vez?
5. Quanto tempo ou dinheiro isso custou? Quem mais teve que se envolver?
6. O que você já tentou antes e por que parou?
7. O que você abriria mão para resolver isso?
8. Da última vez que isso deu errado, o que você fez depois?

Aprofundamento neutro: "pode me dar um exemplo?", "como você sabia que tinha dado certo?", "o que fez você decidir isso naquele dia?".

## Perguntas a evitar e como reformular

| Evitar | Problema | Reformular |
| --- | --- | --- |
| "Você usaria um app que faz X?" | opinião sobre o futuro; a pessoa agrada | "Como você resolve X hoje? Me conte a última vez." |
| "Você acha que seria útil...?" | elogio genérico | "O que você faz quando isso acontece? O que custa?" |
| "Quanto pagaria por isso?" | preço hipotético | "Quanto gasta hoje com isso (tempo ou dinheiro)?" |
| "Você sempre/geralmente faz X?" | generaliza | "Da última vez que X, o que você fez?" |
| "Não seria melhor se...?" | pergunta indutiva | "Como você gostaria que fosse?" só depois de ouvir o passado |
| Apresentar a solução antes de ouvir | contamina todo o resto | guarde para o encerramento, ou para outra sessão |

## Regras anti-viés

1. Pergunte sobre a vida do participante, não sobre a sua ideia.
2. Pergunte sobre comportamento passado e específico, não sobre intenção futura.
3. Ouça muito mais do que fala (referência de V-33: cerca de 80% de escuta).
4. Não apresente solução durante a exploração.
5. Trate elogio genérico ("legal!", "usaria sim!") como ruído; peça um exemplo concreto ou ignore.

Rótulo: estas regras vêm de V-33 (secundária, B 7). O Mom Test não foi lido; não atribua a ele.

## Modelo de anotações

Cada entrevista gera um arquivo `notas-<id-participante>.md`. O ID de cada nota permite que a síntese cite sem inventar.

```markdown
# Entrevista <ID-participante>  (data AAAA-MM-DD, duração <min>, perfil: <critério de recrutamento>)
Consentimento para gravar: sim | não   Anotador: <nome>

## Notas literais (uma ideia por linha; trecho entre aspas = fala literal)
- N01 [passado] "Da última vez fiz tudo numa planilha e perdi dois pedidos."
- N02 [relatado] Usa três ferramentas para o mesmo controle.
- N03 [opinião] Acha que automatizar seria bom.      <- marcar como opinião
- N04 [elogio-genérico] "Legal a ideia!"             <- ruído

## Premissas confrontadas
| Premissa | Evidência a favor (IDs) | Evidência contra (IDs) | Status |
| --- | --- | --- | --- |
| P1 | N01, N02 | | sustentada por 1 pessoa (amostra pequena) |

## Perguntas que ficaram abertas
- <pergunta para a próxima entrevista>
```

Tipos de nota: `passado` (comportamento observado ou relatado de um episódio específico), `relatado` (afirmação sobre rotina), `opinião`, `elogio-genérico`. A síntese separa os dois primeiros dos dois últimos.

## Quantas entrevistas

Não existe número validado no atlas. O guia de Teresa Torres citado em V-32 fala em entrevistas semanais e revisão a cada 3 a 4 entrevistas; pré-requisito mínimo de 3 a 4 entrevistas com histórias antes de montar a árvore. Para qualquer N: rotule o tamanho da amostra e escreva "o que esta amostra não permite concluir".
