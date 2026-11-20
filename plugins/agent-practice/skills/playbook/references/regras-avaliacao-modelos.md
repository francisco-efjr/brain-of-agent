# AVA e CUS — Avaliação de modelos, benchmarks, anúncios e custo

Legenda em [regras-metodo.md](regras-metodo.md). Skill de apoio: `avaliar-modelo`. Modelo: [relatório de avaliação](../assets/templates/relatorio-avaliacao-modelo.md).

## Obrigatório — avaliação

- **AVA-01** [A · C10] Avalie a combinação modelo + ferramenta (harness) + prompt + contexto, nunca o modelo isolado; o mesmo harness pode injetar instruções diferentes por família de modelo. — _por quê:_ trocar só o harness levou um modelo de 24 para 91 e outro de 57 para 18. _(caps. 3, 11)_
- **AVA-02** [A+H · C10] Antes de decisão com dinheiro ou risco, rode o seu teste: tarefa parecida com a real (que você sabe resolver), candidatos várias vezes, comparação às cegas e medida do trabalho humano que sobra; afirmações sobre modelos se baseiam em medição reproduzível que mostra como foi montada e onde errou. — _por quê:_ nenhum anúncio publica o que interessa ao seu trabalho; modelo menor ganhou do maior. _(prefácio; caps. 7, 11, 19; epílogo; aps. I, J)_
- **AVA-03** [A · C10] Repita as rodadas e registre o ruído; diferença dentro do ruído não conta; leia o topo como grupo e use faixas por trabalho humano restante (A: menos de 30 min de conserto; B: 1–2 h; C e D: mais). — _por quê:_ o mesmo modelo tirou 100 e 91 na mesma prova. _(cap. 11)_
- **AVA-04** [A · C10] Use rubrica com quesitos ponderados, leitura arquivo por arquivo e auditoria cega por avaliador independente, conferida à mão. — _por quê:_ a auditoria cega descobriu que a imagem dita de produção era de desenvolvimento, e a nota caiu de 96 para 85. _(cap. 11)_
- **AVA-05** [A · C10 C7] Isole o ambiente de avaliação: sem plugins e configurações pessoais, sem rubrica, gabarito, relatórios ou entregas de terceiros ao alcance; varra os logs e anule a rodada contaminada. — _por quê:_ modelos leram gabarito e código de concorrente; a prova à prova de cola se faz no ambiente, não na instrução. _(caps. 3, 11, 12)_
- **AVA-06** [A · C10] Guarde e, quando publicar, publique pedido, código, registros, critérios e correções do teste. — _por quê:_ só gráfico impede contestação. _(cap. 11; ap. I)_
- **AVA-07** [A · C10] Aposente prova saturada (quase todos entre 95 e 100); use cenários em teia (um projeto que evolui em etapas) e sabotagens plantadas sem aviso, pontuadas por peso (achou e corrigiu sozinho = total; só depois de revelada = parcial; nunca = zero). — _por quê:_ teste que todos gabaritam não enxerga nada acima do teto. _(caps. 11, 19, 22; ap. J)_
- **AVA-08** [A+H · C10] Entre candidatos da faixa A, escolha por custo, tempo e ferramenta que já usa, comparando também o nível de esforço de raciocínio. — _por quê:_ no topo a escolha é quase indiferente para o dia a dia; o custo variou mais de cem vezes com nota parecida. _(caps. 11, 22)_
- **AVA-09** [A · C10] Confirme que o modelo medido é o contratado (roteamento silencioso, troca de modelo pela ferramenta, intermediários). _(cap. 15)_
- **AVA-10** [A · C10] Custo real soma todas as voltas e releituras de cache; audite o código que extrai as métricas; desconfie de "por centavos" e confie na ordem de grandeza. — _por quê:_ custos saíram 7 vezes e até 40–90 vezes abaixo do real. _(caps. 11, 15; aps. I, J)_
- **AVA-11** [A · C10] Não deixe o agente desenhar o benchmark sem checar o viés dele (tende a desafios isolados que saturam rápido). _(ap. J)_
- **AVA-12** [A · C10] Declare escopo e limites do método: prova pequena serve para comparar versões; benchmark de tarefa única não se generaliza; análise estática não prova comportamento; caixa-preta via API não certifica a origem de um modelo; não achar não prova ausência. _(caps. 12, 14, 18; aps. I, J)_
- **AVA-13** [A · C10] Com pesos abertos, verifique derivação com evidência refazível por qualquer um; se o ganho de um derivado vem do original, use o original, salvo avaliação reproduzível em contrário. _(cap. 12)_
- **AVA-14** [A · C10] Documente publicamente o caminho errado quando um benchmark seu se mostrar ruim. _(ap. J)_
- **AVA-15** [A · C10] Avalie no trabalho real, não em demonstração: produção recorrente, termos técnicos, sem babá; dê um boletim de critério único (estabilidade e usabilidade, 1–10) a cada projeto ou ferramenta, porque publicado não é bom. — _por quê:_ o substituto barato falhou num episódio real de 30 minutos; projeto sem usuário tende a nota baixa. _(caps. 10, 13)_
- **AVA-16** [A · C10] Treino ou ajuste próprio: confira onde ficam os parâmetros (vocabulário emprestado pode consumir a maior parte) e compare modelos por dados de treino e tarefas, não só por número de parâmetros. — _por quê:_ 154 de 239 milhões de parâmetros estavam na tabela de vocabulário. _(cap. 14)_

