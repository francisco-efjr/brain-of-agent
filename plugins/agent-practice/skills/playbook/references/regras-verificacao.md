# VER — Verificação, oráculo e evidência

Legenda em [regras-metodo.md](regras-metodo.md). Skill de apoio: `definir-oraculo`.

## Obrigatório

- **VER-01** [A · C0 C4] Toda tarefa tem um oráculo externo: algo que mede a realidade sem depender de quem fez (teste executável, implementação de referência, comparação lado a lado, verificador formal, respostas congeladas). Laço sem medida não roda. — _por quê:_ onde havia medida independente o agente rendeu; onde não havia, só produziu volume. _(caps. 3, 8, 19, 22)_
- **VER-02** [A · C0 C4] Pergunte sempre quem escreveu a verificação: o mesmo modelo não escreve o código e o dublê (mock) ou teste que o valida; verificação feita pelo réu não vale como prova. — _por quê:_ mock sob medida para um método inexistente deu teste verde com app quebrado. _(cap. 12; ap. J)_
- **VER-03** [A · C0 C4] Prove pelo comportamento real: suba o sistema, use, meça; depuração visual pede navegador ou dispositivo real; ignore o que o modelo declara sobre o próprio trabalho. — _por quê:_ "dois processos em paralelo" era um só. _(caps. 3, 7, 11, 12)_
- **VER-04** [A · C0 C4 C6] Meça na fonte, não pelo relato: conte arquivos e processos, compare tamanho e conteúdo, confira o que de fato foi enviado ao modelo ou ao serviço. — _por quê:_ todas as falhas graves do ano tiveram alguém acreditando no próprio relatório. _(caps. 12, 16)_
- **VER-05** [A · C0 C4] Confirme quem executou (qual modelo, qual ferramenta, qual versão) e leia os registros por baixo do "concluído"; erro repetido no log com conclusão sem falha é erro mascarado; defeito de medição só aparece debaixo do número. — _por quê:_ uma ferramenta trocou de modelo em silêncio e o resultado foi atribuído ao modelo errado. _(caps. 3, 11; ap. F)_
- **VER-06** [A · C2 C4] Testes rodam com um único comando, sem configuração manual e com saída previsível; CI roda a suíte inteira em todo commit; só commit verde entra na linha principal. — _por quê:_ a CI pegou bug real mais de 50 vezes em 274 commits. _(caps. 6, 9)_
- **VER-07** [A · C4] Além dos testes isolados, teste o sistema inteiro com serviços reais (inclusive o LLM) e dados realistas obtidos com segurança. — _por quê:_ mocks não testam o contrato entre peças; dados reais revelaram caracteres perdidos e limites que dublê não tem. _(cap. 6; ap. J)_
- **VER-08** [A · C4] Avalie o que os testes cobrem (núcleo, caminho de erro, chamada central), não quantos são; dê a cada teste que pode mentir um controle (entrada vazia que deve falhar, sentinela de conclusão, sementes diferentes). — _por quê:_ 11 testes bons valeram mais que 37 que ignoravam o núcleo. _(cap. 11; ap. J)_
- **VER-09** [A · C0 C4] No fim, revise requisito a requisito como Passou, Parcial ou Falhou, cada um com evidência; assuma as falhas. — _por quê:_ falha admitida vale mais que sucesso inventado. _(cap. 11)_
- **VER-10** [A · C0] Rotule toda afirmação como Verificado (executado), Inferido, Suposição ou Não verificável; leitura de código não é execução; peça ao modelo que cite só o material fornecido e marque o que não puder verificar. — _por quê:_ reduz a invenção, mesmo sem eliminá-la. _(caps. 4, 9)_
- **VER-11** [A · C4 C10] Antes de acusar alucinação, confira na fonte (código ou documentação da biblioteca); se a acusação estava errada, refaça a avaliação e corrija os textos derivados. — _por quê:_ o auditor errou e o erro ficou meses em vários textos. _(caps. 3, 11; ap. J)_
- **VER-12** [A · C0 C11] Números, datas e nomes são conferidos contra a fonte primária; quando um resumo (inclusive de agente) discorda da fonte, vale a fonte. Quando dois números discordam, descubra o motivo e declare o escopo de cada um, sem escolher o mais bonito; o que não foi verificado fica fora. — _por quê:_ a conferência pegou datas, custos e tipos de estudo errados em resumos. _(cap. 11; epílogo; posfácio; ap. A)_
- **VER-13** [A · C4] Teste em dois níveis: trecho isolado contra uma referência e o sistema inteiro com o mesmo roteiro de entrada. _(cap. 8)_
- **VER-14** [A+H · C4 C8] Use o resultado de verdade (instale, use no dia a dia) e coloque-o diante de usuários reais. — _por quê:_ o teste pega o que foi especificado; o uso pega o que ninguém sabia especificar. _(caps. 17, 20)_
- **VER-15** [A · C4] Antes de dizer "pronto", revise a saída final inteira (documento, áudio, vídeo gerado) e teste no ambiente real de destino, com casos fora do que foi treinado ou ensaiado. — _por quê:_ trecho de 90 segundos virou 9 minutos inventados; modelo bom no treino falhou num "olá, mundo". _(caps. 13, 14; ap. J)_
- **VER-16** [A+H · C4 C5] Audite o erro silencioso à parte: testes e modelos pegam o que quebra, não o que está errado em silêncio (teste adulterado, soma errada, índice removido). — _por quê:_ falha barulhenta aparece em minutos; erro quieto só com auditoria própria. _(caps. 11, 19)_
- **VER-17** [A · C4 C11] Tenha um verificador automático, como uma CI, que reprova violação das regras do projeto (estilo, link quebrado, citação inexistente, saída sem origem). — _por quê:_ entrega com erro não passa. _(posfácio)_
- **VER-18** [A · C4 C11] Itere ler-editar-ler até os problemas pararem de voltar; cada padrão de falha vira regra escrita; aceite que a conferência por agentes deixa passar erros e mantenha um canal de correção aberto. — _por quê:_ edição cria problema novo; as falhas caíram rodada a rodada mas não zeraram. _(posfácio; ap. A)_
- **VER-19** [A · C4 C12] Ao retomar processo longo, confira hash, passo exato, estado e dados antes de continuar; não confie no nome do arquivo ("último"). — _por quê:_ o arquivo "mais recente" carregou um passo antigo. _(ap. J)_
- **VER-20** [A · C4] Falha de infraestrutura ou de montagem não é erro do código nem do modelo: conserte e rode de novo antes de concluir. _(ap. J)_
- **VER-21** [A · C4 C9 C10] Congele as respostas certas antes de rodar qualquer modelo e teste isolados os casos críticos de regra; separe treino e prova por unidade inteira (projeto, cliente), com uma prova final trancada usada uma vez e um ambiente isolado, sem rede, contra testes fixos. — _por quê:_ o mesmo projeto dos dois lados vira cola; prova parecida demais com a aula engana. _(caps. 13, 14; ap. J)_
- **VER-22** [A · C4 C10] Escolha entre versões só por tarefas executadas em lista congelada antes, nunca por métrica interna do processo (perda de treino, nota que o modelo se dá). — _por quê:_ a perda caiu e o acerto também. _(cap. 14)_
- **VER-23** [A · C4 C10] Desconfie de resultado bom demais: inspecione o log e rode de novo; o defeito pode estar no avaliador. _(caps. 12, 14)_
- **VER-24** [A+H · C4 C5] Procure pontos cegos com um adversário dedicado (red team), inclusive em sistema forte. — _por quê:_ desempenho excelente em quase tudo não exclui falha sistemática. _(interlúdio 2)_
- **VER-25** [A · C4 C9] Em classificação ou decisão automática, meça a calibração (confiança declarada contra acerto) e interprete "99% de acerto" pela raridade do alvo, pelo número de casos e pelo custo de cada erro. — _por quê:_ num teste, 48 de 71 respostas dadas com confiança acima de 90% estavam erradas. _(cap. 15; ap. B)_
- **VER-26** [A · C4] Em lotes grandes, revise por amostragem priorizando os piores casos. — _por quê:_ cerca de 10% de um lote bom ainda exigiu ajuste. _(interlúdio 1)_
- **VER-27** [A · C4 C2] Em interface, teste a direção nas páginas internas, no celular, nos estados de erro e nos e-mails, não só no protótipo; o humano decide o que preservar. _(cap. 21)_

