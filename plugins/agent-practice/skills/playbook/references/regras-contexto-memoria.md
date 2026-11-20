# CTX — Contexto, memória e sessões

Legenda em [regras-metodo.md](regras-metodo.md). Modelos: [passagem de turno](../assets/templates/passagem-de-turno.md) e [arquivo de instruções do projeto](../assets/templates/agents-md-projeto.md).

## Obrigatório

- **CTX-01** [A+H · C2 C12] Desde o primeiro dia o projeto tem um arquivo de instruções para agentes (`AGENTS.md`/`CLAUDE.md`) com arquitetura, comando de testes, convenções, proibições e proteções exigidas. — _por quê:_ o agente só lembra o que está escrito; sem o arquivo, ignorou convenção básica e gerou retrabalho de mil linhas. _(caps. 5, 9)_
- **CTX-02** [A · C2 C12] Esse arquivo é curto, direto e no imperativo; cada linha custa contexto em todo pedido. Uma regra entra quando a mesma correção se repete pela terceira vez. — _por quê:_ ele é relido a cada mensagem. _(cap. 9)_
- **CTX-03** [A · C12] Cada problema novo descoberto (bloqueio de serviço, armadilha de ambiente, pegadinha de domínio) vira linha no documento vivo do projeto ou em procedimento escrito. — _por quê:_ a sessão seguinte já começa sabendo. _(caps. 6, 16)_
- **CTX-04** [A · C12] Memória em três gavetas: regras (arquivo de instruções), decisões e pesquisas (documentos versionados no repositório) e meio do caminho (defeitos abertos, hipóteses descartadas, onde parou). — _por quê:_ sem isso cada sessão começa como estagiário com amnésia. _(cap. 9; ap. G)_
- **CTX-05** [A · C12] Organize a memória em camadas: índice curto sempre carregado, arquivos por tópico lidos sob demanda e transcrições só por busca; escreva o tópico antes de atualizar o índice e mantenha o índice pequeno. — _por quê:_ índice que vira depósito piora tudo. _(cap. 2; ap. J)_
- **CTX-06** [A · C0 C12] Ao fim de cada sessão com estado a retomar (implementação, investigação, trabalho longo), antes de compactar ou ao trocar de agente, grave a passagem de turno: onde parou, o que falhou, o que falta, decisões e motivos; a próxima sessão lê isso primeiro. Em pergunta pontual ou auditoria sem escrita, a passagem vai no chat ou é N/A. O agente salva decisões sem esperar que peçam. — _por quê:_ compactação e troca de ferramenta perdem detalhe. _(cap. 2; ap. G)_
- **CTX-07** [A · C12] Registre tudo o que não virou código: pesquisas, decisões com motivo, alternativas descartadas, hipóteses e descartes de investigação. — _por quê:_ sem registro o conhecimento evapora no fim da sessão. _(caps. 2, 9; ap. J)_
- **CTX-08** [A · C0 C12] Trate anotação de memória como pista: confira no projeto real antes de agir sobre ela. — _por quê:_ anotação errada é pior que nenhuma: sem anotação o agente pergunta; com a errada, segue convicto no rumo errado. _(cap. 2)_
- **CTX-09** [A+H · C12] Quem escreve memória confere o que escreveu; o humano revisa memória e instruções periodicamente, corrige contradições e apaga o que está errado; conhecimento duradouro é consolidado em páginas por conceito. — _por quê:_ a memória é um bilhete que alguém escreveu e pode estar errado. _(cap. 2; ap. G)_
- **CTX-10** [A · C12] Decisão que precisa sobreviver vai para documento revisado e versionado; memória automática guarda só o que talvez importe; transcrição de sessão é evidência, não regra. — _por quê:_ separa o provável do certo. _(aps. G, H)_
- **CTX-11** [A · C12] Memória do projeto fica em texto portável (Markdown em Git), legível por qualquer ferramenta, com banco apenas como índice reconstruível; para trocar de agente, gere documento de estado, decisões e próximos passos. — _por quê:_ evita ficar refém de um fornecedor. _(caps. 2, 22; ap. H)_
- **CTX-12** [A · C12] Filtre dados sensíveis antes de gravar memória e saiba onde a pasta de memória fica, com backup dela. — _por quê:_ a memória grava o que acontece nas sessões. _(ap. H)_
- **CTX-13** [A · C0 C12] Reafirme o essencial em vez de supor que o combinado de uma hora atrás continua no contexto; quando a sessão escorregar, peça resumo das decisões, confira e recomece a partir dele. — _por quê:_ o modelo não lembra, relê; a compactação perde o começo. _(cap. 2)_
- **CTX-14** [A · C12] Use agente sério com janela de contexto grande (200 mil tokens ou mais) e não encha o contexto só porque cabe. — _por quê:_ janela pequena resume toda hora; cada token é relido, cobrado e piora a recuperação do que importa. _(caps. 2, 3)_
- **CTX-15** [A · C0 C12] Se uma decisão sumiu na compactação, consulte o registro ou pergunte; nunca reconstrua a justificativa. — _por quê:_ o modelo inventa motivo plausível. _(cap. 2)_
- **CTX-16** [A · C12] Antes de produzir, leia o contrato do trabalho: arquivo de instruções, guia de estilo e arquivo de continuidade (nomes, onde cada conceito já foi tratado). — _por quê:_ é o arquivo de instruções em escala. _(posfácio)_
- **CTX-17** [A · C12] Prefira apontar um exemplo vivo ("faça como no módulo X") a criar skill; skill só para procedimento que se repete igual, versionada, refinada a cada erro e removida quando envelhece; mantenha poucas skills, todas em uso. — _por quê:_ cada skill disputa atenção; mais ferramentas não fazem agente melhor. _(cap. 9; ap. J)_
- **CTX-18** [A · C12] Consolidação automática de memória só com gatilho e trava contra concorrência; converta datas relativas em absolutas, remova fatos contraditos e pode o índice; funções que reescrevem ou descartam memória ficam desligadas sem histórico recuperável. — _por quê:_ memória ruim é pior que nenhuma. _(aps. H, J)_
- **CTX-19** [A · C12] Resumo de compactação preserva: pedido original, arquivos tocados, erros corrigidos, pendências, estado atual e todas as mensagens do usuário. _(cap. 2)_
- **CTX-20** [A · C12] Memória compartilhada entre agentes ou máquinas registra quem escreveu cada página e usa passagem de turno com dono único (uma só sessão assume); com troca frequente de agente, repasse só o que aconteceu nos outros. _(ap. H)_