## Obrigatório — leitura de benchmark (responda antes de citar uma tabela)

- **AVA-B01** [A · C10] Qual tarefa, qual ferramenta e qual critério de correção? _(ap. I)_
- **AVA-B02** [A · C10] Quantas rodadas? Uma rodada é amostra de um. _(ap. I)_
- **AVA-B03** [A · C10] A diferença supera o ruído entre execuções? Se não, escolha a faixa e decida por preço, tempo e ferramenta. _(ap. I)_
- **AVA-B04** [A · C10] Quem corrigiu, e pedido, código, registros e erratas estão publicados? _(ap. I)_
- **AVA-B05** [A · C10] Como contaram o custo (cache relido, soma dos passos)? _(ap. I)_
- **AVA-B06** [A · C10] A prova está saturada? _(ap. I)_
- **AVA-B07** [A · C10] A resposta pode ter vazado para o treino (prova antiga e famosa)? Passar no corretor não é ser aceito por quem mantém o projeto. _(cap. 11; ap. I)_
- **AVA-B08** [A · C10] Quem escreveu a verificação? Teste e mock do mesmo modelo concordam com o erro. _(ap. I)_
- **AVA-B09** [A · C10] Havia gabarito acessível ao modelo durante a prova? Nota alta demais pede leitura do log. _(ap. I)_
- **AVA-B10** [A · C10] O teste diz algo confiável sobre de onde o modelo veio? Só com acesso aos pesos dá para provar a origem. _(ap. I)_
- **AVA-B11** [A · C10] Você rodou o seu teste? Que tarefa, medida de que jeito, em quantas repetições, comparada com quais alternativas e por quanto? _(cap. 11; ap. I)_

## Obrigatório — leitura de anúncio, promessa ou "estudo" de IA