## Proibido

- **VER-P01** [A · C0 C4] Aceitar como prova "todos os testes passam" quando os testes foram escritos pelo próprio agente sem conferência. — _por quê:_ teste que simula API inventada certifica a alucinação; sinais: método que a biblioteca real não tem, nota que salta ao trocar pelo real. _(caps. 6, 7, 11, 12)_
- **VER-P02** [A · C0 C4] Aceitar sinal verde de ferramenta (backup concluído, cópia OK, pipeline terminou limpo) como prova de que o objetivo foi atingido. — _por quê:_ é a ferramenta falando de si. _(aps. G, J)_
- **VER-P03** [A · C4 C10] Concluir com rodada única ou com amostra escolhida a dedo. — _por quê:_ a mesma pergunta rende respostas diferentes; cada caso novo vira surpresa. _(caps. 1, 8, 11)_
- **VER-P04** [A · C4] Declarar vitória porque o resultado tem formato certo ou parece código válido. — _por quê:_ de 42 respostas erradas, 39 pareciam perfeitas. _(cap. 14)_
- **VER-P05** [A · C0 C4] Supor que o agente leu o arquivo ou a saída inteira. — _por quê:_ ferramentas truncam em silêncio. _(cap. 2)_
- **VER-P06** [A · C2 C4] Gerar código traduzido ou otimizado às cegas, sem medida de correção e de desempenho. _(cap. 8)_
- **VER-P07** [A+H · C4] Parar em 80% de acerto quando o domínio exige mais, ou empilhar regras manuais tentando os últimos pontos. — _por quê:_ chegar a 95% pedia centenas de regras; o último 1% pode ser inviável. _(cap. 8)_

## Sinais de alerta

- **VER-S01** [A · C4] Tarefa parecida com o que o modelo viu sai direto; tarefa inédita ou de domínio fechado (regra interna, hardware sem documentação) só avança com verificador automático, e o agente não a resolve sozinho. _(cap. 22; ap. B)_
- **VER-S02** [A · C4] Modelo pode aprender a afirmar "os testes passaram" sem passar; construir e revisar são capacidades distintas. _(caps. 11, 14)_
- **VER-S03** [A · C4] Degraus diferentes: sintaxe válida não é correção, correção não é uso de ferramenta, uso de ferramenta não é memória longa; protocolo não é habilidade e contexto não é memória. _(cap. 14; ap. J)_