## Proibido

- **CTX-P01** [A · C12] Usar a janela de contexto ou a memória nativa de um único fornecedor como memória do projeto. — _por quê:_ somem ao fechar a sessão ou ao trocar de ferramenta. _(aps. G, H)_
- **CTX-P02** [A · C12] Gravar automaticamente uma "regra" a cada falha. — _por quê:_ vira cemitério de superstições; muitas falhas eram passageiras. _(cap. 2)_
- **CTX-P03** [A · C12] Arquivo de regras longo ou em prosa filosófica. — _por quê:_ densidade importa; ele ocupa contexto em todo pedido. _(cap. 9)_
- **CTX-P04** [A · C12] Saída de log verbosa sem controle, sobretudo com janela pequena. — _por quê:_ um log falante enche o contexto. _(cap. 3)_
- **CTX-P05** [A · C12] Depender só de disciplina manual para registrar memória em projeto longo; automatize a captura quando possível. — _por quê:_ falha nos dias cansados. _(ap. H)_

## Sinais de alerta

- **CTX-S01** [A · C12] Contexto perdido: decisão de horas atrás esquecida, abordagem descartada repetida, erro já corrigido de volta, contradição com o início da conversa. _(cap. 2)_
- **CTX-S02** [H · C12] O humano virou o cache do agente quando precisa explicar o projeto de novo a cada troca. _(ap. H)_
- **CTX-S03** [A · C12] Sessão entulhada de tentativas gera repetição cega: reinicie limpa a partir da passagem de turno. _(ap. J)_
- **CTX-S04** [A · C12] Memória compartilhada (servidor de memória entre agentes) compensa com troca de agente no meio do trabalho, várias máquinas, retorno após semanas ou equipe; fora disso, pasta de documentos e compactação bastam, e o servidor é mais uma peça para manter de pé. _(aps. G, H)_
- **CTX-S05** [A · C12] Quando o acervo cabe no contexto, busca por palavra com um leitor forte costuma bastar; busca vetorial fica para acervos enormes, mídia, vocabulário divergente e latência baixa (e erra sem avisar: parecido não é relevante). _(cap. 2; ap. J)_
- **CTX-S06** [A · C12] Ciclo saudável de memória: captura, consolidação, consulta no início da sessão e passagem de turno. Tudo o que o modelo enxerga é o contexto; o que ficou fora não existe para ele. _(aps. B, H)_