- **AVA-C01** [A · C10 C13 C14] Pergunte sempre: serve para quê, quem conferiu e quanto custa. _(prefácio)_
- **AVA-C02** [A · C10 C14] Separe em três colunas: medido por terceiro independente, palavra de quem vende, ninguém sabe; o barulho está na coluna do meio. _(cap. 12; ap. I)_
- **AVA-C03** [A · C10 C14] Quem lucra se você acreditar (abertura de capital, venda de chip, curso)? Interesse não prova falsidade, mas exige prova mais forte, inclusive de quem escreve o guia; quando alerta e lucro apontam na mesma direção, redobre o escrutínio. Sinais de empresa se preparando para abrir capital: despesa chamada de investimento, contratação em massa, nenhuma data para lucro. _(prefácio; caps. 1, 15, 22; ap. I)_
- **AVA-C04** [A · C10 C14] Alguém independente consegue testar? Capacidade anunciada como perigosa demais, acesso restrito a parceiros ou fila de espera continuam sendo só alegação. _(cap. 15; ap. I)_
- **AVA-C05** [A · C10 C14] Qual a definição do termo grande ("AGI", "zero alucinação", "precisão")? Pode ser meta contratual, definição conveniente ou concordância com outro modelo; restringir a saída impede categoria inventada, não categoria errada. _(cap. 15; ap. I)_
- **AVA-C06** [A · C10 C14] Comparado com quem e com qual régua? Procure no texto a explicação de como o número saiu; número sem comparação e sem régua declaradas não vale. _(cap. 15; ap. I)_
- **AVA-C07** [A · C10 C14] O que é o produto sem o nome novo? Muito "novo paradigma" é prática antiga renomeada; não pague por rótulo sem recibo de projetos reais que melhoraram. _(cap. 15; ap. I)_
- **AVA-C08** [A · C10 C14] Aconteceu ou poderia acontecer? Leia verbos, condicionais e prazos ("poderia", "variante", "em 6 a 12 meses"); aceite o resultado pelo que ele provou. _(cap. 15; ap. I)_
- **AVA-C09** [A · C10 C14] Quem ganha com o seu medo? Catástrofe e milagre empurram o mesmo carrinho. _(ap. I)_
- **AVA-C10** [A · C10 C14] Quanto custou o feito? Milhões em computação mostram força bruta, não inteligência. _(cap. 15; ap. I)_
- **AVA-C11** [A · C10 C14] Os que concordam têm fontes independentes? Dez reproduções do mesmo comunicado e duas IAs concordando com a sua hipótese são uma voz só; ferramenta recomendada por muita gente com o mesmo tom liga o alarme e é ponto de partida para investigar. _(cap. 15; ap. I)_
- **AVA-C12** [A · C10 C14] A credencial confere com datas, artigo e autores? E o "treinamos o nosso modelo": com quanto texto, contra qual prova, quem de fora conferiu? _(caps. 14, 15; ap. I)_
- **AVA-C13** [A+H · C10 C13 C14] Você precisa disso hoje? Dê um mês de prazo antes de se assustar ou de comprar; adote camada nova só quando a falta dela doer; clones e "mortes de produto" anunciados se conferem lendo os avisos e testando. _(caps. 15, 20; ap. I)_
- **AVA-C14** [A · C10 C11] Defina antes o que mudaria a sua conclusão e julgue por medições de quem não vende o modelo; a decisão é sua, não do benchmark, do influenciador ou do autor. _(caps. 11, 22; epílogo)_

## Proibido

- **AVA-P01** [A · C10] Tratar demonstração de anúncio, "feito em 40 minutos", "a nova versão é melhor" ou painel de agentes como desempenho típico. — _por quê:_ o exemplo famoso foi o melhor de dez sorteios; a versão nova de um modelo caiu 15 pontos. _(caps. 1, 7, 10, 11)_
- **AVA-P02** [A+H · C10 C13] Escolher modelo pelo marketing ("caro e perigoso demais") ou comprar ferramenta e curso por medo de ficar para trás. — _por quê:_ o modelo vendido assim empatou com o anterior custando quase o dobro. _(prefácio; cap. 15; epílogo)_
- **AVA-P03** [A · C10] Afirmar por impressão que os modelos deram um salto de inteligência, ou creditar ao modelo um ganho que veio da ferramenta em volta. _(cap. 3)_
- **AVA-P04** [A · C10] Acusar plágio ou fraude sem prova; descreva só o que a evidência mostra (por exemplo, falha de atribuição). _(cap. 12)_
- **AVA-P05** [O · C10 C13] Confiar em métrica que virou prêmio. — _por quê:_ premiar bug corrigido estimula criar bug; modelos e pessoas contornam a régua (reward hacking nasce de decisões humanas encadeadas). _(caps. 12, 15)_
- **AVA-P06** [A · C10] Confundir pesos abertos com grátis ou com "roda em casa", ou esperar que um modelo destilado tenha o conhecimento do professor. — _por quê:_ destilado copia estilo, não memória factual. _(cap. 13)_
- **AVA-P07** [A · C10 C11] Usar autoridade como argumento ("fulano diz que entendem"). _(ap. B)_

