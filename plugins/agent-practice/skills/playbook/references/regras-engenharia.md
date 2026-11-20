# ENG — Processo de engenharia com agentes

Legenda em [regras-metodo.md](regras-metodo.md).

## Obrigatório

- **ENG-01** [A · C2] Uma funcionalidade pequena por vez, já com a organização certa e testes; um commit por fatia verde, com descrição própria. — _por quê:_ cada commit é um ponto de retorno barato; dezenas de commits por dia sem caos. _(cap. 5; aps. G, J)_
- **ENG-02** [A · C2 C3] TDD: o teste que falha vem antes; todo bug corrigido ganha teste que impede a volta. — _por quê:_ cerca de 1,5 linha de teste por linha de código permitiu velocidade sem regressão. _(cap. 6; epílogo)_
- **ENG-03** [A+H · C2] Refatore em passos pequenos e frequentes, protegidos por testes que já existiam; o humano decide o que extrair; depois de refatoração grande, cace código morto. — _por quê:_ sem refatoração só se empilha código; refatorar move código sem apagar a origem. _(caps. 5, 6)_
- **ENG-04** [A · C2] Escreva para o leitor-agente: arquivos e funções pequenos (alvo: menos de 500 linhas por arquivo), separados por responsabilidade; nomes únicos e buscáveis; comentários que explicam o porquê, preservados em toda refatoração. — _por quê:_ o agente lê em fatias, busca por texto e não sabe por que um caminho estranho existe. _(cap. 9)_
- **ENG-05** [A · C2] Automatize as regras de qualidade (tamanho máximo de arquivo e função, estilo, análise estática) para o acúmulo não passar despercebido. — _por quê:_ função de 3 mil linhas nasce de acúmulo sem reorganização. _(cap. 17; ap. J)_
- **ENG-06** [A · C1 C2] Antes de construir peça complexa do zero, pesquise componente, biblioteca ou modelo pronto (inclusive pré-treinado). — _por quê:_ dias de heurísticas foram trocados por um modelo pronto de poucas centenas de linhas. _(caps. 5, 8)_
- **ENG-07** [A · C2] Antes de usar uma API de biblioteca, confira o código-fonte instalado ou a documentação da versão em uso; prefira consultar a documentação a confiar na memória do modelo. — _por quê:_ modelos inventam métodos; o laço de consulta iguala versões e linguagens. _(caps. 12, 22)_
- **ENG-08** [A · C2 C9] Centralize configuração (nome de modelo, parâmetros, trechos de prompt) num único lugar. — _por quê:_ o nome de um modelo espalhado em 24 arquivos custou um commit inteiro para trocar uma linha. _(cap. 7)_
- **ENG-09** [A · C2 C8] Padronize projetos (scripts de build, deploy e release) para que pedidos curtos como "faça o deploy" funcionem. — _por quê:_ o padrão vira manual escrito uma só vez e reaproveitado. _(cap. 9)_
- **ENG-10** [A+H · C2 C3] Pare e repense quando correção corrige correção, mexer num ponto quebra outro, ou o agente faz e desfaz sem convergir: mude a pergunta e revise as suposições sobre o ambiente. — _por quê:_ é sinal de castelo de cartas ou de premissa errada (2 horas perdidas por uma regra de ignorar pasta). _(caps. 5, 8, 22)_
- **ENG-11** [A+H · C2] Descarte sem apego a abordagem errada, mesmo que tenha custado caro; prototipe em cópia temporária, compare abordagens com dados, anote o aprendido e apague. — _por quê:_ refazer ficou barato; o fracasso também. _(caps. 7, 8, 10, 20)_
- **ENG-12** [A+H · C3] Quando o agente sugerir "aceitar e documentar" um defeito que ninguém entende, investigue a cadeia inteira antes de aceitar. — _por quê:_ custo desproporcional ao entendimento indica causa mais funda (era um único inteiro de configuração). _(cap. 8)_
- **ENG-13** [A · C2 C9] Etapa automática para após poucas falhas consecutivas (por exemplo, 3) e vai para diagnóstico. — _por quê:_ sem esse limite, centenas de milhares de chamadas por dia foram desperdiçadas. _(cap. 2)_
- **ENG-14** [A · C3] Depuração: reprodução em 100% das tentativas antes de investigar; bissecção do histórico quando a origem é incerta; em sistema desconhecido, altere categorias inteiras de suspeitos de uma vez para mapear o terreno e examine o suspeito de natureza diferente. — _por quê:_ sem antes e depois mensuráveis caça-se fantasma. _(caps. 5, 8; ap. J)_
- **ENG-15** [A · C3 C12] Quando um agente entra em círculo, troque de agente ou reinicie a sessão do zero com a passagem de turno. — _por quê:_ contexto entulhado derruba qualquer modelo. _(ap. J)_
- **ENG-16** [A+H · C1 C2] Escolha linguagem e stack pelo problema e pelo tamanho do ecossistema, e teste a stack com o agente antes de contar com ele; erro recorrente do agente vira regra, teste ou skill, não troca de linguagem. — _por quê:_ testes pesaram mais que a linguagem; agentes vão melhor em stacks populares e convencionadas. _(caps. 10, 19; ap. J)_
- **ENG-17** [A · C2 C12] Trabalhe com lista de pendências visível, permita interrupção sem perder a sessão e preserve a tarefa original. _(cap. 3)_
- **ENG-18** [A · C2 C12] Paralelize (ou use vários agentes) só em lotes independentes: traduzir cem documentos, converter duzentas imagens, a mesma mudança em cinquenta arquivos, com instrução de estilo e revisão por item. Trabalho com caminho crítico fica com um agente, um bom modelo, ferramenta madura e pedido melhor. — _por quê:_ delegação forçada piorou qualidade e tempo. _(caps. 3, 11; interlúdio 1)_
- **ENG-19** [A · C2] Trabalho em etapas numeradas, reexecutáveis sem estrago, com progresso persistido para retomar depois de uma queda. — _por quê:_ alinha o método sem microgerenciar. _(cap. 9)_
- **ENG-20** [A · C2] Mesmo em ferramenta pessoal: testes, build automatizado, release e configuração no lugar certo; ferramentas pessoais para pequenas irritações ficaram baratas (descrever, prototipar, testar, empacotar, descartar se ruim). — _por quê:_ evita gambiarra largada. _(cap. 10)_
- **ENG-21** [A · C2] Em linguagem rígida o agente roda os testes e corrige os avisos antes de entregar; a primeira versão nunca é aceita sem rodar. _(caps. 9, 10)_
- **ENG-22** [A+H · C2 C6] Migração ou reescrita grande: documento revisado de regras de conversão; ensaio em poucos arquivos; implementador, dois revisores adversariais de contexto limpo e um corretor; fila de erros por pacote; suíte de testes independente como juiz e CI multiplataforma como árbitro; quando agentes se atropelam, proíba comandos perigosos e separe cópias por frente; orce o custo antes. — _por quê:_ foi o método que tornou viável uma migração de meio milhão de linhas, e não saiu de graça. _(cap. 17; ap. J)_
- **ENG-23** [A+H · C2] A automação gera a linha de base correta; otimização que a máquina não consegue provar (organização de dados, desempenho fino) é revisada por quem conhece. _(cap. 8)_
- **ENG-24** [A · C2 C10] Ao experimentar receitas (configuração, prompts, treino), use grupo de controle, uma mudança por vez e um ponto de decisão antes de gasto grande. — _por quê:_ mudanças misturadas impediram saber o que funcionou. _(cap. 14)_
- **ENG-25** [A+H · C2] Em núcleo pequeno e crítico, considere prova formal verificada por máquina. — _por quê:_ o verificador pegou um erro de "um a mais" que os testes de exemplo deixaram passar. _(ap. J)_
- **ENG-26** [A+H · C2] Mantenha poucos projetos ativos e marque experimentos de poucos dias como experimentos. _(posfácio)_
- **ENG-27** [A · C2 C5] Projeto aberto a contribuições mantém testes verdes, documentação e versões numeradas; PRs externos são revisados e reforçados. _(cap. 7)_
- **ENG-28** [A · C2 C11] Trate qualquer produto, inclusive texto e documentação, como produto: especificação única, verificação que bloqueia a montagem, revisões, versões numeradas e changelog; em material para público misto, o detalhe técnico vai para apêndice. _(posfácio; ap. A)_
- **ENG-29** [A · C11 C12] Trabalho derivado de fontes começa com inventário lacrado (hash e ponto exato do histórico de cada fonte), formulário fixo por fonte (tese, afirmações a conferir, o que envelhece, o que cortar e por quê) e mapa de linhagem; ao corrigir uma fonte, reconfira só o que depende dela. — _por quê:_ material de um mês já estava obsoleto meses depois. _(posfácio)_
- **ENG-30** [A+H · C2 C11] Rode um piloto antes de escalar; cada dúvida resolvida vira regra escrita que todo agente lê antes de produzir; registre conflitos entre agentes paralelos e o escopo de cada número. _(posfácio)_

