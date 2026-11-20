# REV — Revisão humana, auditoria e contribuições

Legenda em [regras-metodo.md](regras-metodo.md). Skill de apoio: `revisar-codigo-de-ia`.

## Obrigatório

- **REV-01** [A+H · C5 C2] Olhe o código por dentro a cada entrega, mesmo com "sucesso" na tela, e revise à mão cada pacote de mudanças em tudo o que importa. — _por quê:_ é o único remédio contra código descartável em volume (slop). _(caps. 5, 10)_
- **REV-02** [H · C5 C8 C13] Software para terceiros (clientes, venda, produção) exige revisão de pessoa experiente; nenhum código fica imune, seja de voluntário, de agente ou do próprio dono. — _por quê:_ sem isso, dispensar programadores é falácia. _(caps. 5, 10, 17)_
- **REV-03** [A+H · C5] Em PR ou contribuição: não confie na descrição do autor; audite o diff inteiro; resuma; a decisão final é humana; a revisão automática trata toda alegação do autor como não verificada. — _por quê:_ a descrição é hipótese; o diff é a evidência. _(caps. 9, 17, 20)_
- **REV-04** [A+H · C5 C7] Revise e audite com mais de uma combinação modelo + ferramenta, de empresas diferentes, mais a revisão humana; o resultado é a união das listas. — _por quê:_ nenhum revisor achou tudo e cada um perdeu falhas reais. _(caps. 3, 6, 16)_
- **REV-05** [A · C5] Revisores adversariais trabalham com contexto limpo; testes que já existiam são o juiz independente. _(cap. 17)_
- **REV-06** [A+H · C5 C11] Relatório de auditoria feito por IA é lista de onde olhar, não veredito: confirme cada achado crítico e afirme em público só o que foi conferido. — _por quê:_ auditoria de IA traz falsos positivos e perde falhas. _(caps. 17, 18)_
- **REV-07** [A · C5 C7] Peça auditoria de segurança nomeando classes de falha (condição de corrida em contador, segredo padrão no código, reuso de código de dois fatores, redirecionamento aberto, injeção de SQL, path traversal). — _por quê:_ achou 22 falhas só porque os tipos foram nomeados; "revise a segurança" de forma vaga não acha. _(cap. 7)_
- **REV-08** [A · C5] Na revisão, cace sabotagem explícita: alerta silenciado, exceção criada no scanner, teste desligado ou afrouxado em vez de corrigir a causa. — _por quê:_ modelos escolheram silenciar a vulnerabilidade em vez de atualizar a biblioteca. _(cap. 12)_
- **REV-09** [A · C5] Depois de um lote de contribuições, rode uma segunda auditoria (regressão, duplicação, código morto). _(cap. 17)_
- **REV-10** [A+H · C5 C13] Volume grande de contribuições passa por triagem com IA (filtrar, resumir, comparar com o objetivo) e aprovação de uma pessoa que responde. _(cap. 17; ap. J)_
- **REV-11** [A+H · C5 C8] Antes de liberar, responda por escrito: vai para produção? aguenta a carga? é seguro? é manutenível? integra com o resto? resolve o problema certo? Se algum "não", diga por quê e como corrigir. _(cap. 19)_
- **REV-12** [H · C5] Mantenha atrás do agente alguém que saiba dizer o que reescrever e qual bug passou; revisão proporcional ao risco, sem publicar às cegas nem fiscalizar cada vírgula. _(cap. 19)_
- **REV-13** [A · C5 C11] Ao consolidar revisões: falha de lógica conferida se corrige sem votação; problema de clareza só entra se mais de um revisor apontar; gosto isolado fica de fora. — _por quê:_ evita ruído sem perder erro real. _(posfácio)_
- **REV-14** [A · C5 C11] Revisores simulados (personas com papel e receio definidos, só leitura, lendo tudo na ordem) avaliam texto ou produto; o que eles apontam é hipótese, conferida contra o produto e depois com pessoas reais. — _por quê:_ revisão de forma não diz se o leigo foi convencido; falhas típicas: conclusão maior que a evidência, argumento que nunca perde, remissão errada. _(cap. 21; posfácio; ap. A)_
- **REV-15** [A · C5 C7] Para julgar software feito com IA, de terceiros ou nosso: alguém revisa antes de entrar? há testes e CI que rodam de verdade? os autores usam no dia a dia? falhas relatadas recebem correção e explicação? vai mexer com senhas, arquivos ou dinheiro (então exija mais)? _(cap. 17)_

## Proibido

- **REV-P01** [A · C5] Confiar numa única auditoria (de IA ou humana) ou supor que dois agentes juntos acham tudo. — _por quê:_ duas auditorias acharam os mesmos furos graves, mas cada uma perdeu outros. _(caps. 6, 16)_
- **REV-P02** [H · C5] Tomar a própria revisão linha a linha de grande volume como suficiente, ou usar "o modelo erra pouco" como argumento. — _por quê:_ revisão manual de volume não pega o erro quieto. _(cap. 20)_
- **REV-P03** [A · C5 C7] Enviar ou aceitar relatório de segurança gerado por LLM sem verificação de especialista. — _por quê:_ relato falso custa horas a quem mantém; houve programa de recompensa suspenso por isso. _(cap. 17)_
- **REV-P04** [A · C5 C10] Usar como medida a nota de qualidade que um modelo dá ao código. _(cap. 17)_
- **REV-P05** [O · C5 C13] Usar proibição de IA, detector de texto de IA ou marca d'água como controle ou prova de autoria. — _por quê:_ autoria não é detectável com certeza; a marca some com paráfrase; proibir só funciona em comunidade pequena. _(caps. 4, 17; ap. J)_
- **REV-P06** [A · C5] Partir do pressuposto de que código escrito por pessoas é seguro e o gerado por IA não é. — _por quê:_ todo código tem bug; muda a escala. _(cap. 17)_
- **REV-P07** [A · C5 C11] Manter no relatório narrativa que não é evidência conferível. _(posfácio)_

## Sinais de alerta

- **REV-S01** [A · C5] Revisão ausente: volume de commits implausível para leitura humana, funções de milhares de linhas, aninhamento muito profundo. _(cap. 17)_
- **REV-S02** [A · C5] Processo ruim vira relaxo industrializado; o modelo rende dentro de um processo de engenharia e só nele. _(cap. 17)_
- **REV-S03** [A · C5] Falso positivo de varredura é comum (um "keylogger" era log de depuração): confirme o contexto antes de acusar. _(cap. 18)_
- **REV-S04** [A · C5] Erro que o compilador não pega (uso de memória já devolvida, regra de negócio entre operações) foi pego por revisão humana ou adversarial. _(ap. J)_