## Obrigatório — custo e escolha de ferramenta

- **CUS-01** [A+H · C10 C12] Mantenha medidor de uso visível com alerta antes do teto; comece refatoração grande só com cota fresca; perto do limite, passe a tarefa a outro agente (de outro fornecedor) ou recarregue antes de travar; em lote, estime o consumo antes. — _por quê:_ estourar o limite no meio de tarefa grande perde a tarde. _(interlúdio 1; ap. G)_
- **CUS-02** [A · C10 C12] Ajuste o nível de esforço à tarefa: baixo para traduzir e resumir; alto para vulnerabilidade, bug difícil e otimização. Para leitura em massa, modelo menor; reserve o mais forte para verificação e decisão. _(cap. 22)_
- **CUS-03** [A+H · C10] Em uso pesado, assinatura mensal costuma sair mais barata que pagar por token; modelo barato só se a qualidade aceitar; não migre para pagamento por pedido por pressa — descansar até a cota voltar pode ser o mais barato. _(caps. 5, 10)_
- **CUS-04** [A · C10 C9] Use prompt caching e meça o volume relido do cache. — _por quê:_ corta até 90% do custo do texto repetido; uma execução releu milhões de tokens. _(cap. 3)_
- **CUS-05** [A+H · C10] Alugue o modelo de quem estiver melhor no mês; memória, processo e conhecimento ficam seus, em formato aberto. — _por quê:_ limites, preços e qualidade mudam sem aviso. _(cap. 22)_
- **CUS-06** [A+H · C10] Modelo local só se o hardware já estiver disponível para outro uso ou se o dado for proibido de sair do ambiente. Dimensione por memória (o que cabe) e largura de banda (velocidade), mais o cache da conversa; use pelo menos 4 bits de quantização para código e raciocínio; não divida o modelo entre memória de vídeo e RAM; modelo de mistura de especialistas é rápido, mas ocupa a memória do modelo inteiro. Custo local soma máquina, energia e horas: escreva "não medido", nunca "zero". — _por quê:_ comprar máquina cara para economizar centavos por decisão é comprar problema. _(cap. 13; ap. J)_
- **CUS-07** [A+H · C10] Serviço pago que poupa horas pode valer mais que infraestrutura própria barata; a diferença de centavos entre modelos é irrelevante diante do custo de uma decisão errada. _(cap. 13)_
- **CUS-08** [A+H · C10 C13] Adote camada nova (orquestrador, framework, curso) só quando a falta dela doer; comece pelo agente que já usa, direto. _(cap. 15)_
- **CUS-09** [A+H · C10] Antes de especializar um modelo, decida qual tarefa vale especializar e como medir; prefira adaptar modelo aberto pronto a treinar do zero, investindo em exemplos e medição. _(cap. 14)_
- **CUS-10** [A+H · C10 C12] Escolha o agente pela fase: um rende mais em pesquisa e experimento, outro na execução do que já foi decidido; registre a observação com data. _(cap. 7)_

## Proibido — custo

- **CUS-P01** [A+H · C10] Comprar solução "a IA aprende sozinha" ou banco vetorial por moda. — _por quê:_ o que parecia indispensável numa época virou opcional em menos de três anos. _(cap. 2)_

## Sinais de alerta

- **AVA-S01** [A · C10] A inteligência de base segue curva em S: cada geração custa mais (chip, memória, energia) para melhorar menos; o que cresceu em 2025–2026 foi o uso de ferramentas em sequência, que dobra o tamanho da tarefa autônoma a cada poucos meses. Separe "cérebro" de "mãos" ao avaliar ganho; dados de treino de qualidade estão acabando (tendência, não prova). _(caps. 1, 3, 14, 19, 22; ap. B)_
- **AVA-S02** [A · C10] Desempenho sobre-humano em quase tudo não exclui ponto cego sistemático que um adversário dedicado acha. _(interlúdio 2)_
- **AVA-S03** [A · C10] Tokenização explica erro em contar letras; português e termos técnicos viram mais pedaços e custam mais. _(ap. B)_