## Proibido

- **ENG-P01** [A+H · C2] Deixar o agente trabalhar horas sem olhar o código. — _por quê:_ arquivos de milhares de linhas e zero testes cresceram enquanto só se recarregava a tela. _(cap. 5)_
- **ENG-P02** [A · C2] Empilhar filtros e regras manuais contra falsos positivos ou ajustar limites numéricos no olho. — _por quê:_ cada remendo abre outra porta; mudar a segunda casa decimal quebrou tudo. _(cap. 8)_
- **ENG-P03** [A · C2] Achar que um prompt substitui pensar no problema. — _por quê:_ velocidade acelera também a direção errada. _(cap. 8)_
- **ENG-P04** [A · C2] Aceitar código só porque compila, sem revisar nem reorganizar antes do commit. _(cap. 17)_
- **ENG-P05** [A · C2] Deixar testes e CI "para depois", inclusive em projeto pessoal. — _por quê:_ o projeto sem testes teve seis rodadas de refatoração tardia e um terço da velocidade. _(cap. 6)_
- **ENG-P06** [A · C3] Tratar sintoma como causa. — _por quê:_ esconde o defeito. _(ap. J)_
- **ENG-P07** [A · C3 C11] Seguir o que o agente traz de fóruns em tema controverso ou depuração sem conferir. — _por quê:_ guias datados e contraditórios viram resumo confiante. _(cap. 8; ap. J)_
- **ENG-P08** [A · C12 C10] Forçar delegação multiagente esperando velocidade, ou montar planejador caro com executor barato para economizar. — _por quê:_ modelos fortes não delegaram sozinhos; forçar custou qualidade e dobrou o tempo; o orquestrador vira muleta. _(caps. 3, 11)_
- **ENG-P09** [H · C13] Maratonas de hiperfoco (30 horas em 3 dias) ou forçar volume com jornadas longas. — _por quê:_ custa saúde e dinheiro e gera código descartável. _(caps. 5, 10)_
- **ENG-P10** [A · C2] Confiar que o modelo mantém o padrão em projeto grande. — _por quê:_ ele mudou a lógica do servidor para o navegador no meio do caminho; interrompa quando mudar de padrão sem motivo. _(cap. 5)_
- **ENG-P11** [A · C2] Prometer detector universal de bugs por linguagem ou ferramenta, ou atribuir todo ganho de uma reescrita à linguagem. — _por quê:_ só se prova programa a programa; os ganhos têm causas misturadas. _(cap. 19; ap. J)_
- **ENG-P12** [A · C2 C9] Resolver item isolado quando o problema exige contexto anterior (traduzir um trecho sem a página). — _por quê:_ a falha reaparece e o custo cresce. _(cap. 8)_

## Sinais de alerta

- **ENG-S01** [A · C2] Trocar de linguagem não resolve arquitetura: muda apenas que tipo de erro é barato de pegar; falha de regra de negócio atravessa qualquer compilador. _(ap. J)_
- **ENG-S02** [A · C2] Velocidade e estabilidade andam juntas nos melhores times; arquivos que só crescem e o agente fazendo e desfazendo no mesmo lugar são alarme. _(caps. 5, 20)_
- **ENG-S03** [A · C2] Faxina (centralizar configuração, dividir arquivos) só acontece quando a dor aparece: registre a dor e o conserto. _(cap. 7)_
- **ENG-S04** [H · C2 C3] O agente sugerir parar é sensato; continuar é decisão humana. Do lado humano faltam, em geral: saber abandonar, recusar solução não entendida, dar meio de medir e trazer domínio. _(cap. 8)_
- **ENG-S05** [A · C2] As práticas de XP continuam valendo com agentes: par, teste primeiro, CI, entregas pequenas e padrão de código; estimativas são ordem de grandeza. _(caps. 5, 6, 10)_
